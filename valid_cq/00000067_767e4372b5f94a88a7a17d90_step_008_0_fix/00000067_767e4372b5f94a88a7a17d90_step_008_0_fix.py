import cadquery as cq

# Parameters
base_length = 50
base_width = 20
base_thickness = 3

bracket_depth = 20
bracket_wall_thickness = 3
bracket_wall_height = 10

ramp_radius = 30
ramp_length = 15
ramp_width = base_width

# Base plate
base = cq.Workplane("XY").rect(base_length, base_width).extrude(base_thickness)

# U-shaped bracket walls
opening_start = base_length/2 - bracket_depth
left_wall_x = opening_start + bracket_wall_thickness/2
right_wall_x = base_length/2 - bracket_wall_thickness/2

walls = (
    base.faces(">Z")
        .workplane()
        .pushPoints([(left_wall_x, 0), (right_wall_x, 0)])
        .rect(bracket_wall_thickness, base_width)
        .extrude(bracket_wall_height)
)

# Ramp section: half-cylinder intersected with a box
# Create the bounding box for the ramp piece
ramp_box = (
    cq.Workplane("XY")
      .box(ramp_length, ramp_width, ramp_radius)
      .translate((
          -base_length/2 + ramp_length/2,
          0,
          ramp_radius/2
      ))
)

# Create a full cylinder (axis along Y) to carve the curved ramp
cylinder = (
    cq.Workplane("XZ")
      .center(-base_length/2 + ramp_radius, 0)
      .circle(ramp_radius)
      .extrude(ramp_width, both=True)
)

ramp_vol = cylinder.intersect(ramp_box)

# Combine all parts
result = base.union(walls).union(ramp_vol)