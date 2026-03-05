import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the image
main_width = 30.0          # Width of the tall vertical section
main_height_side = 60.0    # Height of the straight vertical edges
top_arch_offset = 5.0      # Height of the curve peak above the side edges
flange_width = 25.0        # Width of the lower horizontal section
flange_height = 20.0       # Height of the flange
thickness = 25.0           # Depth of the extrusion

large_cutout_radius = 12.0 # Radius of the bottom cutout on the main block
small_cutout_radius = 8.0  # Radius of the bottom cutout on the flange
hole_diameter = 6.0        # Diameter of the through-hole
hole_pos_y = 22.0          # Height of the hole center from the bottom

# --- Coordinate Calculations ---
# Setting origin (0,0) at the bottom-right corner of the main block
# X axis points right, Y axis points up. Moving left results in negative X.
x_right = 0
x_main_left = -main_width
x_flange_left = -(main_width + flange_width)

x_main_mid = (x_right + x_main_left) / 2.0
x_flange_mid = (x_main_left + x_flange_left) / 2.0

# --- Modeling ---

# 1. Create the base L-shaped profile with a curved top
# Drawing on the XY plane to extrude along Z
profile = (
    cq.Workplane("XY")
    .moveTo(x_flange_left, 0)
    .lineTo(x_flange_left, flange_height)
    .lineTo(x_main_left, flange_height)
    .lineTo(x_main_left, main_height_side)
    # Create the convex top surface using a 3-point arc
    .threePointArc(
        (x_main_mid, main_height_side + top_arch_offset),
        (x_right, main_height_side)
    )
    .lineTo(x_right, 0)
    .close()
)

# 2. Extrude the profile to create the base solid
base_solid = profile.extrude(thickness)

# 3. Create the geometry for cuts (Cylinders)
# Large cutout on the bottom of the main block
large_cutout = (
    cq.Workplane("XY")
    .moveTo(x_main_mid, 0)
    .circle(large_cutout_radius)
    .extrude(thickness)
)

# Small cutout on the bottom of the flange
small_cutout = (
    cq.Workplane("XY")
    .moveTo(x_flange_mid, 0)
    .circle(small_cutout_radius)
    .extrude(thickness)
)

# Through-hole in the main block
hole = (
    cq.Workplane("XY")
    .moveTo(x_main_mid, hole_pos_y)
    .circle(hole_diameter / 2.0)
    .extrude(thickness)
)

# 4. Apply the cuts to the base solid
result = base_solid.cut(large_cutout).cut(small_cutout).cut(hole)