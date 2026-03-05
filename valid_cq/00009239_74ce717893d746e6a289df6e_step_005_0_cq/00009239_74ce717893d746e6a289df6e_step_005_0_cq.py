import cadquery as cq

# Parameters for the chamfered square plate
width = 50.0       # Overall width of the plate (x-axis)
length = 50.0      # Overall length of the plate (y-axis)
thickness = 10.0   # Thickness of the plate (z-axis)
chamfer_size = 10.0 # The distance from the corner to the start of the chamfer

# Create the base geometry
# Method: Create a rectangle and then chamfer the corners (Z-axis vertices)
result = (
    cq.Workplane("XY")
    .box(width, length, thickness)
    .edges("|Z")  # Select vertical edges
    .chamfer(chamfer_size)
)

# Alternative method: Sketching a polygon directly
# This method gives more explicit control over the vertex positions if it wasn't a standard chamfer
# points = [
#     (width/2 - chamfer_size, length/2),
#     (width/2, length/2 - chamfer_size),
#     (width/2, -length/2 + chamfer_size),
#     (width/2 - chamfer_size, -length/2),
#     (-width/2 + chamfer_size, -length/2),
#     (-width/2, -length/2 + chamfer_size),
#     (-width/2, length/2 - chamfer_size),
#     (-width/2 + chamfer_size, length/2)
# ]
# result = cq.Workplane("XY").polyline(points).close().extrude(thickness)