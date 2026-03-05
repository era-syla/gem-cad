import cadquery as cq

# Parametric dimensions for the L-shaped plate
height = 120.0          # Total height of the vertical section
leg_width = 40.0        # Width of the vertical section
arm_extension = 45.0    # Length the top arm extends to the right
arm_thickness = 15.0    # Vertical thickness of the top arm
plate_thickness = 2.0   # Thickness of the extrusion

# Define the vertices of the profile in counter-clockwise order
# Sketching on the XZ plane so the model stands upright
points = [
    (0, 0),                                              # Bottom-left
    (leg_width, 0),                                      # Bottom-right of leg
    (leg_width, height - arm_thickness),                 # Inner corner under arm
    (leg_width + arm_extension, height - arm_thickness), # Bottom-right of arm tip
    (leg_width + arm_extension, height),                 # Top-right corner
    (0, height)                                          # Top-left corner
]

# Create the solid geometry
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(plate_thickness)
)