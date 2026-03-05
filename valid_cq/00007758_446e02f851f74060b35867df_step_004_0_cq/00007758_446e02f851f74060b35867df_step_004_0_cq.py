import cadquery as cq

# -- Parametric Dimensions --
length = 100.0  # Total length of the plate
height = 40.0   # Total height of the plate
thickness = 5.0 # Thickness of the plate

hole_diameter = 5.0    # Diameter of the mounting holes
hole_inset_x = 10.0    # Distance from side edge to hole center
hole_inset_y = 10.0    # Distance from top/bottom edge to hole center

# -- Model Creation --

# Create the base rectangular plate
plate = cq.Workplane("XY").box(length, height, thickness)

# Define hole positions relative to the center
# We need 4 holes. The box is centered at (0,0,0) by default.
# Coordinates will be calculated based on insets.
x_pos = length / 2 - hole_inset_x
y_pos = height / 2 - hole_inset_y

hole_locations = [
    (-x_pos, y_pos),  # Top-Left
    (-x_pos, -y_pos), # Bottom-Left
    (x_pos, y_pos),   # Top-Right
    (x_pos, -y_pos)   # Bottom-Right
]

# Cut the holes through the plate
result = (plate
          .faces(">Z")
          .workplane()
          .pushPoints(hole_locations)
          .hole(hole_diameter)
          )

# The 'result' variable now contains the final geometry