import cadquery as cq

# Define parametric dimensions
cylinder_radius = 20.0
cylinder_height = 80.0
cut_angle = 45.0  # Angle of the cut in degrees
cut_height_offset = 30.0 # Height where the cut starts on the lower side

# Create the base cylinder
base_cylinder = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)

# Define the cutting plane
# We need a plane that is angled.
# We can create a large box or a plane and use it to cut the cylinder.
# A simple way is to define a cutting tool (a large box) oriented at the correct angle.

# Calculate the position and orientation for the cut
# We will create a box that will represent the volume to remove.
# The box needs to be rotated and positioned so it slices off the top part.

# Alternative approach: Use a plane to split the object, but CadQuery's split operation can be complex.
# Easier approach: Construct a cutting solid.

# Let's define a cutting box.
# Dimensions need to be large enough to cover the cylinder.
box_size = cylinder_radius * 4

# Create a cutting tool (a box)
# We position it such that its bottom face acts as the cutting plane.
cutting_tool = (
    cq.Workplane("XY")
    .box(box_size, box_size, box_size)
    .rotate((0, 0, 0), (0, 1, 0), cut_angle) # Rotate around Y axis
    .translate((0, 0, cylinder_height)) # Move it up
)

# This approach with a box is tricky to get the exact offset right parametrically without trigonometry.
# Let's try a different approach:
# 1. Create the cylinder.
# 2. Create a face or a block that represents the "void" space above the angled plane.
# 3. Cut the cylinder with that block.

# A more robust parametric way using a custom workplane for the cut:
result = (
    cq.Workplane("XY")
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)

# Define the cutting shape
# We want to keep the bottom part.
# Let's visualize the cut: a plane rotated around the Y-axis.
# It passes through a point. Let's say the lowest point of the cut is at Z = `cut_height_offset`.
# The highest point will be determined by the angle.

# We can create a wedge shape to subtract.
wedge = (
    cq.Workplane("XY")
    .workplane(offset=cut_height_offset) # Start at the lower lip of the cut
    .transformed(rotate=(0, -cut_angle, 0)) # Rotate the workplane
    .rect(cylinder_radius * 4, cylinder_radius * 4) # Make a big rectangle
    .extrude(cylinder_height * 2) # Extrude upwards (relative to the rotated plane)
)

# Perform the cut
result = result.cut(wedge)

# If the result is meant to be a hollow pipe instead of a solid cylinder:
# We would shell it or perform two cylinder extrusions and subtract.
# Looking at the shading, the top face looks solid grey like the sides, implying a solid object.
# However, "pipes" cut like this are common. I will assume solid based on the prompt "solid geometry" unless indicated otherwise,
# but usually, these diagrams represent solid rods.
# Let's stick to the solid rod interpretation.

# To ensure the cut orientation matches the image (high point at the back/left, low point at the front/right):
# The image shows the highest point roughly at the "back-left" and lowest at "front-right".
# The previous code rotated around Y.
# Let's adjust the rotation to match the visual orientation.
# If we rotate around the Y axis, the slope changes along X.
# Let's refine the parameters to match the visual aspect ratio.

result = (
    cq.Workplane("XY")
    .circle(25)  # Radius
    .extrude(100) # Height
)

# Create a cutting volume
# We want a plane defined by a point and a normal, or a rotation.
# Let's create a huge block that is rotated and subtract it.
cutting_plane = (
    cq.Workplane("XY")
    .workplane(offset=40)  # Height of the lowest part of the cut
    .transformed(rotate=(0, -45, 0)) # Rotate 45 degrees around Y
    .rect(200, 200)       # Large enough to cover the cylinder
    .extrude(200)         # Extrude 'up' relative to the new plane to create the volume to remove
)

result = result.cut(cutting_plane)