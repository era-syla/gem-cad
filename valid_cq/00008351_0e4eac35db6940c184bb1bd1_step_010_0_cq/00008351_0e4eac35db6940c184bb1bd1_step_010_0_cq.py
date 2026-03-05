import cadquery as cq

# Parameters for the stepped mandrel
hex_width = 10.0      # Width across flats for the hex head
head_height = 8.0     # Height of the hex head
total_length = 80.0   # Total length of the tool
shaft_length = 70.0   # Length of the tapered section
base_diameter = 8.0   # Diameter of the shaft at the base (near head)
tip_diameter = 0.5    # Diameter at the very tip
num_steps = 25        # Number of ridges/steps along the taper
step_groove_depth = 0.2 # Depth of the indentation between steps

# Create the Hex Head
# We use polygon for the hex shape
head = (
    cq.Workplane("XY")
    .polygon(6, hex_width / 0.866025) # converting flat-to-flat to corner-to-corner (approx)
    .extrude(head_height)
)

# Create the main tapered shaft
# We'll create a simple cone first representing the envelope
shaft_base_plane = head.faces(">Z").workplane()

# Instead of a smooth cone, we need the stepped/ridged look.
# We can achieve this by stacking cylinders or truncated cones.
# Looking at the image, it looks like a series of small segments.
# Let's construct it by iterating and fusing segments.

# Calculate step height
step_height = shaft_length / num_steps

# We will build the shaft as a single object by lofting or simple union, 
# but to get the "ridged" look, a simple cone isn't enough.
# The image shows distinct rings. Let's model it as a stack of truncated cones 
# where the top of one is slightly smaller than the bottom of the next, 
# or by cutting grooves into a main cone.

# Approach: Create a main cone, then cut grooves.
# This is often more robust in CAD kernels than unioning 50 small solids.

# 1. Create the main solid cone
main_cone = (
    shaft_base_plane
    .circle(base_diameter / 2.0)
    .workplane(offset=shaft_length)
    .circle(tip_diameter / 2.0)
    .loft(combine=True)
)

# 2. Cut grooves to create the stepped appearance.
# The grooves are likely circular cuts spaced evenly.
# We'll create a profile to revolve-cut or just a series of torus cuts.
# A simpler way that often looks cleaner in code is to make the "steps" explicit.

# Let's try the stack approach for a more precise "stepped" look if the boolean overhead is okay.
# Actually, the image looks like a smooth taper with rings. 
# Let's stick to the base shape (Hex + Cone) and add the rings as cuts.

tool_body = head.union(main_cone)

# Create the cutter for the grooves
# We want to cut rings along the length.
# We will define a cutter profile on a plane passing through the Z axis (XZ plane) and revolve cut it.

groove_cutter = cq.Workplane("XZ")

for i in range(num_steps):
    # Calculate position along Z
    z_pos = head_height + (i + 0.5) * step_height
    
    # Calculate radius at this height (linear interpolation)
    # r = r_base + (r_tip - r_base) * (current_length / total_shaft_length)
    current_dist = (i + 0.5) * step_height
    t = current_dist / shaft_length
    current_radius = (base_diameter/2.0) * (1-t) + (tip_diameter/2.0) * t
    
    # Create a small notch profile. 
    # To make it visible on a taper, the cut needs to be perpendicular to the surface or just horizontal.
    # Simple horizontal torus cut works well.
    # We position a rectangle or circle to remove material.
    
    # Using a simple triangular notch or small circle for the groove
    # Offset slightly inward from the outer surface
    groove_cutter = (
        groove_cutter
        .workplane()
        .moveTo(current_radius, z_pos)
        .circle(step_height * 0.15) # Small circular groove
    )

# Perform the cut
# Note: Revolve cutting multiple disjoint profiles in one go can sometimes be tricky in OCCT.
# If it fails, we iterate. But let's try one operation first.
# CadQuery's cut method with a revolved solid is standard.
# However, generating `num_steps` separate circles in one sketch and revolving might be complex.

# Alternative: Construct the shaft as a series of lofts to simulate segments directly.
# This is often safer and cleaner for "stepped" geometry.

stepped_shaft = cq.Workplane("XY").workplane(offset=head_height)

for i in range(num_steps):
    # Bottom of this segment
    h_bottom = i * step_height
    radius_bottom = (base_diameter/2.0) * (1 - (h_bottom/shaft_length)) + (tip_diameter/2.0) * (h_bottom/shaft_length)
    
    # Top of this segment
    h_top = (i + 1) * step_height
    radius_top = (base_diameter/2.0) * (1 - (h_top/shaft_length)) + (tip_diameter/2.0) * (h_top/shaft_length)
    
    # We create a segment. To make the "ridge" visible, the bottom of the NEXT segment
    # should ideally be distinct, but a smooth loft just recreates the cone.
    # The image shows ridges. This implies the diameter steps DOWN at each interval.
    # Like a telescope.
    
    # Let's model it as a stack of cylinders or cones where the top radius of segment N
    # is slightly LARGER than bottom radius of segment N+1? Or imply a groove?
    
    # Let's simulate the ridges by making each segment a slight bulge or taper.
    # Let's make each segment a truncated cone, but ensure the start of the next one matches?
    # No, to get the ridged look seen in the image (which looks like distinct bands), 
    # let's assume slight convex curvature or grooves.
    
    # Let's go with the groove approach on a solid cone, implemented via a loop of cuts.
    pass

# Re-implementing the robust cut loop
final_model = tool_body

for i in range(1, num_steps): # Skip the very base and very tip to avoid edge artifacts
    z_pos = head_height + i * step_height
    t = (i * step_height) / shaft_length
    r_at_height = (base_diameter/2.0) * (1-t) + (tip_diameter/2.0) * t
    
    # Create a cutting torus
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(r_at_height + 0.05) # Outer boundary of cut
        .circle(r_at_height - 0.05) # Depth of cut
        .extrude(0.1) # Thickness of the cut line
    )
    # This makes a thin washer. Subtracting it creates a groove.
    final_model = final_model.cut(cutter)


# Final result assignment
result = final_model