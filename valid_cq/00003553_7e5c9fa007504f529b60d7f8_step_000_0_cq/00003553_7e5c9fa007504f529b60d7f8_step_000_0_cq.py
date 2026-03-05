import cadquery as cq

# --- Parametric Dimensions ---
base_length = 60.0    # Length of the base at the bottom (front to back)
base_width = 70.0     # Width of the object (left to right)
height_back = 80.0    # Height of the rear wall
height_front = 50.0   # Height of the front wall (at the top edge before the cut)
wall_thickness = 3.0  # Thickness of the walls
bottom_thickness = 4.0 # Thickness of the floor
cutout_radius = 45.0  # Radius of the semi-circular cutout on the front face
cutout_depth = 20.0   # How deep the semi-circle dips from the top edge

# --- Helper Geometry construction ---

# 1. Create the Main Block
# We will create a loft or a simple extrusion with a cut to get the wedge shape.
# Let's use an extrusion and then cut the slope.

# Create the base block
main_block = cq.Workplane("XY").box(base_width, base_length, height_back, centered=(True, True, False))

# Create the cutting wedge to define the slope
# The slope goes from height_back at y = +base_length/2 to height_front at y = -base_length/2
# Slope calculation:
# Top face points: (x, y, z)
# We want to slice off the top front.
# Let's create a cutting tool from the side (YZ plane).

slope_cut_tool = (
    cq.Workplane("YZ")
    .moveTo(base_length/2, height_back) # Top back corner
    .lineTo(-base_length/2, height_front) # Top front corner
    .lineTo(-base_length/2, height_back + 10) # Go up
    .lineTo(base_length/2, height_back + 10) # Go back
    .close()
    .extrude(base_width + 10, both=True) # Extrude wide enough to cut everything
)

wedge_shape = main_block.cut(slope_cut_tool)

# 2. Hollow out the inside (Shelling)
# We select the top face (which is now slanted) and shell inwards.
# However, shelling a slanted face can sometimes be tricky with exact dimensions.
# A robust method is to create the inner void by making a smaller copy and subtracting it.

# Dimensions for the inner pocket
inner_width = base_width - (2 * wall_thickness)
inner_length = base_length - (2 * wall_thickness)

# Instead of complex math for the inner wedge, let's use the Shell operation on the top face.
# We need to find the top face. It's the one with the normal roughly pointing up.
# The side walls are vertical, bottom is horizontal.
shelled_body = wedge_shape.faces("+Z").shell(-wall_thickness)

# 3. Create the Front Circular Cutout
# We need to cut a circular profile from the front face.
# The front face is angled. But the cutout looks like a projection from the Y-axis (front view).
# Let's cut a cylinder through the front face.

# Position for the cylinder center. It needs to be centered in X, and positioned in Z such that 
# the arc cuts appropriately.
# The lowest point of the cut is at (height_front - cutout_depth).
# If the radius is 'cutout_radius', the center Z is (height_front - cutout_depth + cutout_radius).

center_z = height_front - cutout_depth + cutout_radius
cylinder_cut = (
    cq.Workplane("XZ")
    .workplane(offset=-base_length/2 - 10) # Position in front of the object
    .moveTo(0, center_z)
    .circle(cutout_radius)
    .extrude(base_length + 20) # Extrude through the object
)

# We only want to cut the front wall, not the back wall.
# But looking at the image, the cut seems to only affect the front and maybe slightly the sides,
# but definitely creates that "scoop".
# Actually, looking closer at the image, the scoop is on the front face.
# Let's apply this cut.
scooped_body = shelled_body.cut(cylinder_cut)

# 4. Add the "JM" Text
# The text is on the front face. The front face is slightly slanted if we followed the pure wedge logic,
# but in the image, the front face looks vertical, and the *top* is slanted.
# Let's re-examine the image.
# It looks like: Vertical Front, Vertical Back, Vertical Sides.
# The Top is slanted from Back (High) to Front (Low).
# My previous logic created a slanted top, but vertical walls. That is correct.
# So the front face is vertical.

text_face = scooped_body.faces("<Y").workplane()

# Add "J"
text_j = (
    text_face
    .center(-12, height_front/2 - 10) # Adjust position
    .text("J", fontsize=30, distance=-1.0, font="Arial", kind='regular', cut=True)
)

# Add "M"
# We need to combine operations or do them sequentially on the resulting object
# CadQuery text operations usually return the modified object if cut=True

# Let's reconstruct the text part properly on the object
result = (
    scooped_body
    .faces("<Y").workplane()
    .center(-13, height_front/2 - 15) # approximate position for J
    .text("J", fontsize=28, distance=-1.5, font="Arial", halign="center", valign="center")
)

result = (
    result
    .faces("<Y").workplane()
    .center(13, height_front/2 - 15) # approximate position for M
    .text("M", fontsize=28, distance=-1.5, font="Arial", halign="center", valign="center")
)

# 5. Adding the foot/base extension
# The image shows a small lip or extension at the bottom rear.
# Let's look closer. Actually, it looks like the base is wider at the bottom?
# Or maybe it's just a chamfer/fillet?
# Looking at the bottom left corner of the image, there is a triangular protrusion.
# It looks like a stability foot extending backwards.

foot_length = 15.0
foot_height = 8.0

foot = (
    cq.Workplane("YZ")
    .moveTo(base_length/2, 0) # Bottom back corner
    .lineTo(base_length/2 + foot_length, 0) # Extend back
    .lineTo(base_length/2, foot_height) # Slope up to back wall
    .close()
    .extrude(base_width, both=True) # Extrude across the width
)

result = result.union(foot)

# 6. Final Fillets
# The edges look relatively sharp, but maybe small fillets on the text or top edges.
# The image shows a very clean "CAD" look.
# The scoop edge on the front is sharp.
# Let's leave it sharp as per the typical style of such CAD renders unless specified.

# Re-orient for display similar to image (Isometric-ish)
# No code needed for orientation, the viewer handles that.