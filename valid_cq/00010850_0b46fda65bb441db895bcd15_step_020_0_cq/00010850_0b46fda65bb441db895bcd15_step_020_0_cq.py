import cadquery as cq

# Parametric dimensions
total_length = 200.0
shaft_diameter = 10.0
end_cap_diameter = 16.0
end_cap_length = 20.0
taper_length = 5.0
tip_diameter = 5.0

# Create the main central shaft
# We center it on the origin for symmetry
shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(total_length)

# Define a function to create an end cap
def create_end_cap():
    # Base cylinder part of the cap
    cap_base = (
        cq.Workplane("XY")
        .circle(end_cap_diameter / 2)
        .extrude(end_cap_length - taper_length)
    )
    
    # Tapered/Conical tip part
    # We create a cone by lofting two circles
    taper = (
        cq.Workplane("XY")
        .workplane(offset=end_cap_length - taper_length)
        .circle(end_cap_diameter / 2)
        .workplane(offset=taper_length)
        .circle(tip_diameter / 2)
        .loft(combine=True)
    )
    
    # Combine base and taper
    full_cap = cap_base.union(taper)
    return full_cap

# Generate the top cap
top_cap = create_end_cap()
# Move it to the top of the shaft
# The shaft was extruded from Z=0 to Z=total_length. 
# We need to position the cap at the top end.
# However, usually caps sit *on* the shaft or slightly overlap. 
# Based on the image, the thicker part seems to sleeve over or extend the shaft.
# Let's align the bottom of the cap with the top of the shaft minus a small overlap 
# or just sit flush depending on interpretation. 
# Looking closely, it looks like a distinct component on the ends.
# Let's position the top cap so its bottom face is slightly down from the top edge 
# to simulate being a fitting, or just place it at the ends.
# The image shows the total length includes the caps. Let's adjust.

# Revised Strategy:
# 1. Create the long thin cylinder (shaft).
# 2. Create the caps at the ends.
# The shaft seems to run between the caps.

# Let's recalculate positions based on center-origin for easier rotation/mirroring
shaft_length = total_length - (2 * end_cap_length)

# Create the central shaft centered on Z
# Extrude symmetrically to make positioning easier
shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(total_length - 2 * end_cap_length)
shaft = shaft.translate((0, 0, end_cap_length)) # Shift up so bottom starts at Z=end_cap_length

# Create Bottom Cap
bottom_cap = create_end_cap()
# Rotate it 180 degrees to point down
bottom_cap = bottom_cap.rotate((0,0,0), (1,0,0), 180)
# Position it at the bottom (Z=0 area relative to the total assembly if built upwards)
# Since the rotate flips it around X, it's now pointing -Z.
# We move it so its "top" (now bottom) is at Z=0? No, let's assemble cleanly.

# Let's rebuild simply using absolute positioning logic.
# Z=0 is the bottom tip of the entire assembly.

# 1. Bottom Cap
bottom_cap_part = (
    cq.Workplane("XY")
    .circle(tip_diameter / 2)
    .workplane(offset=taper_length)
    .circle(end_cap_diameter / 2)
    .loft(combine=True) # The taper
    .faces(">Z").workplane()
    .circle(end_cap_diameter / 2)
    .extrude(end_cap_length - taper_length) # The cylinder part
)

# 2. The Shaft
shaft_start_z = end_cap_length
shaft_h = total_length - (2 * end_cap_length)

shaft_part = (
    cq.Workplane("XY")
    .workplane(offset=shaft_start_z)
    .circle(shaft_diameter / 2)
    .extrude(shaft_h)
)

# 3. Top Cap
top_cap_start_z = total_length - end_cap_length
top_cap_part = (
    cq.Workplane("XY")
    .workplane(offset=top_cap_start_z)
    .circle(end_cap_diameter / 2)
    .extrude(end_cap_length - taper_length) # Cylinder part
    .faces(">Z").workplane()
    .circle(end_cap_diameter / 2)
    .workplane(offset=taper_length)
    .circle(tip_diameter / 2)
    .loft(combine=True) # The taper
)

# Combine all parts
result = bottom_cap_part.union(shaft_part).union(top_cap_part)