import cadquery as cq

# Geometric parameters based on the visual proportions of the image
length = 120.0       # Total length of the part
height = 60.0        # Total height of the part
thickness = 15.0     # Total thickness (width) of the part
notch_height = 8.0   # Height of the cutout/rabbet at the bottom
notch_depth = 5.0    # Depth of the cutout/rabbet from the front face

# Create the model by sketching the side profile on the YZ plane and extruding along X.
# The profile represents a rectangle with a notch removed from the bottom-front corner.
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                                      # Bottom-back corner
        (0, height),                                 # Top-back corner
        (thickness, height),                         # Top-front corner
        (thickness, notch_height),                   # Start of the notch on front face
        (thickness - notch_depth, notch_height),     # Inner top corner of the notch
        (thickness - notch_depth, 0),                # Inner bottom corner of the notch
        (0, 0)                                       # Close the profile back to start
    ])
    .close()
    .extrude(length)
)