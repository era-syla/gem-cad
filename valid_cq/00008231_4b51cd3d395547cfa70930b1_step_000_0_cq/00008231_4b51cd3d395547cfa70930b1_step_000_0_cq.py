import cadquery as cq

# Parametric dimensions
width = 50.0       # Width of the block (x-direction)
length = 40.0      # Length/Depth of the block (y-direction)
height = 50.0      # Total height of the block
hole_diameter = 30.0 # Diameter of the central hole

# Calculate the radius of the bottom arc
# Assuming the bottom is fully rounded (semicircle) to match the width
radius = width / 2.0

# Calculate the height of the rectangular part
rect_height = height - radius

# Create the sketch and extrude
# We'll draw on the front plane (XZ) and extrude along Y
result = (
    cq.Workplane("XZ")
    .moveTo(-width/2, 0)
    .lineTo(-width/2, rect_height)
    .lineTo(width/2, rect_height)
    .lineTo(width/2, 0)
    .threePointArc((0, -radius), (-width/2, 0)) # Create the rounded bottom
    .close()
    .extrude(length)
)

# Cut the hole through the center of the rounded section
# The center of the arc was at (0, 0) in the sketch plane (XZ), 
# but since the arc dips down to -radius, the "center" of the circular part is at (0,0) in our sketch.
result = (
    result
    .faces(">Y")  # Select the front face
    .workplane()
    .circle(hole_diameter / 2)
    .cutThruAll()
)