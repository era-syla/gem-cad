import cadquery as cq

# Parametric dimensions
plate_width = 300.0   # Width of the rectangular plate
plate_height = 200.0  # Height of the rectangular plate
thickness = 5.0       # Thickness of the plate

# Large hole parameters
large_hole_diameter = 30.0
large_hole_spacing = 150.0  # Distance between centers of large holes
large_hole_offset_y = 0.0   # Vertical offset from center (0 means centered vertically)

# Small corner hole parameters
corner_hole_diameter = 4.0
corner_margin = 10.0  # Distance from the edge to the center of corner holes

# Create the base plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, thickness)
)

# Create the large central holes
# The holes are spaced apart symmetrically from the center
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-large_hole_spacing / 2, large_hole_offset_y), 
        (large_hole_spacing / 2, large_hole_offset_y)
    ])
    .hole(large_hole_diameter)
)

# Create the small corner mounting holes
# Calculate positions based on width, height, and margin
x_pos = (plate_width / 2) - corner_margin
y_pos = (plate_height / 2) - corner_margin

corner_points = [
    (-x_pos, -y_pos),
    (x_pos, -y_pos),
    (x_pos, y_pos),
    (-x_pos, y_pos)
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(corner_points)
    .hole(corner_hole_diameter)
)