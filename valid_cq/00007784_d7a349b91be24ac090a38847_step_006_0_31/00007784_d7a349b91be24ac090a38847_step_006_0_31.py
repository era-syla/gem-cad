import cadquery as cq

# Parametric dimensions
length = 150.0
width = 35.0
thickness = 3.0
rim_width = 2.5
pocket_depth = 1.5
corner_radius = 4.0
chamfer_size = 1.0

# Text parameters
text_str = "KIsureous pa"
font_size = 14.0
text_height = pocket_depth  # Text flush with the top rim

# Calculated parameters
inner_radius = max(0.1, corner_radius - rim_width)
pocket_floor_z = thickness - pocket_depth

# Create the base profile with rounded corners
sk_base = cq.Sketch().rect(length, width).vertices().fillet(corner_radius)

# Extrude the main base plate
base = cq.Workplane("XY").placeSketch(sk_base).extrude(thickness)

# Add a chamfer to the outer top edge
base = base.edges(">Z").chamfer(chamfer_size)

# Create the inner pocket profile
sk_pocket = cq.Sketch().rect(length - 2 * rim_width, width - 2 * rim_width).vertices().fillet(inner_radius)

# Cut the inner pocket
base = base.faces(">Z").workplane().placeSketch(sk_pocket).cutBlind(-pocket_depth)

# Generate the 3D text
text_wp = cq.Workplane("XY").workplane(offset=pocket_floor_z)
text_3d = text_wp.text(text_str, font_size, text_height, font="Times New Roman", kind="bold")

# Add the small alignment pin in the bottom left corner
pin_radius = 1.2
pin_x = -(length / 2) + rim_width + 4.5
pin_y = -(width / 2) + rim_width + 4.5
pin = (
    cq.Workplane("XY")
    .workplane(offset=pocket_floor_z)
    .center(pin_x, pin_y)
    .circle(pin_radius)
    .extrude(text_height)
)

# Combine all features into the final result
result = base.union(text_3d).union(pin)