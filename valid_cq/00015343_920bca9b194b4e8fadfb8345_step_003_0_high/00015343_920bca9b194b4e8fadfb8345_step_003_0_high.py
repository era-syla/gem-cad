import cadquery as cq

# -- Parametric Dimensions --
width = 30.0                # Total width of the part
length_straight = 40.0      # Length of the rectangular base section
base_height = 25.0          # Height of the base block
top_thickness = 6.0         # Thickness of the top plate
wall_thickness = 5.0        # Wall thickness for the base structure

# -- Calculations --
nose_radius = width / 2.0
inner_width = width - (2 * wall_thickness)
inner_radius = inner_width / 2.0
# Calculate vertical height of the straight part of the tunnel
# Total available height minus floor, ceiling, and the arc radius
tunnel_vert_height = (base_height - 2 * wall_thickness) - inner_radius

# -- Geometry Construction --

# 1. Create the Top Plate
# Constructed on the XY plane, elevated to the top of the base.
# It consists of a rectangular section and a semi-circular overhang.
top_plate = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .moveTo(0, -width / 2.0)
    .lineTo(length_straight, -width / 2.0)
    .threePointArc(
        (length_straight + nose_radius, 0),   # Point on arc (tip of nose)
        (length_straight, width / 2.0)        # End point of arc
    )
    .lineTo(0, width / 2.0)
    .close()
    .extrude(top_thickness)
)

# 2. Create the Base Block
# A simple solid block positioned under the straight section of the top plate.
base_block = (
    cq.Workplane("YZ")
    .rect(width, base_height, centered=(True, False))
    .extrude(length_straight)
)

# 3. Create the Tunnel Profile (Void)
# We create a solid representing the negative space (the tunnel) and cut it from the base.
# The profile is sketched on the YZ plane to match the base orientation.
tunnel_void = (
    cq.Workplane("YZ")
    .moveTo(inner_width / 2.0, wall_thickness)
    .lineTo(inner_width / 2.0, wall_thickness + tunnel_vert_height)
    .threePointArc(
        (0, wall_thickness + tunnel_vert_height + inner_radius),       # Top of arch
        (-inner_width / 2.0, wall_thickness + tunnel_vert_height)      # End of arch
    )
    .lineTo(-inner_width / 2.0, wall_thickness)
    .close()
    .extrude(length_straight)
)

# Cut the tunnel from the base block
base_final = base_block.cut(tunnel_void)

# 4. Final Combination
# Union the top plate and the hollowed base
result = top_plate.union(base_final)