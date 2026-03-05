import cadquery as cq

# Parametric dimensions
width = 50.0       # Outer width of the box
height = 50.0      # Total height of the box
thickness = 3.0    # Wall thickness
fillet_radius = 5.0 # Radius of the vertical edges
cutout_width = 30.0 # Width of the bottom cutout (feet)
cutout_height = 3.0 # Height of the bottom cutout

# 1. Create the main base shape (square prism)
base = cq.Workplane("XY").box(width, width, height)

# 2. Fillet the vertical edges to get rounded corners
# Select edges parallel to Z axis
base = base.edges("|Z").fillet(fillet_radius)

# 3. Hollow out the box to create the shell
# We select the top face ("+Z") and shell inwards by negative thickness
result = base.faces("+Z").shell(-thickness)

# 4. Create the cutouts at the bottom to form the feet
# We need to cut a slot through the bottom of the walls on each side.
# An easy way is to sketch on the side faces or simply cut a cross shape at the bottom.

# Approach: Create a cross-shaped cutter at the bottom Z level
cutter_x = (
    cq.Workplane("XZ")
    .rect(width + 10, cutout_height) # Make it wider than the box
    .extrude(cutout_width) # Extrude to the cutout width
    .translate((0, 0, -height/2 + cutout_height/2)) # Position at bottom
)

cutter_y = (
    cq.Workplane("YZ")
    .rect(width + 10, cutout_height) # Make it wider than the box
    .extrude(cutout_width) # Extrude to the cutout width
    .translate((0, 0, -height/2 + cutout_height/2))
    # Note: Workplane "YZ" extrudes along X, so no rotation needed, 
    # but the logic above creates a block oriented along X.
    # Let's simplify: Just make two box cutters.
)

# Alternative Approach for Cutouts: simple boolean subtraction
# Create a cutter for the X-axis direction
cutter1 = cq.Workplane("XY").box(width * 2, cutout_width, cutout_height).translate((0, 0, -height/2 + cutout_height/2))
# Create a cutter for the Y-axis direction
cutter2 = cq.Workplane("XY").box(cutout_width, width * 2, cutout_height).translate((0, 0, -height/2 + cutout_height/2))

# Apply the cuts
result = result.cut(cutter1).cut(cutter2)

# Export or visualization would happen here (e.g., show_object(result))