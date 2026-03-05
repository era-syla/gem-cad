import cadquery as cq

# Parametric dimensions
length = 100.0       # Overall length (X-axis)
width = 80.0         # Overall width (Y-axis)
height = 40.0        # Overall height (Z-axis)

# V-notch parameters
notch_depth = 50.0   # How deep the V-notch goes into the block (Y-axis)
notch_width = 80.0   # How wide the notch is at the opening (X-axis)

# Hole parameters for the left face (X-min face)
large_hole_diam = 10.0
small_hole_diam = 6.0
large_hole_spacing = 15.0 # Vertical spacing between large holes
small_hole_spacing = 15.0 # Vertical spacing between small holes
hole_set_spacing_x = 15.0 # Horizontal spacing between small and large hole sets

# Hole parameters for the side faces of the V-legs
side_hole_diam = 6.0

# Create the base block
# Centered on XY to make symmetry easier, Z-up
base = cq.Workplane("XY").box(length, width, height)

# Create the V-shaped cutout
# We will create a triangular prism and subtract it
# The notch is centered on the front face (Y-min)
p1 = (0, -width/2 + notch_depth)  # Tip of the V inside the block
p2 = (-notch_width/2, -width/2)   # Left edge of opening
p3 = (notch_width/2, -width/2)    # Right edge of opening

# Sketch the triangle for the cut
notch_sketch = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3, p1])
    .close()
    .extrude(height)
)

# Apply the cut
block_with_notch = base.cut(notch_sketch)

# Add holes to the left face (X-min face)
# We select the face with X < 0
left_face = block_with_notch.faces("<X").workplane()

# Large holes (closer to the center of the block thickness usually, or aligned)
# Based on image, small holes are "behind" large holes relative to the front
# Let's position them parametrically relative to the face center
# Face local coordinates: X is likely along global Y, Y is along global Z
result_with_left_holes = (
    left_face
    # Large holes
    .pushPoints([(hole_set_spacing_x/2, large_hole_spacing/2), 
                 (hole_set_spacing_x/2, -large_hole_spacing/2)])
    .hole(large_hole_diam)
    # Small holes
    .pushPoints([(-hole_set_spacing_x/2, small_hole_spacing/2), 
                 (-hole_set_spacing_x/2, -small_hole_spacing/2)])
    .hole(small_hole_diam)
)

# Add holes to the side faces of the "legs" created by the V-notch
# There is a hole visible on the right leg's outer face (X-max) and likely one on the inner face of the left leg (visible in image)
# Actually, looking closer at the image, there is a hole on the small rectangular face at the tip of the "legs" formed by the V.
# Let's target the faces that are the "ends" of the U/V shape.
# These faces are at Y-min, but split by the notch.

# Let's select the front-most faces (Y-min)
# There are two such faces after the cut.
front_faces = result_with_left_holes.faces("<Y")

# We want to put a hole in the center of each of these small faces going inward
result = (
    front_faces.workplane()
    .hole(side_hole_diam, depth=20) # Drilled into the leg
)

# If the holes in the image are actually on the angled faces or side faces:
# The image shows a hole on the flat narrow face at the front right.
# And another hole on the flat narrow face at the front left.
# The previous step accomplishes this.

# Final Export
# result is already defined above