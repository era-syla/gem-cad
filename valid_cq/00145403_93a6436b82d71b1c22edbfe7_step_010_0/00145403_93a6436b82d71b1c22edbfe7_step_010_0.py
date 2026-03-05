import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 120.0       # Overall length of the plate
height = 30.0        # Overall height of the plate
thickness = 5.0      # Thickness of the plate
border_width = 5.0   # Width of the solid frame around the slot

# Create the 3D model
# We use the XZ plane to match the upright orientation shown in the isometric view
result = (
    cq.Workplane("XZ")
    # Draw the outer rectangle
    .rect(length, height)
    # Draw the inner rectangle (the slot)
    # By adding a second rectangle inside the first before extruding, 
    # CadQuery automatically interprets the space between them as the solid face.
    .rect(length - 2 * border_width, height - 2 * border_width)
    # Extrude the sketch to create the 3D solid
    .extrude(thickness)
)