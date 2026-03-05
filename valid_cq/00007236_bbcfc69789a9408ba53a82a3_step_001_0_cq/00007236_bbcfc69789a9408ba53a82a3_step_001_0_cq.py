import cadquery as cq

# Parameters for the plate
plate_width = 100.0   # Width of the plate (X direction)
plate_height = 100.0  # Height of the plate (Y direction)
thickness = 2.0       # Thickness of the plate (Z direction)

# Parameters for corner mounting holes
corner_hole_diameter = 4.0
corner_hole_inset = 6.0  # Distance from the edge to the hole center

# Parameters for center holes
center_hole_diameter = 2.0
center_hole_spacing = 20.0 # Vertical distance between the two center holes

# Calculate positions for corner holes
# Coordinates are (x, y) relative to center (0,0)
x_inset = plate_width / 2 - corner_hole_inset
y_inset = plate_height / 2 - corner_hole_inset

corner_pts = [
    (-x_inset, -y_inset),
    (x_inset, -y_inset),
    (x_inset, y_inset),
    (-x_inset, y_inset)
]

# Calculate positions for center holes
# Vertically aligned on X=0
center_pts = [
    (0, -center_hole_spacing / 2),
    (0, center_hole_spacing / 2)
]

# Create the base plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, thickness)
    .faces(">Z")
    .workplane()
    # Add corner holes
    .pushPoints(corner_pts)
    .hole(corner_hole_diameter)
    # Add center holes
    .pushPoints(center_pts)
    .hole(center_hole_diameter)
)