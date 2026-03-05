import cadquery as cq

# T-junction pipe connector
# Main horizontal pipe along X axis, vertical pipe along Z axis

outer_r = 15
inner_r = 11
wall = outer_r - inner_r

# Lengths of each arm
horiz_len = 50  # total horizontal length (each side ~25)
vert_len = 50   # total vertical length

# Create horizontal cylinder (along X axis)
horiz = (
    cq.Workplane("YZ")
    .circle(outer_r)
    .extrude(horiz_len, both=True)
)

# Create vertical cylinder (along Z axis)
vert = (
    cq.Workplane("XY")
    .circle(outer_r)
    .extrude(vert_len, both=True)
)

# Union the two cylinders
body = horiz.union(vert)

# Now hollow out the pipes
# Hollow horizontal pipe
horiz_hole = (
    cq.Workplane("YZ")
    .circle(inner_r)
    .extrude(horiz_len, both=True)
)

# Hollow vertical pipe
vert_hole = (
    cq.Workplane("XY")
    .circle(inner_r)
    .extrude(vert_len, both=True)
)

body = body.cut(horiz_hole).cut(vert_hole)

# Add small diagonal gussets/fillets at the junction
# The junction between horizontal and vertical pipes

# Add cross-shaped slots/holes on the pipe ends (decorative connector holes)
# These are the cross-shaped cutouts visible on each pipe end

def add_cross_slots(wp_workplane, pipe_len, pipe_outer_r, pipe_inner_r, axis='Z'):
    """Add cross-shaped slot holes near pipe ends"""
    slot_w = 3
    slot_h = 6
    slot_depth = wall + 2
    
    return wp_workplane

# Let's add the cross slots manually
# For vertical pipe - top end
slot_w = 3.0
slot_h = 7.0

# Top of vertical pipe - 4 slots arranged in cross pattern
for angle in [0, 90, 180, 270]:
    rad = __import__('math').radians(angle)
    import math
    # Slot on the side of the pipe near top
    # Position slot on the curved surface
    x_pos = (outer_r - wall/2) * math.cos(rad)
    y_pos = (outer_r - wall/2) * math.sin(rad)
    
    # Create slot as a small box cutting through wall
    slot = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(x_pos, y_pos, vert_len - 8))
        .rect(slot_w, slot_h)
        .extrude(wall + 2, both=True)
    )
    # Actually use radial cuts
    pass

# Simpler approach: drill small rectangular holes through pipe walls near ends
def drill_cross_holes(solid, center_z, pipe_outer_r, slot_w=3, slot_h=7):
    """Drill 4 cross-shaped holes through pipe wall at given Z height"""
    import math
    result = solid
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        # Direction vector
        dx = math.cos(rad)
        dy = math.sin(rad)
        
        cutter = (
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(0, 0, center_z),
                         rotate=cq.Vector(0, 0, angle))
            .rect(slot_w, slot_h)
            .extrude(pipe_outer_r + 2, both=True)
        )
        result = result.cut(cutter)
    return result

# Drill holes at ends of each arm
# Vertical top
body = drill_cross_holes(body, vert_len - 10, outer_r)
# Vertical bottom  
body = drill_cross_holes(body, -(vert_len - 10), outer_r)
# Horizontal +X
import math
def drill_cross_holes_x(solid, center_x, pipe_outer_r, slot_w=3, slot_h=7):
    result = solid
    for angle in [0, 90, 180, 270]:
        cutter = (
            cq.Workplane("YZ")
            .transformed(offset=cq.Vector(0, 0, center_x),
                         rotate=cq.Vector(0, 0, angle))
            .rect(slot_w, slot_h)
            .extrude(pipe_outer_r + 2, both=True)
        )
        result = result.cut(cutter)
    return result

body = drill_cross_holes_x(body, horiz_len - 10, outer_r)
body = drill_cross_holes_x(body, -(horiz_len - 10), outer_r)

result = body