import cadquery as cq

# Base block dimensions
length = 140
width = 70
height = 25

# Cutout dimensions
cutout_x = -15
cutout_y = 15

# Pin dimensions and positions
pin_radius = 4
pin_height = 15
pin_fillet = 3.5
pin_positions = [(-45, -20), (45, 20)]

# Tool (cavity) dimensions
narrow_radius = 3.5
wide_radius = 10
sphere_radius = 13
sphere_center_x = 40
sprue_radius = 2

# 1. Create base block with the side cutout
base_sketch = (
    cq.Workplane("XY")
    .moveTo(length/2, -width/2)
    .lineTo(-length/2, -width/2)
    .lineTo(-length/2, cutout_y)
    .lineTo(cutout_x, cutout_y)
    .lineTo(cutout_x, width/2)
    .lineTo(length/2, width/2)
    .close()
)
base = base_sketch.extrude(-height)

# 2. Add alignment pins on the top face
pins = (
    base.faces(">Z").workplane()
    .pushPoints(pin_positions)
    .circle(pin_radius)
    .extrude(pin_height)
)
# Fillet the top edges of the pins (selecting highest Z edges)
base_with_pins = pins.edges(">Z").fillet(pin_fillet)

# 3. Create the cavity tool
# The tool is built centered on Z=0 so that subtracting it leaves a perfect half-cavity
revolved_part = (
    cq.Workplane("XZ")
    .moveTo(-75, 0)
    .lineTo(-75, narrow_radius)
    .lineTo(cutout_x, narrow_radius)  # Straight narrow channel
    .threePointArc((5, 5.5), (25, wide_radius))  # Flared transition
    .lineTo(35, wide_radius)  # Straight wide channel
    .lineTo(35, 0)
    .close()
    .revolve(360, (-75, 0, 0), (35, 0, 0))
)

# Spherical end
sphere_part = cq.Workplane("XY").center(sphere_center_x, 0).sphere(sphere_radius)

# Small sprue/vent channel at the right end
sprue_part = (
    cq.Workplane("YZ")
    .workplane(offset=sphere_center_x)
    .circle(sprue_radius)
    .extrude(40)  # Extrude completely past the right edge
)

# Combine all tool parts into a single solid
tool = revolved_part.union(sphere_part).union(sprue_part)

# 4. Subtract the tool from the base block to create the mold cavity
result = base_with_pins.cut(tool)