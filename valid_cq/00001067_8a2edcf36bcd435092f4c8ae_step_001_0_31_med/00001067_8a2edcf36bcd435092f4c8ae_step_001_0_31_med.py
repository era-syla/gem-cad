import cadquery as cq

# Parametric dimensions
thickness = 2.0
plate_w = 100.0
plate_h = 45.0
cutout_w = 40.0
arm_ext_x = 25.0
arm_ext_y = 15.0
arm_tip_h = 5.0
arm_length = 35.0

# Define the outer profile points of the base geometry
profile_pts = [
    (plate_w / 2, plate_h),                                       # Top right
    (-plate_w / 2, plate_h),                                      # Top left
    (-plate_w / 2, 0),                                            # Mid left inner corner
    (-plate_w / 2 - arm_ext_x, -arm_ext_y),                       # Outer left top
    (-plate_w / 2 - arm_ext_x, -arm_ext_y - arm_tip_h),           # Outer left bottom
    (-cutout_w / 2, -arm_length),                                 # Inner left tip
    (-cutout_w / 2, 0),                                           # Cutout inner left corner
    (cutout_w / 2, 0),                                            # Cutout inner right corner
    (cutout_w / 2, -arm_length),                                  # Inner right tip
    (plate_w / 2 + arm_ext_x, -arm_ext_y - arm_tip_h),            # Outer right bottom
    (plate_w / 2 + arm_ext_x, -arm_ext_y),                        # Outer right top
    (plate_w / 2, 0)                                              # Mid right inner corner
]

# Create the main extruded body
result = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(thickness)
)

# Define and cut the large central holes
large_hole_radius = 4.0
large_hole_centers = [
    (-12.0, 15.0),
    (12.0, 15.0)
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(large_hole_centers)
    .circle(large_hole_radius)
    .cutThruAll()
)

# Define and cut the small mounting holes
small_hole_radius = 1.5
small_hole_centers = [
    (-40.0, 10.0), (40.0, 10.0),    # Outer side holes
    (-15.0, 30.0), (15.0, 30.0),    # Top inner holes
    (-15.0, 5.0),  (15.0, 5.0)      # Bottom inner holes near cutout
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(small_hole_centers)
    .circle(small_hole_radius)
    .cutThruAll()
)