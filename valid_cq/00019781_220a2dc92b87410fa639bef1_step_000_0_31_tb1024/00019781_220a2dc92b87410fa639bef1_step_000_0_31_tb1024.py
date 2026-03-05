import cadquery as cq

# Parametric dimensions
base_length = 120.0
base_width = 50.0
base_thickness = 12.0

block_length = 60.0
block_height = 48.0

cutout_radius = 24.0
cutout_z = 36.0

hole_dist = 90.0
hole_radius = 5.0

# Create base and central block
base = cq.Workplane("XY").box(base_length, base_width, base_thickness, centered=(True, True, False))
block = cq.Workplane("XY").box(block_length, base_width, block_height, centered=(True, True, False))

# Combine geometries
result = base.union(block)

# Create the semi-cylindrical cutout
cylinder_cut = cq.Workplane("XZ", origin=(0, 0, cutout_z)).circle(cutout_radius).extrude(base_width * 2, both=True)
result = result.cut(cylinder_cut)

# Add mounting holes on the base
result = (
    result.faces("<Z").workplane()
    .pushPoints([(-hole_dist/2, 0), (hole_dist/2, 0)])
    .hole(hole_radius * 2)
)