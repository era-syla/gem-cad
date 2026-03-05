import cadquery as cq

# Parameters
box_width = 80.0
box_depth = 60.0
box_height = 80.0
wall_thickness = 3.0

side_indent = 10.0  # How much the side walls are recessed
flange_width = 5.0  # The width of the vertical "ears" or flanges

center_cyl_outer_diam = 30.0
center_cyl_inner_diam = 25.0
center_cyl_height = box_height  # It spans the full height

screw_post_diam = 6.0
screw_hole_diam = 3.0
screw_post_offset = 5.0 # Distance from corner

# Calculate derived dimensions
inner_box_width = box_width - 2 * wall_thickness
inner_box_depth = box_depth - 2 * wall_thickness

# --- Main Body Construction ---

# 1. Start with the main U-shaped profile (extruded vertically)
# The profile looks like an H or a U with flanges. 
# It's easier to think of it as two large side plates connected by a central structure.

# Let's build the outer shape first.
# We will create the general rectangular prism and shell it/cut it.

# Create the main block
base = cq.Workplane("XY").box(box_width, box_depth, box_height)

# Create the large cutout in the center (the "through" hole perpendicular to the cylinder)
# Looking at the image, there's a rectangular void running through the depth.
cutout_width = box_width - 2 * side_indent
cutout_height = box_height - 2 * wall_thickness # Top and bottom walls remain
cutout_depth = box_depth + 10 # Through all

# Make the main central cavity
main_shape = (
    base
    .faces(">Y or <Y") # Select front and back faces
    .shell(-wall_thickness) # Shell inwards to create the walls
)

# Now we need to handle the specific "indented side" geometry.
# The image shows the side faces (left and right in the image) are recessed compared to the front/back plates.
# Let's refine the strategy: Build the profile in 2D and extrude.

# --- Profile Strategy ---

# Outer width: box_width
# Outer depth: box_depth
# Side wall recess: side_indent

# Let's sketch the top-down profile (XY plane) if we were extruding up.
# However, the features vary along Z (the cylinder is in the middle).
# Let's stick to boolean operations on primitives, it's often more robust for this kind of "bracket" shape.

# Re-starting the "Add/Cut" strategy which is clearer for this shape.

# 1. Front and Back Plates
plate_thickness = wall_thickness
plate_width = box_width
plate_height = box_height

front_plate = cq.Workplane("XZ").rect(plate_width, plate_height).extrude(plate_thickness).translate((0, box_depth/2 - plate_thickness/2, 0))
back_plate = cq.Workplane("XZ").rect(plate_width, plate_height).extrude(plate_thickness).translate((0, -box_depth/2 + plate_thickness/2, 0))

# 2. Side Walls (Recessed)
side_wall_depth = box_depth - 2 * plate_thickness
side_wall_width = wall_thickness
side_wall_height = box_height

# Position: offset from center X by (box_width/2 - side_indent)
left_wall = (
    cq.Workplane("YZ")
    .rect(side_wall_depth, side_wall_height)
    .extrude(side_wall_width)
    .translate((-box_width/2 + side_indent + side_wall_width/2, 0, 0))
)

right_wall = (
    cq.Workplane("YZ")
    .rect(side_wall_depth, side_wall_height)
    .extrude(side_wall_width)
    .translate((box_width/2 - side_indent - side_wall_width/2, 0, 0))
)

# 3. Top and Bottom Connecting Plates (between the side walls)
# Width spans between the side walls
# Depth spans full depth (connecting front and back plates)
connect_width = box_width - 2 * side_indent - 2 * side_wall_width
connect_depth = box_depth # Intersects front/back plates
connect_thickness = wall_thickness

top_connect = (
    cq.Workplane("XY")
    .rect(connect_width, connect_depth)
    .extrude(connect_thickness)
    .translate((0, 0, box_height/2 - connect_thickness/2))
)

bottom_connect = (
    cq.Workplane("XY")
    .rect(connect_width, connect_depth)
    .extrude(connect_thickness)
    .translate((0, 0, -box_height/2 + connect_thickness/2))
)

# Combine structural elements
structure = front_plate.union(back_plate).union(left_wall).union(right_wall).union(top_connect).union(bottom_connect)

# 4. Central Cylinder
# It goes from top to bottom, through the connecting plates.
cyl_outer = (
    cq.Workplane("XY")
    .circle(center_cyl_outer_diam / 2)
    .extrude(box_height)
    .translate((0, 0, -box_height/2))
)

cyl_inner = (
    cq.Workplane("XY")
    .circle(center_cyl_inner_diam / 2)
    .extrude(box_height + 2) # Slightly longer for clean cut
    .translate((0, 0, -box_height/2 - 1))
)

# Add cylinder to structure, then bore it out
structure = structure.union(cyl_outer).cut(cyl_inner)

# 5. Screw Bosses (The small tubes in the corners)
# They are located inside the "recess" area, attached to the side walls and the front/back plates.

# Coordinates for bosses
# X: Just inside the front/back plate overhang.
# Y: Inside the front/back plates.
# Z: There seem to be bosses at the top and bottom corners.

bosses = cq.Workplane("XY")

# We need 4 corners, but top and bottom. The image shows continuous long rods/tubes? 
# Looking closely at the image:
# - There are holes at the top face of the corner features.
# - There are holes at the bottom face.
# - It looks like a continuous cylinder running near the corner formed by the front plate and the recessed side wall.

boss_x = box_width/2 - side_indent/2 # Centered in the flange/overhang area
boss_y_dist = box_depth/2 - plate_thickness - screw_post_diam/2 

# Let's place 4 cylinders
boss_locs = [
    (boss_x, boss_y_dist),
    (boss_x, -boss_y_dist),
    (-boss_x, boss_y_dist),
    (-boss_x, -boss_y_dist),
]

boss_shape = (
    cq.Workplane("XY")
    .pushPoints(boss_locs)
    .circle(screw_post_diam / 2)
    .extrude(box_height)
    .translate((0, 0, -box_height/2))
)

boss_holes = (
    cq.Workplane("XY")
    .pushPoints(boss_locs)
    .circle(screw_hole_diam / 2)
    .extrude(box_height + 2)
    .translate((0, 0, -box_height/2 - 1))
)

# Fuse bosses and cut holes
structure = structure.union(boss_shape).cut(boss_holes)

# 6. Cleaning up the intersection between Top/Bottom plates and the Cylinder
# The image shows the top/bottom plates don't just intersect the cylinder, 
# there is a hole in them matching the cylinder bore.
# Since we unioned the cylinder outer and then cut the inner, the bore should exist.
# However, the rectangular top/bottom plates effectively block the cylinder if we don't cut them.
# The previous step `structure.union(cyl_outer).cut(cyl_inner)` handles this correctly 
# because the cut removes material from the *union* of the structure and the cylinder.

# 7. Fillets/Chamfers (Optional refinement based on image look)
# The image shows some rounded internal corners, but for a robust parametric model, 
# explicit large fillets can be fragile. We will stick to the primary geometry.
# There is a distinct transition where the side wall meets the front plate. 
# It looks like a step. Our geometry captures this.

# Final verification of the geometry based on the image:
# - Large outer front/back faces: Check.
# - Recessed side walls: Check.
# - Top/Bottom horizontal walls connecting sides: Check.
# - Central vertical tube: Check.
# - Corner screw bosses in the recess: Check.

result = structure