import cadquery as cq

# -- Parametric Dimensions --
length = 100.0       # Total length of the top plate
width = 40.0         # Width of the plate
thickness = 10.0     # Thickness of the curved top plate section

# Mounting holes
hole_spacing_x = 60.0  # Distance between hole centers lengthwise
hole_spacing_y = 25.0  # Distance between hole centers widthwise
counterbore_dia = 10.0 # Diameter of the counterbore
counterbore_depth = 4.0 # Depth of the counterbore
hole_dia = 5.5         # Diameter of the through hole

# Bottom protrusion (Key/Tab)
key_width = 12.0       # Width of the rectangular protrusion on the bottom
key_height = 10.0      # Height/Depth of the protrusion from the bottom of the plate
key_length = length    # Length of the protrusion (appears to run full length)

# -- Modeling --

# Step 1: Create the main body
# We start with a rectangle and extrude it.
# The ends are fully rounded. The easiest way is to extrude a rectangle 
# and then fillet the short edges with a radius equal to half the width.
# Alternatively, sketch the profile with arcs. Let's use the fillet method for simplicity.

main_body = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z") # Select vertical edges
    .fillet(width / 2.0 - 0.01) # Fillet radius approx half width (minus tiny epsilon to avoid kernel errors with touching geometry)
)

# Step 2: Create the bottom key/protrusion
# We need to add material to the bottom (-Z) face.
# It looks like a rectangular block running along the center.

# Finding the bottom face
bottom_face = main_body.faces("<Z")

result_with_key = (
    bottom_face
    .workplane()
    .center(0, 0)
    .rect(key_length, key_width)
    .extrude(key_height)
)

# Step 3: Create the counterbored holes
# There are 4 holes arranged in a rectangle pattern on the top face.

# Finding the top face
top_face = result_with_key.faces(">Z")

result = (
    top_face
    .workplane()
    .rect(hole_spacing_x, hole_spacing_y, forConstruction=True) # Construction rectangle for positioning
    .vertices() # Select corners of the construction rectangle
    .cboreHole(hole_dia, counterbore_dia, counterbore_depth) # Create counterbored holes
)

# Export or display (standard boilerplate for CadQuery scripts)
# show_object(result) is implicit in some environments, but 'result' variable is required.