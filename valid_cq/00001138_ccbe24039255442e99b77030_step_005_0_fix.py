import cadquery as cq

def make_tube(start, end, radius=5):
    """Create a tube (cylinder) between two points."""
    import numpy as np
    start = cq.Vector(*start)
    end = cq.Vector(*end)
    diff = end - start
    length = diff.Length
    if length < 0.001:
        return None
    mid = cq.Vector((start.x + end.x)/2, (start.y + end.y)/2, (start.z + end.z)/2)
    
    # direction vector
    dx, dy, dz = diff.x/length, diff.y/length, diff.z/length
    
    # Create cylinder along Z, then rotate to align with direction
    tube = (cq.Workplane("XY")
            .circle(radius)
            .extrude(length))
    
    # We need to rotate from Z-axis to the direction vector
    # Use transformation approach
    z_axis = cq.Vector(0, 0, 1)
    dir_vec = cq.Vector(dx, dy, dz)
    
    # Get rotation axis and angle
    cross = z_axis.cross(dir_vec)
    cross_len = cross.Length
    dot = z_axis.dot(dir_vec)
    
    if cross_len < 1e-6:
        if dot < 0:
            # opposite direction
            tube = tube.rotate((0,0,0), (1,0,0), 180)
        # else same direction, no rotation needed
    else:
        angle = float(cq.Vector(0,0,1).cross(dir_vec).Length)
        import math
        angle_deg = math.degrees(math.atan2(cross_len, dot))
        ax = cross.normalized()
        tube = tube.rotate((0,0,0), (ax.x, ax.y, ax.z), angle_deg)
    
    # Translate to start position
    tube = tube.translate((start.x, start.y, start.z))
    return tube

# Define the go-kart frame tubes as pairs of (start, end) points
# Frame is roughly 400 long, 150 wide, scaled appropriately
r = 4  # tube radius

tubes_coords = [
    # Main bottom frame - left side
    ((0, 0, 0), (350, 0, 0)),
    # Main bottom frame - right side
    ((0, 80, 0), (350, 80, 0)),
    # Front cross member
    ((0, 0, 0), (0, 80, 0)),
    # Rear cross members
    ((350, 0, 0), (350, 80, 0)),
    ((300, 0, 0), (300, 80, 0)),
    ((250, 0, 0), (250, 80, 0)),
    # Nose cone - converging front
    ((0, 0, 0), (-80, 40, 0)),
    ((0, 80, 0), (-80, 40, 0)),
    # Nose tip extension
    ((-80, 40, 0), (-120, 40, 0)),
    # Roll hoop - left upright
    ((80, 0, 0), (80, 0, 70)),
    # Roll hoop - right upright
    ((80, 80, 0), (80, 80, 70)),
    # Roll hoop - top bar
    ((80, 0, 70), (80, 80, 70)),
    # Roll hoop - diagonal braces from top
    ((80, 0, 70), (120, 0, 0)),
    ((80, 80, 70), (120, 80, 0)),
    # Side bars at height - left
    ((80, 0, 70), (200, 0, 40)),
    ((80, 80, 70), (200, 80, 40)),
    # Upper rear rails
    ((200, 0, 40), (300, 0, 0)),
    ((200, 80, 40), (300, 80, 0)),
    # Front diagonal braces
    ((80, 0, 0), (80, 0, 70)),
    # Additional cross braces
    ((150, 0, 0), (150, 80, 0)),
    ((200, 0, 40), (200, 80, 40)),
    # Rear wing/axle mounts
    ((300, 0, 0), (320, -20, 0)),
    ((300, 80, 0), (320, 100, 0)),
    # Front axle bar
    ((0, -10, 0), (0, 90, 0)),
]

# Build all tubes and union them
result = None
for start, end in tubes_coords:
    try:
        tube = make_tube(start, end, radius=r)
        if tube is not None:
            if result is None:
                result = tube
            else:
                result = result.union(tube)
    except Exception:
        continue

if result is None:
    result = cq.Workplane("XY").box(10, 10, 10)