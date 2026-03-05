import cadquery as cq

# Define parametric dimensions
width = 40.0      # Width of the rectangular plate
height = 80.0     # Height of the rectangular plate
thickness = 5.0   # Thickness of the plate
hole_diameter = 10.0 # Diameter of the hole
hole_offset_top = 15.0 # Distance from the top edge to the hole center

# Create the main rectangular body
# Using centered=False on Z to place the base on the XY plane, 
# and centered=True on X and Y to make positioning easier relative to origin.
# However, for a simple tag like this, centering on X/Y is often standard.
# Let's align it so it stands upright as shown in the image.
# The image shows it standing on the X-Z or Y-Z plane typically, but standard CAD starts on XY.
# Let's build it flat on XY and then standard viewing orientation handles the rest,
# or simply build a box.

# Step 1: Create the base plate centered on the origin
result = cq.Workplane("XY").box(width, height, thickness)

# Step 2: Create the hole
# The hole is located near the "top". If the box is height=80 centered, 
# the top edge is at y = height/2 = 40.
# The hole center y-coordinate = (height/2) - hole_offset_top.
hole_y_pos = (height / 2.0) - hole_offset_top

result = result.faces(">Z").workplane().pushPoints([(0, hole_y_pos)]).hole(hole_diameter)

# Alternatively, if the user wanted the exact orientation shown (standing up):
# result = cq.Workplane("XZ").box(width, height, thickness)
# ... but usually standard view is isometric, so flat on XY is fine. 
# Let's stick to the simplest XY construction which results in the shown geometry 
# when viewed isometrically.

# To strictly match the vertical orientation in the image viewer if it were a default "Front" view:
# We can construct it on the front plane.
# Let's try to match the visual orientation: It looks like a wall standing up.
result = cq.Workplane("XY").box(width, thickness, height) # Width=x, Thickness=y, Height=z

# Now the top face is >Z. The top edge is at z = height/2.
# The hole is on the broad face. The broad face is the Front face (XZ plane essentially).
# Let's select the front face (min Y or max Y depending on the box param).
# Let's select the face with normal +Y.
result = result.faces(">Y").workplane().pushPoints([(0, (height / 2.0) - hole_offset_top)]).hole(hole_diameter)

# This creates a standing plate with a hole near the top, matching the visual representation better.