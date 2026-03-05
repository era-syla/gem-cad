import cadquery as cq

# Parametric dimensions
length = 60.0       # Total length of the box
width = 60.0        # Total width of the box
height = 30.0       # Total height of the box
wall_thickness = 4.0 # Thickness of the outer frame
cutout_radius = 15.0 # Radius for the side cutouts
bottom_cutout_radius = 8.0 # Radius for the small cutouts at the bottom corners

# 1. Create the base block
# We start with a solid box centered on X and Y, sitting on Z=0
base = cq.Workplane("XY").box(length, width, height)

# 2. Hollow out the inside vertically to make a frame
# This creates the main square hole through the top
box_shell = base.faces(">Z").workplane().rect(length - 2*wall_thickness, width - 2*wall_thickness).cutThruAll()

# 3. Create the arched cutouts on the sides (X faces)
# We will sketch on the XZ plane
# The cutouts look like large semicircles or ovals removing material from the sides
x_cutout = (
    cq.Workplane("YZ")
    .workplane(offset=length/2.0) # Move to the +X face
    .center(0, -height/2.0)       # Center coordinate system at bottom edge
    .moveTo(0, height/2.0)        # Move up a bit
    .circle(cutout_radius)        # Create the circle profile
    .extrude(-length)             # Cut through the entire width (negative X direction)
)

# 4. Create the arched cutouts on the front/back (Y faces)
# Similar to step 3 but rotated
y_cutout = (
    cq.Workplane("XZ")
    .workplane(offset=width/2.0)  # Move to the +Y face
    .center(0, -height/2.0)       # Center at bottom edge
    .moveTo(0, height/2.0)
    .circle(cutout_radius)
    .extrude(-width)              # Cut through the entire length (negative Y direction)
)

# 5. Create corner relief cutouts at the bottom
# Looking at the image, the corners where the "legs" touch the ground have semi-circular bites taken out.
# We can do this by placing cylinders at the corners and cutting.
corner_cutouts = (
    cq.Workplane("XY")
    .rect(length, width, forConstruction=True) # Reference rectangle for corner vertices
    .vertices()
    .circle(bottom_cutout_radius)
    .extrude(height/2.0) # Cut halfway up
)

# 6. Apply the cuts
result = (
    box_shell
    .cut(x_cutout)
    .cut(y_cutout)
    .cut(corner_cutouts)
)

# 7. Add fillets to smooth internal edges (optional but looks like the render)
# The render shows smooth transitions where the cutouts intersect.
# Selecting the edges created by the intersection of the main vertical hole and the side cutouts.
try:
    # Attempt to fillet the vertical internal edges formed by the side cutouts
    # This selection logic targets vertical edges near the center
    result = result.edges("|Z").fillet(2.0)
except:
    # Fallback if specific edge selection fails, just return un-filleted result
    pass

# Export or display
if "show_object" in locals():
    show_object(result)