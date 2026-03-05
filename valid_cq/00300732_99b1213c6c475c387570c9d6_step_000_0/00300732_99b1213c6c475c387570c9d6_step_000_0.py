import cadquery as cq

# Parameters for the geometry
length = 100.0
height = 40.0
width = 20.0
text_string = "Battery"
font_size = 12.0
cut_depth = 1.0

# Create the base rectangular block
# box(length, width, height) creates a box centered at the origin
# Dimensions: X=length, Y=width, Z=height
result = cq.Workplane("XY").box(length, width, height)

# Create the text on the front face
# 1. Select the face in the positive Y direction (Front face)
# 2. Create a workplane. Default orientation: Local X = Global X, Local Y = Global Z (Up)
# 3. Rotate workplane 180 degrees around Local X. 
#    - New Local Y becomes Global -Z (Down).
#    - New Local Z becomes Global -Y (Pointing into the block).
#    This flips the text upside-down relative to the Z-axis, matching the image,
#    and orients the extrusion direction into the part for cutting.
result = (result
          .faces(">Y")
          .workplane()
          .transformed(rotate=(180, 0, 0))
          .text(text_string, font_size, cut_depth, cut=True))