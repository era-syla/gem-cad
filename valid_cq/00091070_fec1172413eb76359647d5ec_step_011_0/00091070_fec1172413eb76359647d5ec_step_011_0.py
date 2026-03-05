import cadquery as cq

# -- Parametric Dimensions --
length = 180.0       # Total length of the plate
width = 35.0         # Width (height) of the plate
thickness = 3.0      # Plate thickness
hole_diameter = 4.0  # Diameter of corner holes
hole_margin = 5.0    # Distance from hole center to edges
text_content = "Havana FP Body"
font_size = 9.0
text_depth = 0.5     # Depth of engraving

# -- Modeling --

# 1. Base Plate
# Create the main rectangular body centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Corner Holes
# Calculate x and y offsets for the holes based on margin
x_offset = length / 2 - hole_margin
y_offset = width / 2 - hole_margin

# Select the top face and cut the four holes
result = (result.faces(">Z")
          .workplane()
          .pushPoints([
              (x_offset, y_offset),
              (x_offset, -y_offset),
              (-x_offset, y_offset),
              (-x_offset, -y_offset)
          ])
          .hole(hole_diameter))

# 3. Text Engraving (Left Side)
# Position the workplane on the top face, move center to the left half
result = (result.faces(">Z")
          .workplane()
          .center(-length / 4, 0)
          .text(text_content, font_size, -text_depth))

# 4. Text Engraving (Right Side - Inverted)
# Position on the right half and rotate 180 degrees to match the image
result = (result.faces(">Z")
          .workplane()
          .center(length / 4, 0)
          .transformed(rotate=(0, 0, 180))
          .text(text_content, font_size, -text_depth))