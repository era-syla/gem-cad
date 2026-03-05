import cadquery as cq

# Parameters for the model
cube_size = 50.0  # Length of the cube's side
hole_diameter = 25.0  # Diameter of the through-holes

# Create the base cube
base = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

# Create the holes
# We need to cut cylinders through each of the three axes (X, Y, Z)
# The cylinders should go all the way through the cube

# 1. Hole along the Z-axis (Top to Bottom)
z_hole = cq.Workplane("XY").circle(hole_diameter / 2).extrude(cube_size, both=True)

# 2. Hole along the Y-axis (Front to Back)
# We orient the workplane on XZ to extrude along Y
y_hole = cq.Workplane("XZ").circle(hole_diameter / 2).extrude(cube_size, both=True)

# 3. Hole along the X-axis (Left to Right)
# We orient the workplane on YZ to extrude along X
x_hole = cq.Workplane("YZ").circle(hole_diameter / 2).extrude(cube_size, both=True)

# Cut the holes from the base cube
result = base.cut(z_hole).cut(y_hole).cut(x_hole)

# Alternative, more compact approach using faces selector:
# result = (cq.Workplane("XY")
#           .box(cube_size, cube_size, cube_size)
#           .faces(">Z").workplane().hole(hole_diameter)
#           .faces(">X").workplane().hole(hole_diameter)
#           .faces(">Y").workplane().hole(hole_diameter))

# Export or visualization step is typically handled by the environment, 
# but 'result' is the required variable name.