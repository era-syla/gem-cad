import cadquery as cq

# Parametric dimensions
# Main L-bracket dimensions
back_plate_width = 40.0
back_plate_height = 100.0
back_plate_thickness = 10.0

# The top flange (overhang)
top_flange_depth = 20.0  # How far it sticks out
top_flange_thickness = 10.0

# The angled brace
brace_width = 20.0  # Width of the angled part
brace_thickness = 10.0 # Thickness of the main diagonal rib
brace_start_height_ratio = 0.8 # Where the brace starts relative to top
brace_end_offset = 20.0 # How far out the brace goes at the bottom

# Small bottom catch/hook dimensions
hook_depth = 10.0
hook_height = 15.0
hook_thickness = 10.0

# Hole dimensions
hole_diameter = 6.0
hole_spacing_y = 50.0  # Vertical distance between holes

# Create the Back Plate
# We start with the vertical plate
back_plate = (
    cq.Workplane("XY")
    .box(back_plate_width, back_plate_thickness, back_plate_height)
    .translate((0, 0, 0)) # Centered at origin for now
)

# Create the Top Flange
# It sits on top of the back plate and extends forward (assuming -Y is forward/back)
top_flange = (
    cq.Workplane("XY")
    .box(back_plate_width, top_flange_depth, top_flange_thickness)
    .translate((0, -(top_flange_depth/2 - back_plate_thickness/2), back_plate_height/2 - top_flange_thickness/2))
)

# Combine base shape
base_structure = back_plate.union(top_flange)

# Create the Angled Brace with the Cutout
# This is the complex central part. It's easier to sketch it from the side (YZ plane).
# The origin (0,0,0) is center of back plate.

# Calculate key points for the side profile sketch
# Y is thickness direction (depth), Z is height.
# Back face is at Y = +back_plate_thickness/2
# Front face of back plate is at Y = -back_plate_thickness/2

# Points relative to the YZ plane center of the back plate
p_top_corner_y = -back_plate_thickness/2
p_top_corner_z = back_plate_height/2 - top_flange_thickness

p_bottom_corner_y = -back_plate_thickness/2 - brace_end_offset
p_bottom_corner_z = -back_plate_height/2 

# Let's sketch the side profile of the brace
brace_profile = (
    cq.Workplane("YZ")
    .workplane(offset=-brace_width/2) # Move to the side of the brace
    .moveTo(p_top_corner_y, p_top_corner_z)
    .lineTo(p_top_corner_y, p_top_corner_z - 20) # Go down a bit straight
    .lineTo(p_bottom_corner_y, p_bottom_corner_z) # Angled line to bottom
    .lineTo(p_bottom_corner_y + 10, p_bottom_corner_z) # Bottom thickness
    .lineTo(p_top_corner_y + top_flange_depth - back_plate_thickness, p_top_corner_z) # Back to top, slightly inset
    .close()
    .extrude(brace_width) # Extrude along X
)

# Re-doing the brace logic to match the image more precisely using points
# The image shows a specific shape: a main diagonal rib and a small "hook" at the bottom.
# It looks like one continuous piece or a union of pieces.
# Let's construct the main triangular rib first.

rib_pts = [
    (0, back_plate_height/2 - top_flange_thickness),  # Top inner corner (relative to front face)
    (0, back_plate_height/2 - top_flange_thickness - 15), # Drop down slightly vertical
    (-50, -back_plate_height/2), # Bottom tip far out
    (-50 + 10, -back_plate_height/2), # Bottom tip thickness
    (0, 0), # Middle of plate roughly
    (0, back_plate_height/2 - top_flange_thickness) # Close loop
]

# Let's try a more specific geometric construction based on visual inspection
# We will draw on the YZ plane (Side view)
# Center of backplate is (0,0). Front face is Y = -5. Back face is Y = 5.

pts = [
    (-back_plate_thickness/2, back_plate_height/2 - top_flange_thickness), # A: Top join
    (-back_plate_thickness/2 - 5, back_plate_height/2 - top_flange_thickness - 10), # B: Slight chamfer/slope down
    (-back_plate_thickness/2 - 40, -back_plate_height/2), # C: Bottom most point
    (-back_plate_thickness/2 - 30, -back_plate_height/2), # D: Thickness at bottom
    (-back_plate_thickness/2, 10), # E: Return to plate
    (-back_plate_thickness/2, back_plate_height/2 - top_flange_thickness) # Close
]

main_rib = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(brace_width)
    .translate((-brace_width/2, 0, 0)) # Center the rib
)

# Now the small hook/catch at the bottom.
# It looks like a small triangle or trapezoid sticking out from the main diagonal.
# Looking closely, it creates a notch.

hook_pts = [
    (-back_plate_thickness/2 - 25, -back_plate_height/2 + 25), # Start on the diagonal
    (-back_plate_thickness/2 - 25, -back_plate_height/2 + 5),  # Go down vertically
    (-back_plate_thickness/2 - 15, -back_plate_height/2 + 5),  # Go in
    (-back_plate_thickness/2 - 15, -back_plate_height/2 + 25), # Go up
]
# This is tricky to get exact without dimensions, but let's model the "notch" by subtraction or adding a shape.
# Actually, looking at the image, there is a secondary support structure.
# Let's refine the shape to be a single sketch extruded, it's cleaner.

# Final Profile Strategy:
# 1. Back vertical line
# 2. Top horizontal (under flange)
# 3. Small vertical drop
# 4. Long diagonal to bottom left
# 5. Bottom horizontal return
# 6. Diagonal up (inner face of rib)
# 7. Vertical down (notch)
# 8. Horizontal in (notch)
# 9. Vertical up (back of hook) -> connects to plate

# Let's define the points for the side profile on YZ plane
# Origin (0,0) is center of back plate volume.
# X is lateral, Y is depth, Z is vertical.
# Front face of back plate is at Y = -5.

front_face_y = -back_plate_thickness/2
top_z = back_plate_height/2
bottom_z = -back_plate_height/2
rib_width = 12.0

# Refined Points for the side profile
p1 = (front_face_y, top_z - top_flange_thickness) # Start under flange
p2 = (front_face_y - 8, top_z - top_flange_thickness - 15) # Angle out slightly
p3 = (front_face_y - 45, bottom_z) # Main diagonal point
p4 = (front_face_y - 33, bottom_z) # Bottom thickness return
p5 = (front_face_y - 18, bottom_z + 25) # Up the diagonal inside
p6 = (front_face_y - 18, bottom_z + 10) # Drop down for hook
p7 = (front_face_y - 8, bottom_z + 10) # Back of hook
p8 = (front_face_y - 8, bottom_z + 35) # Up along hook/plate interface
p9 = (front_face_y, bottom_z + 45) # Back to plate

complex_rib = (
    cq.Workplane("YZ")
    .polyline([p1, p2, p3, p4, p5, p6, p7, p8, p9])
    .close()
    .extrude(rib_width)
    .translate((-rib_width/2, 0, 0))
)


# Combine parts
result = base_structure.union(complex_rib)

# Add Holes
# Upper Hole
result = result.faces(">Y").workplane().center(0, 20).hole(hole_diameter)
# Lower Hole
result = result.faces(">Y").workplane().center(0, -30).hole(hole_diameter)

# Final cleanup: The top flange in the image has a lip going down.
# Let's add that detail.
lip_height = 8.0
lip_thickness = 5.0

top_lip = (
    cq.Workplane("XY")
    .box(back_plate_width, lip_thickness, lip_height)
    .translate((0, -back_plate_thickness/2 - top_flange_depth + lip_thickness/2, back_plate_height/2 - top_flange_thickness - lip_height/2 + 0.01)) # 0.01 overlap
)

# Actually, the image shows the top flange is an inverted L itself.
# Let's adjust the top_flange construction to match image better (L-shape at top)
# My previous top_flange was just a flat plate.
# The image shows: Vertical Back Plate + Horizontal Top Plate + Vertical Down Lip at front of top plate.

# Re-unite with the lip
result = result.union(top_lip)

# Apply fillets to the main rib edges for a smoother look like the render (optional but good)
# result = result.edges("|X").fillet(0.5) # Small edge break

# Final result variable
result = result