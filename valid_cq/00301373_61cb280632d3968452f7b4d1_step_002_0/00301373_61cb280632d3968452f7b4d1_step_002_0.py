import cadquery as cq

# Parametric dimensions
base_width = 20.0
base_depth = 20.0
base_height = 40.0

top_width = 15.0
top_depth = 15.0
top_height = 45.0

pocket_border = 1.5
pocket_depth = 1.0

# Create the base block
# box is created centered at origin, translate moves it to sit on Z=0
base = cq.Workplane("XY").box(base_width, base_depth, base_height).translate((0, 0, base_height / 2))

# Create the top block
# Dimensions are smaller to create the stepped effect
top = cq.Workplane("XY").box(top_width, top_depth, top_height).translate((0, 0, base_height + top_height / 2))

# Union the two blocks to form the main structure
structure = base.union(top)

# Create the rectangular pocket on the side face of the base
# We select the face in the positive Y direction
result = (
    structure
    .faces(">Y")  # Select the face with the maximum Y value (side of the base)
    .workplane()
    .rect(base_width - 2 * pocket_border, base_height - 2 * pocket_border)
    .cutBlind(-pocket_depth)  # Cut into the material
)