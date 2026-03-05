import cadquery as cq

# --- Parameters ---

# Main Dimensions
width = 250.0   # Total width (X)
depth = 250.0   # Total depth (Y)
height = 60.0   # Total height (Z)
thickness = 2.0 # Sheet metal thickness

# Cutout and Feature Parameters
corner_cutout_radius = 15.0  # Radius for the corner indentations
side_notch_width = 30.0      # Width of the rectangular notches on sides
side_notch_depth = 10.0      # Depth of the rectangular notches

# Vent Hole Parameters (Side Grid)
vent_hole_dia = 4.0
vent_rows = 5
vent_cols = 12
vent_spacing_x = 8.0
vent_spacing_y = 8.0

# Front Panel Cutouts
front_circle_dia = 35.0
front_rect_w = 40.0
front_rect_h = 25.0

# Screw Hole Parameters
screw_hole_dia = 3.5
lid_screw_inset = 6.0

# --- Helper Functions ---

def create_corner_cutouts(sketch, width, depth, radius):
    """Adds corner radius cutouts to a rectangular sketch"""
    return (sketch
            .rect(width, depth)
            .vertices()
            .fillet(radius)
           )

# --- 1. Main Chassis (Bottom and Sides) ---

# Constructing the U-shape base profile
# Strategy: Create a solid box, shell it or cut it out. Let's make a U-shape extrusion.

# Outer profile
chassis_base = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(height)
)

# Inner cutout to create walls
chassis_hollow = (
    cq.Workplane("XY")
    .rect(width - 2*thickness, depth - 2*thickness)
    .extrude(height)
)

# This creates a box with walls. But the image shows a specific "U" folded shape usually.
# Let's look closer. It looks like a bottom plate with two side walls folded up.
# The front and back seem open (front covered by faceplate).

chassis = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(thickness) # Bottom plate
    .faces(">Z").workplane()
    # Add Side Walls
    .rect(width, depth, forConstruction=True)
    .vertices()
    .rect(thickness, depth) # This creates 4 rectangles at corners, we need sides
)

# Alternative approach for Chassis: Make the U-profile and extrude along Y (depth)
# Profile on XZ plane
chassis_profile = (
    cq.Workplane("XZ")
    .moveTo(-width/2, height)
    .lineTo(-width/2, 0)
    .lineTo(width/2, 0)
    .lineTo(width/2, height)
    .lineTo(width/2 - thickness, height)
    .lineTo(width/2 - thickness, thickness)
    .lineTo(-width/2 + thickness, thickness)
    .lineTo(-width/2 + thickness, height)
    .close()
    .extrude(depth)
)
# Center the chassis
chassis = chassis_profile.translate((0, depth/2, 0))

# --- Chassis Features ---

# 1. Corner Cutouts (Circular indents at corners of the footprint)
# These cut through the bottom and affect the side walls slightly in the image
corner_locations = [
    (-width/2, -depth/2), (width/2, -depth/2),
    (width/2, depth/2), (-width/2, depth/2)
]

for loc in corner_locations:
    # Cylindrical cut at corners
    chassis = chassis.cut(
        cq.Workplane("XY").center(*loc).circle(corner_cutout_radius).extrude(height + 10)
    )

# 2. Side Rectangular Notches (Middle of sides)
# Left side notch
chassis = chassis.cut(
    cq.Workplane("XY")
    .center(-width/2, 0)
    .rect(side_notch_depth*2, side_notch_width)
    .extrude(height + 10)
)
# Right side notch
chassis = chassis.cut(
    cq.Workplane("XY")
    .center(width/2, 0)
    .rect(side_notch_depth*2, side_notch_width)
    .extrude(height + 10)
)

# 3. Vent Holes (Right Side)
vent_plane = chassis.faces(">X").workplane().center(0, -height/4) # Shift down a bit
vent_grid = (
    vent_plane
    .rarray(vent_spacing_x, vent_spacing_y, vent_cols, vent_rows)
    .circle(vent_hole_dia/2)
    .cutThruAll()
)
chassis = vent_grid

# 4. Mounting Holes on Top Edges of Side Walls
# Left Wall
chassis = (
    chassis.faces(">Z").workplane()
    .pushPoints([(-width/2 + thickness/2, 0), (width/2 - thickness/2, 0)]) # Mid-points
    .hole(screw_hole_dia)
    .pushPoints([
        (-width/2 + thickness/2, -depth/2 + corner_cutout_radius + 10),
        (-width/2 + thickness/2, depth/2 - corner_cutout_radius - 10),
        (width/2 - thickness/2, -depth/2 + corner_cutout_radius + 10),
        (width/2 - thickness/2, depth/2 - corner_cutout_radius - 10)
    ])
    .hole(screw_hole_dia)
)

# 5. Bottom holes (Grid pattern on floor)
chassis = (
    chassis.faces("<Z").workplane()
    .pushPoints([(0,0)]) # Center hole
    .rarray(30, 30, 4, 4) # Random grid approximation
    .hole(screw_hole_dia)
)

# --- 2. Top Lid ---

lid = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(thickness)
)

# Apply same corner cuts to lid
for loc in corner_locations:
    lid = lid.cut(
        cq.Workplane("XY").center(*loc).circle(corner_cutout_radius).extrude(thickness * 2)
    )

# Apply side notches to lid
lid = lid.cut(
    cq.Workplane("XY").center(-width/2, 0).rect(side_notch_depth*2, side_notch_width).extrude(thickness*2)
)
lid = lid.cut(
    cq.Workplane("XY").center(width/2, 0).rect(side_notch_depth*2, side_notch_width).extrude(thickness*2)
)

# Lid Holes (matching chassis wall holes)
lid = (
    lid.faces(">Z").workplane()
    .pushPoints([(-width/2 + thickness/2, 0), (width/2 - thickness/2, 0)])
    .hole(screw_hole_dia)
    .pushPoints([
        (-width/2 + thickness/2, -depth/2 + corner_cutout_radius + 10),
        (-width/2 + thickness/2, depth/2 - corner_cutout_radius - 10),
        (width/2 - thickness/2, -depth/2 + corner_cutout_radius + 10),
        (width/2 - thickness/2, depth/2 - corner_cutout_radius - 10)
    ])
    .hole(screw_hole_dia)
)

# Lid Pattern of holes (2 rows of small holes)
lid = (
    lid.faces(">Z").workplane()
    .center(-width/4, 0)
    .rarray(15, 15, 2, 8)
    .hole(screw_hole_dia)
)

# Move Lid Up for exploded view
lid = lid.translate((0, 0, height + 40))


# --- 3. Front Faceplate ---

faceplate = (
    cq.Workplane("XZ")
    .rect(width, height)
    .extrude(thickness)
)

# Front Features (Big Circular Cutout)
faceplate = (
    faceplate.faces(">Y").workplane()
    .center(-width/4, 0)
    .circle(front_circle_dia/2)
    .cutThruAll()
)

# Front Features (Rectangular Cutout with screw holes)
rect_center_x = -width/8
faceplate = (
    faceplate.faces(">Y").workplane()
    .center(rect_center_x, 0)
    .rect(front_rect_w, front_rect_h)
    .cutThruAll()
    # Add screw holes around rect
    .faces(">Y").workplane() # Reset to face
    .center(rect_center_x, 0)
    .rect(front_rect_w + 10, front_rect_h + 10, forConstruction=True)
    .vertices()
    .hole(screw_hole_dia)
)

# Mounting holes for faceplate (corners)
faceplate = (
    faceplate.faces(">Y").workplane()
    .rect(width - 20, height - 20, forConstruction=True)
    .vertices()
    .hole(screw_hole_dia)
)

# Cut matching holes in Chassis Front flange (implied)
# Since the chassis was a simple extrusion, we need to cut the front face of the chassis legs
# to match the faceplate mounting holes so it looks realistic.
chassis_front_holes = (
    cq.Workplane("XZ")
    .rect(width - 20, height - 20, forConstruction=True)
    .vertices()
    .circle(screw_hole_dia/2)
    .extrude(depth) # Cut through entire depth for simplicity or limit to front
)
# Actually, just cutting the front edge of the side walls
chassis = chassis.cut(
    chassis.faces("<Y").workplane()
    .pushPoints([(-width/2 + thickness/2, height/2 - 10), (width/2 - thickness/2, height/2 - 10)])
    .circle(screw_hole_dia/2)
    .extrude(10) # Cut into the metal
)


# Move Faceplate out for exploded view
faceplate = faceplate.translate((0, -depth/2 - 30, height/2))

# --- Assembly ---

# Combine parts into one result for visualization
# Note: In a real assembly we might use cq.Assembly, but 'result' variable usually expects a compound or solid.
result = chassis.union(lid).union(faceplate)

if 'show_object' in globals():
    show_object(result)