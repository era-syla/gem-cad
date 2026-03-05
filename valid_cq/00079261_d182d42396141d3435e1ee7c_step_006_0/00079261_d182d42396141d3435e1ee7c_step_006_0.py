import cadquery as cq

# Geometric parameters
side_length = 20.0     # Width/Depth of the square profile
height = 150.0         # Height of the bar
hole_diameter = 4.0    # Diameter of the top center hole
hole_depth = 15.0      # Depth of the blind hole

# Create the 3D model
# 1. Start with a box (rectangular prism) centered at the origin
# 2. Select the top face (positive Z direction)
# 3. Create a workplane on that face and cut a hole
result = (
    cq.Workplane("XY")
    .box(side_length, side_length, height)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter, hole_depth)
)