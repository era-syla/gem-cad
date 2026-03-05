import cadquery as cq

# --- Parameters ---
height = 60.0             # Total height of the object
diameter = 30.0           # Outer diameter of the cylindrical sections
radius = diameter / 2.0

# Waist / Groove parameters
neck_diameter = 22.0      # Diameter at the narrowest part of the waist
neck_radius = neck_diameter / 2.0
waist_cut_radius = 12.0   # Radius of the circular profile cutting the waist

# Socket parameters
socket_width = 12.0       # Side length of the square drive socket
socket_depth = 15.0       # Depth of the socket

# Edge treatments
chamfer_top = 3.0         # Chamfer size for the top edge
chamfer_bottom = 1.5      # Chamfer size for the bottom edge

# --- Modeling ---

# 1. Create the base cylinder
result = cq.Workplane("XY").circle(radius).extrude(height)

# 2. Create the waist groove
# We create a toroidal cutting tool by revolving a circle on the XZ plane.
# The circle is positioned so its inner edge touches the defined neck radius.
cut_center_x = neck_radius + waist_cut_radius
cut_center_z = height / 2.0

waist_tool = (
    cq.Workplane("XZ")
    .moveTo(cut_center_x, cut_center_z)
    .circle(waist_cut_radius)
    .revolve(360)  # Revolves around the Z-axis (local Y of XZ plane)
)

# Subtract the waist tool from the main body
result = result.cut(waist_tool)

# 3. Apply Chamfers to top and bottom edges
# We select the top face, get its outer edge, and chamfer
result = result.faces(">Z").edges().chamfer(chamfer_top)
# We select the bottom face, get its outer edge, and chamfer
result = result.faces("<Z").edges().chamfer(chamfer_bottom)

# 4. Cut the Square Socket
# Select the top face, create a workplane, sketch a square, and cut blind
result = (
    result.faces(">Z")
    .workplane()
    .rect(socket_width, socket_width)
    .cutBlind(-socket_depth)
)