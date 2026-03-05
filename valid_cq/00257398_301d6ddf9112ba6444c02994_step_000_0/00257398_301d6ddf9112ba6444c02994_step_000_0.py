import cadquery as cq

# -- Parametric Dimensions --
plate_length = 160.0
plate_width = 70.0
plate_thickness = 8.0

# Central feature dimensions
rim_outer_size = 45.0
rim_height = 8.0
rim_wall_thickness = 4.0
rim_inner_size = rim_outer_size - (2 * rim_wall_thickness)

# Hole dimensions
hole_inset = 8.0  # Distance from edge to hole center
hole_diameter = 5.0
csk_diameter = 10.0
csk_angle = 90.0

# -- 3D Modeling --

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Add countersunk holes at the corners
# We define a construction rectangle to locate the hole centers
h_dist_x = plate_length - (2 * hole_inset)
h_dist_y = plate_width - (2 * hole_inset)

result = (
    result.faces(">Z")
    .workplane()
    .rect(h_dist_x, h_dist_y, forConstruction=True)
    .vertices()
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)

# 3. Create the raised square rim
# We extrude a profile defined by an outer and inner rectangle
result = (
    result.faces(">Z")
    .workplane()
    .rect(rim_outer_size, rim_outer_size)
    .rect(rim_inner_size, rim_inner_size)
    .extrude(rim_height)
)

# 4. Cut the center hole through the base plate
# We select the top of the newly created rim and cut all the way down
result = (
    result.faces(">Z")
    .workplane()
    .rect(rim_inner_size, rim_inner_size)
    .cutThruAll()
)