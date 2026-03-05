import cadquery as cq

# Parameters
length = 200.0
width = 6.0
height = 6.0
pitch = 2.5
hole_dia = 1.2
row_spacing = 2.5
hole_depth = 1.5

# Define the triangular cross-section
pts = [
    (-width/2, height/2),
    (width/2, height/2),
    (0, -height/2)
]

# Create the base triangular prism
base_rail = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length/2, both=True)
)

# Calculate number of holes to fit along the length
num_holes = int((length - pitch) / pitch)

# Add two rows of holes on the top face
result = (
    base_rail.faces(">Y")
    .workplane()
    .rarray(pitch, row_spacing, num_holes, 2)
    .circle(hole_dia/2)
    .cutBlind(-hole_depth)
)