import cadquery as cq

# Overall cabinet dimensions
width = 200
depth = 70
height = 80
thickness = 3

# Create the outer box (cabinet body)
outer = cq.Workplane("XY").box(width, depth, height)

# Create inner cavity (hollow inside)
inner = cq.Workplane("XY").box(
    width - 2 * thickness,
    depth - thickness,
    height - 2 * thickness
).translate([0, thickness / 2, 0])

# Subtract inner from outer to create shell
cabinet = outer.cut(inner)

# Add vertical dividers to create three sections
# Left divider
left_divider = cq.Workplane("XY").box(thickness, depth - thickness, height - 2 * thickness).translate([-width / 6, thickness / 2, 0])

# Right divider  
right_divider = cq.Workplane("XY").box(thickness, depth - thickness, height - 2 * thickness).translate([width / 6, thickness / 2, 0])

cabinet = cabinet.union(left_divider).union(right_divider)

# Add a horizontal shelf in the middle section
shelf = cq.Workplane("XY").box(
    width / 3 - 2 * thickness,
    depth - thickness,
    thickness
).translate([0, thickness / 2, 0])

cabinet = cabinet.union(shelf)

# Create the arch cutout in the front face of the middle panel
# The arch is a rectangle with a semicircular top
arch_width = 18
arch_height = 35
arch_center_x = 0
arch_bottom_z = 2  # slightly above bottom

# Create arch shape: rectangle + semicircle on top
arch_rect = cq.Workplane("XZ").center(arch_center_x, arch_bottom_z + arch_height / 2 - thickness).rect(arch_width, arch_height)
arch_rect_solid = arch_rect.extrude(depth)

# Semicircle on top of rectangle
semi_radius = arch_width / 2
semi_center_z = arch_bottom_z + arch_height

arch_semi = cq.Workplane("XZ").center(arch_center_x, semi_center_z).circle(semi_radius).extrude(depth)

arch_combined = arch_rect_solid.union(arch_semi)

# Cut the arch from the front face area
# Front face is at y = -depth/2
# We need to cut through just the front panel
front_panel_cut = arch_combined.translate([0, 0, 0])

cabinet = cabinet.cut(front_panel_cut)

result = cabinet