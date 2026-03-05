import cadquery as cq
import math

# --- Parameters ---
# Tube dimensions
tube_outer_diam = 25.0
tube_inner_diam = 22.0
tube_thickness = (tube_outer_diam - tube_inner_diam) / 2.0

# Bracket/Plate dimensions
plate_thickness = 3.0

# --- Helper Functions ---

def create_tube(length, outer_d, inner_d):
    """Creates a hollow tube along the Z axis centered at the origin."""
    return cq.Workplane("XY").circle(outer_d/2).circle(inner_d/2).extrude(length)

def create_tube_segment(p1, p2, outer_d, inner_d):
    """Creates a tube connecting two points."""
    # Vector math to orient the tube
    v = cq.Vector(p2) - cq.Vector(p1)
    length = v.Length
    
    # Create the tube along Z
    tube = create_tube(length, outer_d, inner_d)
    
    # Rotate and translate to align with p1->p2
    # Initial direction is (0,0,1)
    # Target direction is v/length
    
    midpoint = (cq.Vector(p1) + cq.Vector(p2)) * 0.5
    
    # Find rotation axis and angle
    initial_dir = cq.Vector(0, 0, 1)
    target_dir = v.normalized()
    
    axis = initial_dir.cross(target_dir)
    angle = math.degrees(math.acos(initial_dir.dot(target_dir)))
    
    if axis.Length < 1e-5: # Parallel
        if initial_dir.dot(target_dir) < 0: # Anti-parallel
            tube = tube.rotate((0,0,0), (1,0,0), 180)
    else:
        tube = tube.rotate((0,0,0), axis, angle)
        
    tube = tube.translate(p1)
    return tube

# --- Geometry Construction ---

# 1. Main Frame Loop / Roll Hoop Structure
# Define key points in space roughly based on the visual perspective
p_top_left = (-150, 0, 400)
p_top_right = (150, 0, 400)
p_mid_left = (-200, 0, 200)
p_mid_right = (200, 0, 200)
p_bot_left = (-180, 0, 0)
p_bot_right = (180, 0, 0)

# Tubes
tubes = []

# Vertical/Slanted main pillars
tubes.append(create_tube_segment(p_bot_left, p_mid_left, tube_outer_diam, tube_inner_diam))
tubes.append(create_tube_segment(p_mid_left, p_top_left, tube_outer_diam, tube_inner_diam))
tubes.append(create_tube_segment(p_bot_right, p_mid_right, tube_outer_diam, tube_inner_diam))
tubes.append(create_tube_segment(p_mid_right, p_top_right, tube_outer_diam, tube_inner_diam))

# Cross bars
tubes.append(create_tube_segment(p_top_left, p_top_right, tube_outer_diam, tube_inner_diam))
tubes.append(create_tube_segment(p_mid_left, p_mid_right, tube_outer_diam, tube_inner_diam))

# Forward supports (the angled pieces going towards the "front")
p_front_left_upper = (-150, 300, 250)
p_front_right_upper = (150, 300, 250)
p_front_left_lower = (-150, 300, 50)
p_front_right_lower = (150, 300, 50)

tubes.append(create_tube_segment(p_mid_left, p_front_left_upper, tube_outer_diam, tube_inner_diam))
tubes.append(create_tube_segment(p_mid_right, p_front_right_upper, tube_outer_diam, tube_inner_diam))

# Lower side rails
tubes.append(create_tube_segment(p_bot_left, p_front_left_lower, tube_outer_diam, tube_inner_diam))
tubes.append(create_tube_segment(p_bot_right, p_front_right_lower, tube_outer_diam, tube_inner_diam))

# Connecting front supports vertically
tubes.append(create_tube_segment(p_front_left_lower, p_front_left_upper, tube_outer_diam, tube_inner_diam))
tubes.append(create_tube_segment(p_front_right_lower, p_front_right_upper, tube_outer_diam, tube_inner_diam))


# 2. Sheet Metal Brackets / Gussets

def create_gusset(p1, p2, p3, thickness):
    """Creates a triangular plate defined by 3 points."""
    v1 = cq.Vector(p1)
    v2 = cq.Vector(p2)
    v3 = cq.Vector(p3)
    
    # Define a local plane
    center = (v1 + v2 + v3) / 3.0
    normal = (v2 - v1).cross(v3 - v1).normalized()
    
    # Project points to 2D for drawing sketch (simplified approach: create flat then rotate)
    # Instead, let's use Workplane with 3 points
    wp = cq.Workplane(cq.Plane(origin=v1, xDir=v2-v1, normal=normal))
    
    # Coordinates in local plane
    # v1 is origin (0,0)
    # v2 is on x-axis
    d2 = (v2 - v1).Length
    # v3 geometric projection
    x3 = (v3 - v1).dot((v2-v1).normalized())
    y3 = ((v3 - v1) - (v2-v1).normalized() * x3).Length
    
    # Ensure winding order or correct orientation isn't flipped by math
    # A simple triangle polygon
    pts = [(0,0), (d2, 0), (x3, y3)]
    
    return wp.polyline(pts).close().extrude(thickness)

# Bracket clusters
brackets = []

# Top corner gussets
g1 = create_gusset(
    (p_top_left[0], p_top_left[1], p_top_left[2] - 50),
    (p_top_left[0] + 50, p_top_left[1], p_top_left[2]),
    (p_top_left[0], p_top_left[1] + 50, p_top_left[2] - 20),
    plate_thickness
)
brackets.append(g1)

g2 = create_gusset(
    (p_top_right[0], p_top_right[1], p_top_right[2] - 50),
    (p_top_right[0] - 50, p_top_right[1], p_top_right[2]),
    (p_top_right[0], p_top_right[1] + 50, p_top_right[2] - 20),
    plate_thickness
)
brackets.append(g2)

# Mid-section mounting plates (Complex folded shapes approximated)
def create_mounting_bracket(pos, angle_rotation):
    """Creates a generic mounting bracket found at nodes."""
    base = cq.Workplane("XY").rect(60, 80).extrude(plate_thickness)
    
    # Add a flange
    flange = (cq.Workplane("XZ")
              .workplane(offset=-40)
              .moveTo(0, plate_thickness)
              .lineTo(0, 50)
              .lineTo(60, 50)
              .lineTo(60, plate_thickness)
              .close()
              .extrude(plate_thickness)
              .translate((-30, 0, 0))
             )
             
    bracket = base.union(flange)
    bracket = bracket.rotate((0,0,0), (0,0,1), angle_rotation)
    bracket = bracket.translate(pos)
    return bracket

# Place brackets at key nodes
brackets.append(create_mounting_bracket(p_mid_left, 90))
brackets.append(create_mounting_bracket(p_mid_right, -90))
brackets.append(create_mounting_bracket(p_front_left_upper, 45))
brackets.append(create_mounting_bracket(p_front_right_upper, -45))

# Lower upright flat plates (Uprights)
def create_upright_plate(pos):
    plate = (cq.Workplane("YZ")
             .moveTo(0,0)
             .lineTo(50, 0)
             .lineTo(40, 150)
             .lineTo(10, 150)
             .close()
             .extrude(plate_thickness)
             .translate(pos)
             )
    return plate

brackets.append(create_upright_plate((p_front_left_lower[0]-10, p_front_left_lower[1], p_front_left_lower[2])))
brackets.append(create_upright_plate((p_front_right_lower[0]+10, p_front_right_lower[1], p_front_right_lower[2])))

# --- Assembly ---
result = tubes[0]
for t in tubes[1:]:
    result = result.union(t)

for b in brackets:
    result = result.union(b)

# Final cleanup/orientations if needed (Optional)
# Orient so Y is up to match typical "Up" view if needed, but keeping Z up as is standard CAD