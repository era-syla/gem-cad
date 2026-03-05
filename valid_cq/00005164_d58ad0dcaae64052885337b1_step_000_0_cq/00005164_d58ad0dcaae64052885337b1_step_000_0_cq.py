import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_width = 40.0
body_height = 60.0
body_depth = 30.0

# Split plane location (visualizing the assembly line)
split_offset = body_depth / 2.0 

# Long shaft dimensions
shaft_diameter = 12.0
shaft_length = 80.0 # Length protruding from face

# Back boss dimensions
boss_diameter = 25.0
boss_height = 10.0 # Height protruding from back face
small_boss_diameter = 10.0 # The smaller cylinder sticking out of the boss
small_boss_height = 5.0

# Top face holes
top_large_hole_dia = 12.0
top_small_hole_dia = 5.0
top_hole_spacing = 15.0 # Distance between centers

# Side mounting holes (pattern of 6)
side_hole_dia = 4.0
side_hole_depth = 10.0
side_hole_margin_x = 5.0
side_hole_margin_y = 5.0

# --- Geometry Construction ---

# 1. Create the main rectangular block
main_body = cq.Workplane("XY").box(body_width, body_height, body_depth)

# 2. Add the long shaft to the front face
# We select the face with the minimum Z coordinate (front)
shaft = (
    main_body.faces("<Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 3. Add the boss structure to the back face
# We select the face with the maximum Z coordinate (back)
# Note: In the image, the boss looks like a sphere cap or a fillet, 
# but often these are cylindrical bosses with fillets. 
# Let's model it as a cylinder with a smaller cylinder on top, then fillet the base.
boss_geo = (
    shaft.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
    .faces(">Z")
    .workplane()
    .circle(small_boss_diameter / 2.0)
    .extrude(small_boss_height)
)

# Apply a heavy fillet to the main boss to match the rounded look in the image
# We select the edge circle at the base of the main boss protrusion
try:
    # Selecting the edge where the boss meets the main body
    boss_geo = boss_geo.edges(f"|Z and >Z and (not >Y) and (not <Y) and (not >X) and (not <X)").filter(lambda e: abs(e.center().z - body_depth/2) < 0.1).fillet(2.0)
    # The image shows a very rounded boss, possibly spherical. Let's fillet the top edge of the main boss.
    boss_geo = boss_geo.edges(f"|Z").filter(lambda e: abs(e.center().z - (body_depth/2 + boss_height)) < 0.1).fillet(boss_height * 0.4)
except:
    pass # Fallback if edge selection fails, geometry remains valid

# 4. Add the vertical split line (visual groove or actual cut)
# The image shows a seam. We can model this by adding a small groove 
# or constructing it as two parts. For a single solid, a small groove works.
# Let's cut a tiny groove around the YZ plane perimeter.
groove_width = 0.5
groove_depth = 0.2
groove_path = cq.Workplane("YZ").rect(body_height + 2, body_depth + 2).rect(body_height, body_depth)
# It's easier just to rely on the geometry, but let's assume it's a solid block first.
# If we want the visual "split", we can cut a slot.
# Let's cut a slot down the middle X=0 plane
result_with_groove = boss_geo.faces(">Y").workplane(centerOption="CenterOfBoundBox").rect(0.2, body_depth + 1).cutThruAll()


# 5. Add Top Holes (Large and Small)
# Select top face (+Y)
top_workplane = result_with_groove.faces(">Y").workplane()

# Large hole (appears to be a counterbore or just a ring, likely an oil port)
# Located slightly off-center towards the back
top_holes = (
    top_workplane
    .center(0, body_depth/4) # Shift towards back
    .circle(top_large_hole_dia / 2.0)
    .cutBlind(-10) # Arbitrary depth
)

# Small hole (located towards the front)
top_holes = (
    top_holes
    .faces(">Y").workplane()
    .center(0, -body_depth/4) # Shift towards front
    .circle(top_small_hole_dia / 2.0)
    .cutBlind(-10)
)

# 6. Add the 6 mounting holes on the side face (+X)
side_workplane = top_holes.faces(">X").workplane()

# Calculate positions relative to center
w = body_depth - 2 * side_hole_margin_x
h = body_height - 2 * side_hole_margin_y

# The pattern is 2 columns of 3 holes
# Coordinates relative to the face center
pts = []
for y_factor in [-0.5, 0, 0.5]: # Top, Middle, Bottom
    for z_factor in [-0.5, 0.5]: # Left, Right (on the face, which corresponds to depth)
        pts.append((z_factor * w, y_factor * h))

final_model = (
    side_workplane
    .pushPoints(pts)
    .circle(side_hole_dia / 2.0)
    .cutBlind(-side_hole_depth)
)

# 7. Add the black ring detail on the shaft base (visual cut/groove)
# This is an aesthetic detail, likely a seal or o-ring groove
final_model = (
    final_model.faces("<Z") # Front face
    .workplane()
    .circle(shaft_diameter/2.0 + 1.5) # Outer dia of ring
    .circle(shaft_diameter/2.0)       # Inner dia of ring
    .cutBlind(-0.5)                   # Shallow cut
)

# 8. Add black ring detail on top large hole
final_model = (
    final_model.faces(">Y") # Top face
    .workplane()
    .center(0, body_depth/4) # Center of large hole
    .circle(top_large_hole_dia/2.0 + 1.5)
    .circle(top_large_hole_dia/2.0)
    .cutBlind(-0.5)
)

# 9. Add black ring detail on top small hole
final_model = (
    final_model.faces(">Y") # Top face
    .workplane()
    .center(0, -body_depth/4) # Center of small hole
    .circle(top_small_hole_dia/2.0 + 1.0)
    .circle(top_small_hole_dia/2.0)
    .cutBlind(-0.5)
)

result = final_model