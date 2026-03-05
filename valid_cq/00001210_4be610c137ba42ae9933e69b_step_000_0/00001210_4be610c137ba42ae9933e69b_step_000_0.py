import cadquery as cq

# Parameters defining the geometry
length = 100.0         # Total length of the part along X
width_root = 35.0      # Width at the larger end (Y direction)
width_tip = 6.0        # Width at the smaller end (Y direction)
height_root = 25.0     # Height at the larger end (Z direction)
height_tip = 8.0       # Height at the smaller end (Z direction)

# Calculate a midpoint for the arc to ensure concavity
# The y-coordinate is set lower than the linear interpolation between widths
arc_mid_x = length / 2.0
arc_mid_y = (width_root + width_tip) / 2.0 * 0.55 

# 1. Create the base shape by extruding the footprint vertically
# The footprint is a wedge with a concave front face defined on the XY plane
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)                   # Back-left corner
    .lineTo(length, 0)              # Back-right corner
    .lineTo(length, width_tip)      # Front-right corner
    .threePointArc(
        (arc_mid_x, arc_mid_y),     # Midpoint of the arc (concave inward)
        (0, width_root)             # Front-left corner
    )
    .close()
    .extrude(height_root)           # Extrude to the maximum height initially
)

# 2. Create a cutting volume to taper the height
# We sketch on the XZ plane (back face) and define the profile of the empty space above the part
cutter = (
    cq.Workplane("XZ")
    .moveTo(0, height_root)
    .lineTo(length, height_tip)        # Slope line defining the top surface
    .lineTo(length, height_root + 50)  # Extend upwards to ensure full coverage
    .lineTo(0, height_root + 50)       # Return to start X
    .close()
    # Extrude in +Y direction to cut through the part
    # Note: Normal of XZ plane is -Y, so negative extrusion goes in +Y
    .extrude(-width_root * 2)          
)

# 3. Apply the cut to the base shape to achieve the sloped top surface
result = base.cut(cutter)