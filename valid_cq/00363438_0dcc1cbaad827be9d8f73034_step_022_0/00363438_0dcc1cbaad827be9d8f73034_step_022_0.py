import cadquery as cq

# Parameters for the joining plate
width = 40.0
height = 60.0
thickness = 5.0
hole_diameter = 5.5  # Clearance for M5 screws
grid_spacing = 20.0
margin = 10.0

# Calculate cut coordinates (45-degree chamfer on top-left)
cut_start_x = width - grid_spacing  # X=20
cut_end_y = height - grid_spacing   # Y=40

# Define the vertices of the plate profile 
# Coordinates are based on a 40x60mm bounding box with origin at Bottom-Left
points = [
    (0, 0),                 # Bottom-Left
    (width, 0),             # Bottom-Right
    (width, height),        # Top-Right
    (cut_start_x, height),  # Top edge, start of cut
    (0, cut_end_y)          # Left edge, end of cut
]

# Define hole locations
# Standard 20mm grid spacing with 10mm margin
hole_locations = [
    (margin, margin),                   # Bottom-Left (10, 10)
    (width - margin, margin),           # Bottom-Right (30, 10)
    (margin, margin + grid_spacing),    # Middle-Left (10, 30)
    (width - margin, margin + grid_spacing), # Middle-Right (30, 30)
    (width - margin, height - margin)   # Top-Right (30, 50)
]

# Generate the 3D model
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