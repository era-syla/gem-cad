import cadquery as cq

# Long rectangular bar with a small hole near one end
bar_length = 200
bar_width = 15
bar_height = 15

# Create the main bar
result = (
    cq.Workplane("XY")
    .box(bar_length, bar_width, bar_height)
)

# Add a small hole near one end (on the face)
hole_offset = bar_length / 2 - 12
hole_diameter = 4

result = (
    result
    .faces(">Z")
    .workplane()
    .center(-hole_offset, 0)
    .hole(hole_diameter, bar_height)
)