import cadquery as cq

# Parameters for the cabinet door
width = 350.0         # Overall width of the door
height = 800.0        # Overall height of the door
thickness = 20.0      # Overall thickness
frame_width = 60.0    # Width of the border frame (stiles and rails)
recess_depth = 6.0    # Depth of the inner panel recess

# Create the base solid block
# .box() centers the object at the origin
door_base = cq.Workplane("XY").box(width, height, thickness)

# Create the shaker-style recess
# 1. Select the top face (+Z)
# 2. Create a new workplane on that face
# 3. Draw a rectangle for the inner panel area (subtracting frame width from both sides)
# 4. Perform a blind cut into the material to the specified depth
result = (
    door_base.faces(">Z")
    .workplane()
    .rect(width - 2 * frame_width, height - 2 * frame_width)
    .cutBlind(-recess_depth)
)