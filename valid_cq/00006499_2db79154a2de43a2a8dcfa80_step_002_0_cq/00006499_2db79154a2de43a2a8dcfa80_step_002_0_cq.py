import cadquery as cq
import math

# --- Parameters ---
thickness = 15.0        # Thickness of the main plate
width = 160.0           # Overall width of the base
height = 120.0          # Overall height from base to top of the arc
rim_width = 30.0        # Width of the frame border
corner_radius = 5.0     # Small fillet on corners, if needed (optional)

# Hole parameters
num_holes = 7           # Total number of square holes
hole_side = 10.0        # Side length of square holes
hole_offset = 15.0      # Distance from outer edge to center of holes (approx)

# Eyelet parameters
eye_outer_radius = 12.0
eye_inner_radius = 6.0
eye_thickness = 8.0

# --- Geometry Construction ---

# 1. Create the Main Body (Outer Profile)
# The shape is essentially a rectangle at the bottom and a semi-circle on top.
# However, the image shows a continuous "tombstone" or arch shape.

# Calculate radii
outer_radius = width / 2.0
inner_radius = outer_radius - rim_width

# Center of the arc portion
arc_center_y = height - outer_radius

# We will sketch the front face and extrude
# Let's define the outer profile first
# The bottom corners are sharp in the image, top is round.

# Create the main D-shape
# We'll use a Workplane on XY
main_body = (
    cq.Workplane("XY")
    .moveTo(-outer_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, arc_center_y)
    .threePointArc((0, height), (-outer_radius, arc_center_y))
    .close()
    .extrude(thickness)
)

# 2. Create the Central Cutout (Inner D-shape)
# The bottom of the cutout seems to be straight, creating a bar at the bottom.
# Let's assume the rim width is consistent all around, including the bottom.
cutout_bottom_y = rim_width

# The inner cutout needs to be an arc on top and straight sides/bottom
# Inner arc center is the same as outer arc center
# Inner straight height ends at arc_center_y
inner_shape = (
    cq.Workplane("XY")
    .moveTo(-inner_radius, cutout_bottom_y)
    .lineTo(inner_radius, cutout_bottom_y)
    .lineTo(inner_radius, arc_center_y)
    .threePointArc((0, height - rim_width), (-inner_radius, arc_center_y))
    .close()
    .extrude(thickness)
)

# Subtract inner shape from outer shape
plate = main_body.cut(inner_shape)

# 3. Create Square Holes
# The holes follow the curvature of the outer arc.
# We need to distribute them along a path offset from the outer edge.

# Calculate the path radius for the hole centers along the arc
hole_path_radius = outer_radius - (rim_width / 2.0)

# We have vertical straight sections and an arc section.
# Looking at the image, the holes are distributed along the arch and the sides.
# Let's define positions manually or polar-ly for the arc, and cartesian for sides.
# There appear to be holes roughly at:
# - Left Side Middle
# - Left Shoulder
# - Top Left
# - Top Right
# - Right Shoulder
# - Right Side Middle
# And maybe one more lower down?
# Let's count again: 3 on left curve/side, 3 on right curve/side... wait, image shows 8 holes visible?
# Let's look closer.
# Left side: One low, one mid-straight, one on corner transition, one on top arc.
# Right side: Symmetric.
# Total 8 holes.

hole_positions = []

# Define vertical positions for the straight section holes
# The straight section goes from y=0 to y=arc_center_y.
# Let's put one near bottom, one near top of straight section.
h1_y = cutout_bottom_y + (hole_side) 
h2_y = arc_center_y - (hole_side)

# Side holes (x is +/- hole_path_radius)
hole_positions.append((-hole_path_radius, h1_y))
hole_positions.append((hole_path_radius, h1_y))
hole_positions.append((-hole_path_radius, h2_y))
hole_positions.append((hole_path_radius, h2_y))

# Arc holes
# We need points on the arc part.
# The arc starts at angle 0 (right) to 180 (left) relative to center (0, arc_center_y).
# We want holes distributed on this arc.
# Let's place them at 30, 60, 120, 150 degrees.
angles = [30, 60, 120, 150]
for angle in angles:
    rad = math.radians(angle)
    x = hole_path_radius * math.cos(rad)
    y = arc_center_y + hole_path_radius * math.sin(rad)
    hole_positions.append((x, y))

# Cut the holes
for pos in hole_positions:
    # Use a local workplane for each hole to cut perpendicular to face
    plate = (
        plate.faces(">Z")
        .workplane()
        .moveTo(pos[0], pos[1])
        .rect(hole_side, hole_side)
        .cutBlind(-thickness)
    )

# 4. Create the Lifting Eyelet
# Located at the very top center (0, height, thickness/2)
# Orientation: The ring faces forward (axis along Y or Z? Looks like axis is along Y, plane is XZ)
# Wait, looking at the image, the eyelet loop is in the plane of the plate (XY plane basically), 
# but rotated 90 degrees so the hole goes through Front-to-Back? 
# No, usually lifting eyes have the hole going sideways or front-back. 
# In the image, we see through the hole. The hole axis is parallel to the Thickness vector (Z axis).
# So the ring is flat against the top edge? No, it's standing up.
# Let's look at the shadow/shading.
# The hole axis is parallel to the Z axis (the thickness direction).
# It looks like a torus or a tube standing on top of the arch.

eye_center = (0, height + eye_outer_radius - 2) # Sinking it slightly into the body for overlap

eyelet = (
    cq.Workplane("XY")
    .moveTo(eye_center[0], eye_center[1])
    .circle(eye_outer_radius)
    .extrude(eye_thickness)
)

eyelet_hole = (
    cq.Workplane("XY")
    .moveTo(eye_center[0], eye_center[1])
    .circle(eye_inner_radius)
    .extrude(eye_thickness)
)

# Center the eyelet on the thickness of the plate
# Current plate is Z=0 to Z=thickness.
# Eyelet is Z=0 to Z=eye_thickness.
# We need to move eyelet to Z = (thickness - eye_thickness) / 2
z_offset = (thickness - eye_thickness) / 2.0
eyelet = eyelet.translate((0, 0, z_offset))
eyelet_hole = eyelet_hole.translate((0, 0, z_offset))

final_eyelet = eyelet.cut(eyelet_hole)

# Combine plate and eyelet
result = plate.union(final_eyelet)

# Optional: Add small fillets to the outer edges for realism (as seen in smooth shading)
result = result.edges("|Z").fillet(1.0)
result = result.edges(">Z").fillet(1.0)
result = result.edges("<Z").fillet(1.0)

# Export or Display (CadQuery usually expects 'result' variable)