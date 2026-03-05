import cadquery as cq

# Parametric dimensions for the model
base_width = 100.0      # Width of the rectangular base plate
base_height = 50.0      # Height of the rectangular base plate
base_thickness = 15.0   # Thickness of the base plate
nozzle_length = 100.0   # Length of the tapered transition
tip_diameter = 30.0     # Diameter of the circular tip

# Create the 3D model
# 1. Start with the base plate oriented in the YZ plane (extruding along X)
result = cq.Workplane("YZ").box(base_width, base_height, base_thickness)

# 2. Create the transition from the rectangular face to the circular tip
result = (
    result
    .faces(">X")                # Select the front face of the base plate
    .workplane()                # Create a working plane on that face
    .rect(base_width, base_height) # Draw the starting rectangular profile (matches base)
    .workplane(offset=nozzle_length) # Create an offset plane for the tip
    .circle(tip_diameter / 2.0)      # Draw the ending circular profile
    .loft(combine=True)         # Loft between profiles and unite with the base
)