import cadquery as cq

# Parameters
dish_radius = 40
dish_depth = 20
thickness = 3
feed_length = 60
feed_size = 6
plate_thickness = 3
plate_height = 50
plate_width = 15
brace_thickness = 3

# Dish (approximate thin-walled conical dish)
profile = [
    (0, 0),
    (dish_depth, dish_radius),
    (dish_depth, dish_radius - thickness),
    (thickness, 0)
]
dish = cq.Workplane("YZ").polyline(profile).close().revolve(360)

# Feed Arm (rectangular beam from the mouth of the dish)
feed = (
    cq.Workplane("YZ")
      .transformed(offset=(0, dish_depth - 1.5, 0))
      .rect(feed_size, feed_size)
      .extrude(feed_length)
)

# Side Plates (two vertical plates mounted behind the dish)
plate1 = (
    cq.Workplane("XZ")
      .transformed(offset=(feed_length, dish_depth + 5, 0))
      .rect(plate_width, plate_height)
      .extrude(plate_thickness)
)
plate2 = (
    cq.Workplane("XZ")
      .transformed(offset=(feed_length, dish_depth + 5 + plate_thickness + 5, 0))
      .rect(plate_width, plate_height)
      .extrude(plate_thickness)
)

# Braces between plates
brace1 = (
    cq.Workplane("XZ")
      .transformed(offset=(feed_length + plate_thickness, dish_depth + 5 + plate_thickness/2, 10))
      .rect(20, brace_thickness)
      .extrude(brace_thickness)
)
brace2 = (
    cq.Workplane("XZ")
      .transformed(offset=(feed_length + plate_thickness, dish_depth + 5 + plate_thickness/2, -10))
      .rect(20, brace_thickness)
      .extrude(brace_thickness)
)

# Combine all parts into the final result
result = dish.union(feed).union(plate1).union(plate2).union(brace1).union(brace2)