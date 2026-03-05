import cadquery as cq

# --- Parameter Definitions ---
# Main body dimensions
top_diameter = 60.0       # Diameter of the top cap
top_thickness = 8.0       # Thickness of the top rounded section
stem_top_diameter = 40.0  # Diameter where the stem meets the top curve
stem_bottom_diameter = 20.0 # Diameter at the very bottom
total_height = 80.0       # Overall height of the object
stem_height = 55.0        # Height of the straight tapered section
curve_height = total_height - stem_height - top_thickness # Height of the concave transition

# Top detail (recess/groove) dimensions
groove_width = 12.0
groove_length = 25.0      # Length from edge towards center
groove_depth = 2.0
tab_radius = 4.0          # Radius of the small circular feature inside groove
tab_offset = 18.0         # Distance of tab center from edge

# --- Geometry Construction ---

# 1. Create the Profile for Revolution
# We will define a profile in the XZ plane and revolve it around Z.

# Calculate key points
# Center bottom point: (0, 0)
# Outer bottom edge: (stem_bottom_diameter/2, 0)
# Top of straight stem: (stem_top_diameter/2, stem_height)
# Bottom of top cap rim: (top_diameter/2, stem_height + curve_height)
# Top of top cap rim: (top_diameter/2, total_height)
# Center top: (0, total_height)

# Note: The transition from stem_top to rim_bottom is a concave curve (fillet-like).
# The transition from rim_bottom to rim_top is a convex curve.

# Let's build it as a stack of solids for easier control over the "loft" or "revolve" logic,
# or define a single comprehensive profile. A single revolved profile is most robust.

# Helper function to generate the profile
def make_profile():
    # Define points
    p0 = (0, 0)
    p1 = (stem_bottom_diameter / 2, 0)
    p2 = (stem_top_diameter / 2, stem_height)
    
    # The rim section
    p3_x = top_diameter / 2
    p3_y = stem_height + curve_height
    
    p4_x = top_diameter / 2
    p4_y = total_height - (top_thickness / 2) # Approximate start of top rounding
    
    p5 = (0, total_height)
    
    # Create the wire
    path = (
        cq.Workplane("XZ")
        .moveTo(*p0)
        .lineTo(*p1)
        .lineTo(*p2) # Straight taper
        .tangentArcPoint((p3_x, p3_y), relative=False) # Concave transition
        .lineTo(p4_x, p4_y) # Short vertical or straight section for rim thickness
        .radiusArc(p5, -top_diameter/1.5) # Large convex dome/curve for the top surface
        .close()
    )
    return path

# Generate the base revolution
base_profile = make_profile()
base_body = base_profile.revolve()

# Add the rim fillet to smooth the outer edge
# Selecting the edge at the widest diameter
try:
    base_body = base_body.edges(cq.selectors.NearestToPointSelector((top_diameter/2, total_height - top_thickness/2))).fillet(top_thickness/2.5)
except:
    # Fallback if selection is tricky, though calculation usually holds
    base_body = base_body.edges(f">Z").fillet(2.0)

# 2. Create the Recess Detail
# The detail looks like a rectangular slot with a rounded end, 
# cutting into the top surface from the edge.

# Create a cutting tool
cutter = (
    cq.Workplane("XY")
    .workplane(offset=total_height) # Move to top
    .moveTo(-top_diameter/2, 0)     # Start at left edge
    .line(groove_length, 0)         # Draw inward
    .moveTo(-top_diameter/2, 0)     # Reset
    
    # Draw the rectangular profile centered on Y
    .rect(groove_length * 2, groove_width) # Make it long enough to cross edge
    .extrude(-groove_depth * 2) # Extrude down
)

# Position the cutter correctly. The rect was drawn centered at (0,0), we need it at the edge.
# Actually, let's draw it precisely relative to the edge.
cutter_rect = (
    cq.Workplane("XY")
    .workplane(offset=total_height + 1.0) # Start slightly above
    .moveTo(-top_diameter/2 + groove_length/2, 0)
    .rect(groove_length, groove_width)
    .extrude(-(groove_depth + 1.0 + 2.0)) # Cut down deep enough
)

# 3. Create the "Tab" feature inside the groove
# It looks like a small semicircular ridge or button inside the groove.
# It acts like a snap fit or retention bump.

tab_center_x = -top_diameter/2 + tab_offset

# Create the flexible/snap tab shape
# This is a bit complex: it looks like a U-shaped cut *around* a central tongue.
# Let's simplify: Cut a U-shape, leaving a tongue.

# Let's refine the cutter strategy. 
# 1. Cut the main rectangular ramp/groove.
# 2. Add the specific U-shaped relief cut that defines the tab.

# Step 2a: The main ramped groove
# It looks like the floor of the groove might be angled? Let's assume flat for simplicity,
# or slightly angled.
ramp_angle = 5.0
ramp_cutter = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .transformed(rotate=(0, -ramp_angle, 0)) # Tilt the working plane
    .moveTo(-top_diameter/2 + groove_length/2 - 2, 0) # Shift out slightly to clear edge
    .rect(groove_length + 5, groove_width)
    .extrude(-10, combine=False) # Downwards
)

# Step 2b: The U-shaped relief cut
# This isolates the "tongue" in the middle.
relief_width = 1.0
tongue_width = groove_width - (2 * relief_width) - 2.0 # Slightly narrower than groove
tongue_len = 10.0

# Create a shape representing the "void" around the tongue
u_cut_sketch = (
    cq.Workplane("XY")
    .workplane(offset=total_height + 0.5)
    .moveTo(tab_center_x, 0)
    # Draw U shape
    .rect(tongue_len + 4, tongue_width + 2) # Outer boundary of cut
    .rect(tongue_len, tongue_width)         # Inner boundary (island)
    .extrude(-5)
)
# That logic creates a hollow frame. We need a boolean subtraction.
# A simpler way for the U-cut:
# Create the solid block for the groove, then add the tongue back? 
# No, let's cut the groove, then cut the U-shape slot through the floor of the groove (if it's a through-hole)
# or just deep enough to define the flexible tab. The image shows a through-slot around the tab.

# Let's construct the final assembly of operations
result = base_body.cut(ramp_cutter)

# Create the U-shaped slot that defines the flexible finger
u_slot = (
    cq.Workplane("XY")
    .workplane(offset=total_height + 2)
    .moveTo(tab_center_x, 0)
    .rect(10, groove_width + 1.0) # The outer box
    .moveTo(tab_center_x, 0)
    .rect(8, groove_width - 3.0)  # The inner box (preserves the tab)
    .extrude(-15)
)

# Since CadQuery's rect().rect() doesn't automatically XOR in extrude without a face check,
# let's explicitly make the U-shape tool.
outer_u = (
    cq.Workplane("XY")
    .workplane(offset=total_height + 2)
    .moveTo(tab_center_x, 0)
    .rect(12, groove_width)
    .extrude(-15)
)
inner_u = (
    cq.Workplane("XY")
    .workplane(offset=total_height + 2)
    .moveTo(tab_center_x + 2, 0) # Shift inner part so the U is open at one end
    .rect(12, groove_width - 2.5)
    .extrude(-15)
)
u_tool = outer_u.cut(inner_u)

# Now cut the U-slot into the main body, inside the groove
result = result.cut(u_tool)

# Add the small raised lip/bump on the tab if visible
# Image shows a rounded raised rib on the tab
rib = (
    cq.Workplane("XY")
    .workplane(offset=total_height - 1.0) # Slightly below surface
    .moveTo(tab_center_x, 0)
    .circle(groove_width/2 - 1.5)
    .extrude(1.5)
    .edges(">Z").fillet(0.5)
)

# Intersect rib with the existing tab location to ensure it sits on geometry
# But simply unioning it usually works if positioned right.
# We need to clip it to the tab shape.
result = result.union(rib)

# Finally, cleanup the intersection of the U-cut to make it look like the image
# The image shows the U-cut going through the rim.
# The previous ramp_cutter might have been too wide or simple.
# Let's refine the specific detailing.

# Re-doing the top detail for higher fidelity to the reference image:
# 1. Main body
# 2. A "finger" cutout.

final_body = base_body

# The cutout for the finger area
finger_width = 10.0
finger_length = 25.0
cutout_block = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .transformed(rotate=(0, -5, 0)) # Angle the floor
    .moveTo(-top_diameter/2 + finger_length/2 - 1.0, 0)
    .rect(finger_length + 2, finger_width)
    .extrude(-10)
)

final_body = final_body.cut(cutout_block)

# Create the finger itself (add material back)
# It's narrower than the cutout
finger_gap = 1.0
finger_stem = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .transformed(rotate=(0, -5, 0))
    .moveTo(-top_diameter/2 + finger_length/2 + 2.0, 0) # Attached at inner side
    .rect(finger_length - 4.0, finger_width - (2*finger_gap))
    .extrude(-10)
)

# We need the finger to be detached at the outer edge (the U shape)
# So we intersect the finger_stem with the original body to get the curvature back,
# then separate it. 
# Simplest approach: Just cut the U-slot.

slot_width = 1.5
u_shape_cutter = (
    cq.Workplane("XY")
    .workplane(offset=total_height + 5)
    .moveTo(-top_diameter/2 + 15, 0) # Center of the U curve
    
    # Outer path
    .line(-15, 0) # Go towards edge
    .moveTo(-top_diameter/2 + 15, 0)
    
    # Let's draw the U profile in 2D and extrude cut
    .rect(20, finger_width) # Outer area
    .moveTo(-top_diameter/2 + 15 + 2, 0) # Move 'back' to secure the base
    .rect(25, finger_width - 2*slot_width) # Inner area (the finger)
    .extrude(-20)
)
# This boolean logic is tricky in one pass. 
# Let's go with the reliable "Cut U-channel" method.

# 1. Define the finger shape
finger = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .moveTo(-top_diameter/2 + 15, 0)
    .rect(25, finger_width - 2*slot_width)
    .extrude(-10)
)
# Intersect finger with base to get top curvature
finger = finger.intersect(base_body)

# 2. Define the cutout area (finger + gaps)
void = (
    cq.Workplane("XY")
    .workplane(offset=total_height + 1)
    .moveTo(-top_diameter/2 + 15, 0)
    .rect(28, finger_width) # Slightly longer to cut edge
    .extrude(-15)
)

# 3. Apply
result = base_body.cut(void).union(finger)

# Add the little arch/bridge detail on the finger (the snap bump)
bump = (
    cq.Workplane("XY")
    .workplane(offset=total_height - 1.5)
    .moveTo(-top_diameter/2 + 12, 0)
    .rect(2, finger_width - 2*slot_width) # Width of finger
    .extrude(2.5)
    .edges(">Z").fillet(0.5)
)

# Refine the bump to be an arch
arch = (
    cq.Workplane("YZ")
    .workplane(offset=-top_diameter/2 + 12)
    .moveTo(0, total_height)
    .circle(finger_width/2 - slot_width)
    .extrude(3) # Thickness of the arch
)

# Cut the bottom of the arch to make it sit on the finger
arch = arch.intersect(
    cq.Workplane("XY").workplane(offset=total_height).rect(50,50).extrude(10)
)

result = result.union(bump)

# Apply a final rotation to match image orientation roughly
result = result.rotate((0,0,0), (0,0,1), 45)