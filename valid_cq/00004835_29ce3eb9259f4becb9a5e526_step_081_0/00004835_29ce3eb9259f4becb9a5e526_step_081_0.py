import cadquery as cq

# Parametric dimensions for the gear rack / notched bar
length = 300.0        # Total length of the bar (Z axis)
width = 8.0           # Width of the bar
thickness = 4.0       # Thickness of the bar
pitch = 8.0           # Distance between teeth/notches
notch_height = 4.0    # Height of each notch (gap between teeth)
notch_depth = 1.5     # Depth of the cut

# Calculate the number of notches that fit along the length
num_notches = int(length / pitch)

# Create the base rectangular bar centered at the origin
# Aligned along the Z-axis to match the vertical orientation in the image
base = cq.Workplane("XY").box(width, thickness, length)

# Create the notches on the front face
result = (
    base
    .faces(">Y")                        # Select the front face
    .workplane(centerOption="CenterOfMass")
    .rarray(
        xSpacing=1,                     # Spacing in X (irrelevant for 1 column)
        ySpacing=pitch,                 # Spacing in Y (along the length of the bar)
        xCount=1,                       # One column of notches
        yCount=num_notches,             # Number of notches
        center=True                     # Center the array pattern
    )
    .rect(width * 1.5, notch_height)    # Rectangle wider than the bar to ensure clean cut
    .cutBlind(-notch_depth)             # Cut into the material
)