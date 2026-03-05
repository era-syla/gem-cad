import cadquery as cq

# Parameters for the geometry
cube_size = 20.0        # Size of the central cube
hole_diameter = 10.0    # Diameter of the central through-hole
pin_diameter = 4.0      # Diameter of the side pins
pin_length = 10.0       # Length of the pins extending from the cube faces

# 1. Create the main cube
# We center it at the origin for easier referencing
main_body = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

# 2. Create the central hole
# The hole appears to go through the front face (YZ plane relative to default box orientation if viewed from an angle)
# Let's assume the hole goes through the Y-axis based on typical orientation, 
# or X-axis depending on view. Looking at the isometric view:
# - Pins are likely on one axis (say X)
# - Hole is on another axis (say Y)
# - Top/bottom is Z.

# Let's align:
# - Pins along the X-axis
# - Hole through the Y-axis (front-to-back)
# - Cube is centered.

main_body = main_body.faces(">Y").workplane().hole(hole_diameter)

# 3. Create the side pins (Axles)
# We need to add cylinders to the left and right faces (X-axis)

# Create the union of the main body and the pins.
# We can create a cylinder along the X axis that goes through the whole part and sticks out,
# or create two separate cylinders. A single long cylinder is often cleaner code.
total_pin_length = cube_size + (2 * pin_length)

# Create a cylinder along the X-axis
pin = cq.Workplane("YZ").circle(pin_diameter / 2).extrude(total_pin_length)
# The extrusion starts at X=0 on the YZ plane. We need to center it on the cube.
# Current center of pin is at X = total_pin_length / 2.
# We need to translate it so its center aligns with the cube center (0,0,0).
pin = pin.translate((-total_pin_length / 2, 0, 0))

# Combine the cube (with hole) and the pin
result = main_body.union(pin)

# Export or visualization step is implicit in the 'result' variable requirement