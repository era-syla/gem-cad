import cadquery as cq

# Define parametric dimensions
length = 100.0   # Total length of the block
width = 40.0     # Width (depth) of the block
height_short = 20.0 # Height of the shorter vertical edge
height_tall = 50.0  # Height of the taller vertical edge
top_flat_length = 50.0 # Length of the top horizontal flat section

# The geometry can be defined as a 2D sketch extruded into 3D.
# We will draw the side profile on the XY plane and extrude it along Z.

# Calculate the coordinates for the side profile polygon
# Points are defined counter-clockwise starting from origin (0,0)
# Let's assume the bottom-left corner is at (0,0)
p1 = (0, 0)
p2 = (length, 0)
p3 = (length, height_tall)
p4 = (length - top_flat_length, height_tall)
p5 = (0, height_short)

# Create the 3D model
result = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3, p4, p5])
    .close()
    .extrude(width)
)

# Optional: If you want to center it or align it differently, you can adjust the workplane or points.
# The current code creates the object with the profile on the XY plane and thickness along Z.
# Based on the isometric view in the image, usually Z is up. Let's adjust to match standard orientation.
# Let's draw on XZ plane (front view) and extrude along Y (depth).

result = (
    cq.Workplane("XZ")
    .polyline([p1, p2, p3, p4, p5])
    .close()
    .extrude(width)
)