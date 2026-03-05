import cadquery as cq

# Parametric dimensions
length = 150.0  # Total length of the box
width = 40.0    # Total width of the box
height = 30.0   # Total height of the box
wall_thickness = 2.0  # Thickness of the walls and bottom
notch_width = 10.0    # Width of the rectangular notch
notch_depth = 3.0     # Depth of the rectangular notch

# 1. Create the main solid block
# We start with a solid box centered on the XY plane, sitting on Z=0
box = cq.Workplane("XY").box(length, width, height)

# 2. Hollow out the box to create the container
# Using the shell operation on the top face (+Z)
# A negative thickness hollows inwards
container = box.faces(">Z").shell(-wall_thickness)

# 3. Create the notch
# The notch is located on one of the short ends (let's say -X face based on the view)
# It's centered on the width of that face and cuts down from the top edge.

# We locate the workplane on the top face
# Then we draw a rectangle centered on the short edge
notch = (
    cq.Workplane("XY")
    .workplane(offset=height/2)  # Move to the top of the box
    .center(-length/2, 0)        # Move center to the -X edge
    .rect(wall_thickness * 3, notch_width) # Make the cutting rect wider than the wall to ensure a clean cut
    .extrude(-notch_depth)       # Cut downwards
)

# 4. Combine the container and the cut
result = container.cut(notch)
