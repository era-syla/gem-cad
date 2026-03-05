import cadquery as cq

# Parametric dimensions estimated from the image
length = 150.0      # Total length of the extrusion
height = 30.0       # Total height of the profile
width = 20.0        # Width of the top horizontal face
lip_height = 10.0   # Height of the vertical front face

# Create the 3D model
# We define the cross-section profile on the YZ plane and extrude it along the X axis.
# The profile consists of a vertical back, horizontal top, vertical front lip, and a slanted bottom face.
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                       # Bottom-Back corner (Origin)
        (0, height),                  # Top-Back corner
        (width, height),              # Top-Front corner
        (width, height - lip_height)  # Bottom of the front vertical lip
    ])
    .close()                          # closes the shape back to (0,0), creating the diagonal face
    .extrude(length)
)