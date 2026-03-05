import cadquery as cq

# --- Parameters ---
length = 600.0          # Total length of the tube (Z axis)
width = 60.0            # Width of the face with holes (X axis)
depth = 30.0            # Depth of the tube (Y axis)
wall_thickness = 4.0    # Thickness of the tube walls
hole_diameter = 8.0     # Diameter of the holes
hole_count = 14         # Number of holes along the length
margin = 30.0           # Distance from the ends to the center of the first/last hole

# --- Modeling ---

# 1. Create the base hollow rectangular tube
# We draw the outer rectangle and the inner rectangle to define the wall, then extrude.
result = (
    cq.Workplane("XY")
    .rect(width, depth)
    .rect(width - 2 * wall_thickness, depth - 2 * wall_thickness)
    .extrude(length)
)

# 2. Calculate hole positions
# The points are defined relative to the center of the selected face.
# Local X is horizontal on the face, Local Y is vertical along the tube length.
hole_points = []
if hole_count > 0:
    # Calculate the span between the first and last hole
    span = length - 2 * margin
    # Calculate the step distance between holes
    step = span / (hole_count - 1) if hole_count > 1 else 0
    # Start position (bottom-most hole relative to face center)
    start_y = -span / 2
    
    for i in range(hole_count):
        # (x, y) coordinates: x=0 centers horizontally, y distributes vertically
        hole_points.append((0, start_y + i * step))

# 3. Cut the holes into the front face
# We select the face with normal in the +Y direction (corresponding to the 'width' dimension)
result = (
    result
    .faces(">Y")            # Select the front face
    .workplane()            # Create a working plane on this face
    .pushPoints(hole_points)# Set the centers for the holes
    .circle(hole_diameter / 2) # Sketch the hole circles
    .cutBlind(-wall_thickness * 2.0) # Cut inwards through the wall (negative depth)
)