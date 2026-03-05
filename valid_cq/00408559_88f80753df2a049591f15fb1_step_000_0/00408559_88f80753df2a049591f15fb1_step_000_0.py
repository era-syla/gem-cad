import cadquery as cq

# --- Parameters ---
length = 130.0        # Total length of the part
height = 36.0         # Total height of the part
depth = 12.0          # Extrusion depth
thickness = 1.8       # Wall thickness
text_string = "SOLUS" # Text to cut
font_size = 20.0      # Font size for the text
hole_diam = 3.2       # Diameter of mounting holes

# --- Modeling ---

# 1. Base Geometry: Stadium shape (Rectangle with full fillets)
# We define the rectangle width such that adding the fillets results in 'length'
rect_width = length - height 
base = (
    cq.Workplane("XY")
    .rect(rect_width, height)
    .extrude(depth)
)

# Apply fillets to vertical edges to create the round ends
# Radius is slightly less than half height to ensure robust kernel operation
base = base.edges("|Z").fillet(height / 2.0 - 0.01)

# 2. Create Shell
# Remove the back face (<Z) and shell inwards to create the hollow bezel
# Negative thickness implies offset inwards
shell = base.faces("<Z").shell(-thickness)

# 3. Text Cutout
# Select the front face (>Z)
front_face = shell.faces(">Z").workplane()
# Cut the text through the face
with_text = front_face.text(text_string, font_size, -thickness * 2, cut=True)

# 4. Stencil Bridge for 'O'
# The letter 'O' has an inner island that needs support.
# We create a small vertical rib to connect it to the main body.
# Estimating position: 'L' is at x=0, 'O' is to the left.
# Approx offset for 'O' center with this font size is around -17mm.
bridge_x = -17.0
bridge_width = 1.5
bridge = (
    cq.Workplane("XY")
    .rect(bridge_width, font_size * 0.75) # Vertical bar
    .extrude(thickness)
    .translate((bridge_x, 0, depth - thickness))
)

# Fuse the bridge with the main body
result = with_text.union(bridge)

# 5. Mounting Holes
# Add holes to the top and bottom flat faces of the rim
# Top hole
result = (
    result.faces(">Y").workplane()
    .center(0, 0)
    .hole(hole_diam, depth=thickness * 3) # Depth ensures it pierces the rim
)

# Bottom hole
result = (
    result.faces("<Y").workplane()
    .center(0, 0)
    .hole(hole_diam, depth=thickness * 3)
)

# The final variable containing the geometry
if 'show_object' in globals():
    show_object(result)