import cadquery as cq

# --- Parameters ---

# Main body dimensions
body_width = 160.0
body_depth = 80.0
body_height_front = 10.0
body_height_rear = 30.0
wall_thickness = 4.0

# Faceplate recess (where the screen and knob sit)
recess_width = 130.0
recess_depth = 60.0
recess_offset = 2.0  # Depth of the recess

# Screen cutout
screen_w = 60.0
screen_h = 35.0
screen_center_offset_x = 15.0 # Shifted right from center

# Knob/Button area
knob_outer_dia = 32.0
knob_inner_dia = 28.0 # The hole
knob_height = 8.0     # The raised cylinder
knob_center_offset_x = -35.0 # Shifted left from center

# Switch/Connector slot
slot_w = 12.0
slot_h = 4.0
slot_offset_x = 50.0
slot_offset_y = 10.0

# Mounting Holes (Main body corners)
mount_hole_dia = 6.0
mount_cbore_dia = 12.0
mount_cbore_depth = 20.0 # Deep enough to cut through the sloped surface

# PCB Mounting Holes (small holes in the recessed area)
pcb_hole_dia = 2.5
pcb_hole_locations = [
    (recess_width/2 - 4, recess_depth/2 - 4),
    (recess_width/2 - 4, -recess_depth/2 + 4),
    (-recess_width/2 + 4, recess_depth/2 - 4),
    (-recess_width/2 + 4, -recess_depth/2 + 4),
]

# --- Geometry Construction ---

# 1. Create the base wedge shape
# We'll sketch the side profile and extrude it.
profile_pts = [
    (0, 0),
    (body_width, 0),
    (body_width, body_height_front),
    (0, body_height_rear)
]

base = (
    cq.Workplane("XZ")
    .polyline(profile_pts)
    .close()
    .extrude(body_depth)
)

# Center the object
base = base.translate((-body_width/2, -body_depth/2, 0))

# 2. Create the slanted top face reference
# The top face is angled. We need a workplane on that face to cut the recess.
# Calculating angle: atan((30-10)/160)
import math
angle_rad = math.atan2((body_height_rear - body_height_front), body_width)
angle_deg = math.degrees(angle_rad)

# We will create a plane rotated to match the slope, positioned correctly.
# Easier method: Use the top face selector, but it can be tricky with complex shapes.
# Let's create the cut relative to the world XY plane but rotated.

# Create a cutting tool for the main recess
recess_cutter = (
    cq.Workplane("XY")
    .rect(recess_width, recess_depth)
    .extrude(20) # Tall enough to cut
)

# Rotate and position the cutter
# It needs to be parallel to the top slope
# We rotate around the Y axis (which is along depth in CadQuery default, wait...)
# In step 1, X is width, Z is height, Y is depth.
# The slope goes down along positive X.
# Rotation is around Y axis.
recess_cutter = (
    recess_cutter
    .rotate((0,0,0), (0,1,0), -angle_deg)
    .translate((0, 0, body_height_rear - (recess_width/2 * math.tan(angle_rad)) - recess_offset))
)

# Apply the recess cut
body = base.cut(recess_cutter)


# 3. Create the features on the recessed plane
# To do this accurately, we make a workplane on the newly cut flat face.
# We select the large flat face that corresponds to the recess bottom.
recess_plane = body.faces(">Z").workplane()

# Cut the Screen Hole
body = (
    recess_plane
    .center(screen_center_offset_x, 0)
    .rect(screen_w, screen_h)
    .cutThruAll()
)

# Add the Knob Housing (Raised cylinder with hole)
# Reset workplane center
knob_feature = (
    recess_plane
    .center(knob_center_offset_x, 0)
    .circle(knob_outer_dia/2)
    .extrude(knob_height)
)

knob_hole = (
    recess_plane
    .center(knob_center_offset_x, 0)
    .circle(knob_inner_dia/2)
    .cutThruAll()
)

body = body.union(knob_feature).cut(knob_hole)

# Add the small slot (top right area)
body = (
    recess_plane
    .center(slot_offset_x, slot_offset_y)
    .rect(slot_w, slot_h)
    .cutThruAll()
)

# 4. Add PCB mounting holes in the corners of the recess
for loc in pcb_hole_locations:
    body = (
        recess_plane
        .center(loc[0], loc[1])
        .circle(pcb_hole_dia/2)
        .cutThruAll()
        .center(-loc[0], -loc[1]) # Reset center for next iteration
    )


# 5. Add Main Mounting Holes (Counterbored) on the main body corners
# These go vertically down, regardless of slope.
# Locations relative to center of the bounding box (approx)
corner_offset_x = body_width/2 - 10
corner_offset_y = body_depth/2 - 10

corners = [
    (-corner_offset_x, -corner_offset_y),
    (-corner_offset_x, corner_offset_y),
    (corner_offset_x, -corner_offset_y),
    (corner_offset_x, corner_offset_y),
]

for x, y in corners:
    # Counterbore logic: Cut large hole partly, small hole through
    
    # We create a workplane at a high Z to ensure we catch the highest point of the slope
    wp = cq.Workplane("XY").workplane(offset=body_height_rear + 5)
    
    # The counterbore (large hole)
    # We need to calculate depth based on the surface, but simple blind cut works visually
    # The request image shows deep "scalloped" cutouts into the slope.
    
    cbore = (
        wp
        .center(x, y)
        .circle(mount_cbore_dia/2)
        .extrude(-mount_cbore_depth) # Cut downwards
    )
    
    thru = (
        wp
        .center(x, y)
        .circle(mount_hole_dia/2)
        .extrude(-100) # Cut all the way down
    )
    
    body = body.cut(cbore).cut(thru)

# 6. Hollow out the underside (Shelling)
# To make it a housing, we remove the bottom face and leave walls.
# However, shelling complex geometry with booleans often fails.
# A robust way is to create an inner tool and cut it.

# Create the inner cutting shape
inner_profile_pts = [
    (wall_thickness, wall_thickness),
    (body_width - wall_thickness, wall_thickness),
    (body_width - wall_thickness, body_height_front - wall_thickness),
    (wall_thickness, body_height_rear - wall_thickness)
]

shell_tool = (
    cq.Workplane("XZ")
    .polyline(inner_profile_pts)
    .close()
    .extrude(body_depth - 2*wall_thickness)
)
shell_tool = shell_tool.translate((-body_width/2, -(body_depth/2 - wall_thickness), 0))

# We need to be careful not to cut away the material supporting the recess.
# The recess cuts down into the solid. The shell cuts up from the bottom.
# Let's check intersection. A simple cut is usually safer for visual models.
body = body.cut(shell_tool)

result = body