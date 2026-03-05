import cadquery as cq

# Parameters
base_length = 120
base_width = 60
base_thickness = 5
wall_height = 20
wall_thickness = 5
hole_diameter = 4

# Base plate
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Left wall with two holes
wall1 = (
    cq.Workplane("XY")
    .box(base_length, wall_thickness, wall_height)
    .faces(">Y")
    .workplane()
    .pushPoints([(-base_length/4, 0), (base_length/4, 0)])
    .hole(hole_diameter)
    .translate((0, base_width/2 - wall_thickness/2, base_thickness/2 + wall_height/2))
)

# Right wall with two holes
wall2 = (
    cq.Workplane("XY")
    .box(base_length, wall_thickness, wall_height)
    .faces("<Y")
    .workplane()
    .pushPoints([(-base_length/4, 0), (base_length/4, 0)])
    .hole(hole_diameter)
    .translate((0, -base_width/2 + wall_thickness/2, base_thickness/2 + wall_height/2))
)

result = base.union(wall1).union(wall2)