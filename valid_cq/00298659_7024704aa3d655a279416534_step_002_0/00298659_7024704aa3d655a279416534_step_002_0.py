import cadquery as cq

# Parametric dimensions for the model
plate_length = 30.0  # Dimension along X axis
plate_width = 20.0   # Dimension along Y axis
plate_thickness = 1.0
gap = 15.0           # Distance between the two plates

# Calculate the offset for placement along the Y axis
# The plates are aligned along the Y axis to match the isometric view direction
# Center-to-center distance = width of one plate + gap
center_offset = (plate_width + gap) / 2.0

# Generate the CAD model
result = (
    cq.Workplane("XY")
    # Define the center points for the two plates
    .pushPoints([(0, -center_offset), (0, center_offset)])
    # Create the rectangular profiles
    .rect(plate_length, plate_width)
    # Extrude to create solids
    .extrude(plate_thickness)
)