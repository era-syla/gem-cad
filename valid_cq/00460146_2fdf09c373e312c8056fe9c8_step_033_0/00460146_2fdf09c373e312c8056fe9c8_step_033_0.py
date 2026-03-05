import cadquery as cq

# Parametric dimensions
thickness = 4.0      # Thickness of the plate
hole_diameter = 5.5  # Diameter of mounting holes (M5 clearance)

# Coordinates for the outer profile
# Shape: L-bracket style with a diagonal gusset and a stepped notch at the corner
# Bounding box is approx 60x60mm
points = [
    (0, 0),       # Bottom-left corner
    (40, 0),      # Bottom edge end (before notch)
    (40, 20),     # Notch inner vertical
    (60, 20),     # Notch inner horizontal
    (60, 60),     # Top-right corner
    (40, 60),     # Top edge end (start of diagonal)
    (0, 20)       # Left edge end (end of diagonal)
]

# Hole locations
# Standard 20mm spacing for 2020 extrusion plates
hole_locations = [
    (10, 10),  # Bottom-left
    (30, 10),  # Bottom-right of the horizontal leg
    (50, 30),  # Bottom of the vertical leg
    (50, 50)   # Top-right
]

# Create the model
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)