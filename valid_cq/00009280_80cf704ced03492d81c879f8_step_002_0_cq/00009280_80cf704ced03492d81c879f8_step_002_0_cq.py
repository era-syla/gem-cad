import cadquery as cq

# -- Parameters --
# These dimensions are estimated based on the visual proportions in the image
length = 40.0   # Dimension along the X axis (width of the shorter side)
width = 80.0    # Dimension along the Y axis (width of the longer side)
height = 150.0  # Dimension along the Z axis (tall vertical side)
wall_thickness = 5.0 # Thickness of the walls

# -- Modeling --

# 1. Create the base solid rectangular block
box = cq.Workplane("XY").box(length, width, height)

# 2. Hollow out the box to create the container shape
# We select the top face (Z direction) and shell the solid inwards.
# A negative thickness in shell() removes material from the inside.
# If we wanted it open at the bottom too, we would select both top and bottom faces.
# Here, it looks like a container closed at the bottom.
result = box.faces(">Z").shell(-wall_thickness)

# If the intention was a tube (open top and bottom), the code would be:
# result = box.faces(">Z or <Z").shell(-wall_thickness)
# Given the typical "container" look, the single open face is the standard interpretation.

# -- Final Result --
# The variable 'result' now contains the 3D geometry