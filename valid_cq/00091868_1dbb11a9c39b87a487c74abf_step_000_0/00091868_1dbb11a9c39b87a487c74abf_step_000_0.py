import cadquery as cq

# Parametric dimensions based on visual estimation
plate_length = 100.0
plate_width = 50.0
plate_thickness = 10.0
hole_diameter = 6.0
hole_spacing = 50.0  # Distance between the two holes

# Create the model
result = (
    cq.Workplane("XY")
    # Create the main rectangular base plate
    .box(plate_length, plate_width, plate_thickness)
    # Select the top face to place the holes
    .faces(">Z")
    .workplane()
    # Define the center points for the two holes
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    # Cut the holes through the entire part
    .hole(hole_diameter)
)