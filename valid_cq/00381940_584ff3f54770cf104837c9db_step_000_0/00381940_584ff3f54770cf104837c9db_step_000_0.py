import cadquery as cq

# Geometric parameters
length = 150.0
width = 25.0
height_front = 15.0
height_back = 55.0

# Define control points for the wavy top surface spline
# The profile draws from the back (right) to the front (left)
# Starting from the top-back corner, going to the top-front corner
wave_profile_points = [
    (135, 68),  # Highest peak near back
    (110, 42),  # Valley
    (85, 55),   # Middle peak
    (60, 28),   # Valley
    (35, 38),   # Front peak
    (0, height_front) # End at front face top
]

# Create the main body
# 1. Sketch on XZ plane
# 2. Draw bottom line and vertical ends
# 3. Connect top with spline
# 4. Extrude along Y
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(length, 0)          # Bottom edge
    .lineTo(length, height_back) # Back vertical edge
    .spline(wave_profile_points, includeCurrent=True) # Top wavy edge
    .close()
    .extrude(width)
)

# Add the two mounting holes on the side face
# Coordinates (x, z) are relative to the global origin projected onto the face
hole_locations = [
    (20, 10),   # Front hole
    (135, 22)   # Back hole
]

result = (
    result.faces(">Y")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints(hole_locations)
    .hole(4.0)
)