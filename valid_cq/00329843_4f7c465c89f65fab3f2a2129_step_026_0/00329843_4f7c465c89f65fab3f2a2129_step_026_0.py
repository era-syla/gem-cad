import cadquery as cq

# Parameters
center_length = 40.0
center_width = 14.0
center_height = 14.0

end_length = 25.0
end_width = 9.0
end_height = 9.0

# Create the main central body (Box centered at origin)
result = cq.Workplane("XY").box(center_length, center_width, center_height)

# Add the right extension
# Select the face at positive X, draw the smaller profile, and extrude
result = (
    result.faces(">X")
    .workplane()
    .rect(end_width, end_height)
    .extrude(end_length)
)

# Add the left extension
# Select the face at negative X, draw the smaller profile, and extrude
result = (
    result.faces("<X")
    .workplane()
    .rect(end_width, end_height)
    .extrude(end_length)
)