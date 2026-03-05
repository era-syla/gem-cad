import cadquery as cq

# Define parametric dimensions
length = 100.0
width = 70.0
height = 30.0
top_thickness = 8.0
front_wall_depth = 32.0
stem_width = 20.0
back_overhang = 15.0
corner_radius = 10.0
cutout_radius = 20.0

# Calculate derived dimensions
stem_length = length - front_wall_depth - back_overhang
lower_height = height - top_thickness

# 1. Create the lower structural part (central stem + front block)
lower_sketch = (
    cq.Sketch()
    # Central stem
    .push([(back_overhang + stem_length / 2.0, 0)])
    .rect(stem_length, stem_width)
    # Front block/wall
    .push([(length - front_wall_depth / 2.0, 0)])
    .rect(front_wall_depth, width)
)

lower_part = (
    cq.Workplane("XY")
    .placeSketch(lower_sketch)
    .extrude(lower_height)
)

# 2. Create the top plate
top_plate = (
    cq.Workplane("XY")
    .workplane(offset=lower_height)
    .box(length, width, top_thickness, centered=(False, True, False))
)

# 3. Combine the lower part and top plate, cleaning up coplanar faces
body = lower_part.union(top_plate).clean()

# 4. Apply fillets to the two front vertical corners
body = body.edges(">X and |Z").fillet(corner_radius)

# 5. Create and apply the front semi-circular cutout
# The cutter is made slightly taller and shifted down to avoid coplanar face issues during the cut
cutter = (
    cq.Workplane("XY")
    .center(length, 0)
    .cylinder(height + 2.0, cutout_radius, centered=(True, True, False))
    .translate((0, 0, -1.0))
)

result = body.cut(cutter)