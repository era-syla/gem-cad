import cadquery as cq

# Define parametric dimensions
# Estimated dimensions based on the visual proportions in the image
length = 100.0       # Outer length of the frame
width = 60.0         # Outer width of the frame
thickness = 15.0     # Vertical thickness (height) of the frame
wall_thickness = 15.0 # Thickness of the walls around the hole

# Create the base rectangular block
# We center it to make subsequent operations easier
outer_box = cq.Workplane("XY").box(length, width, thickness)

# Create the inner rectangular cutout
# The inner dimensions are derived from the outer dimensions and wall thickness
inner_length = length - (2 * wall_thickness)
inner_width = width - (2 * wall_thickness)

# Perform the cut operation
result = outer_box.faces(">Z").workplane().rect(inner_length, inner_width).cutThruAll()

# Alternative method using sketches for a cleaner 2D-to-3D approach
# result = (
#     cq.Workplane("XY")
#     .sketch()
#     .rect(length, width)
#     .rect(inner_length, inner_width, mode='s')
#     .finalize()
#     .extrude(thickness)
# )