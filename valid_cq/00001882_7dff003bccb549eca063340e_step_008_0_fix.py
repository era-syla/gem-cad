import cadquery as cq
import math

# Create a sheep/lamb cookie cutter shape
# The cookie cutter has a thin wall following the sheep outline with a handle/top

def make_sheep_cookie_cutter():
    # Define sheep outline points (approximate from image)
    # The sheep has a fluffy body outline with legs and head
    
    # Create the sheep profile as a series of points forming the outline
    # Scale: roughly 80mm wide, 55mm tall
    
    # Outer profile points for sheep silhouette (clockwise)
    # Starting from bottom-left, going around
    
    sheep_pts = [
        # Bottom of legs
        (-25, -25),
        (-22, -28),
        (-18, -28),
        (-15, -25),
        (-10, -25),
        (-7, -28),
        (-3, -28),
        (0, -25),
        (5, -25),
        (8, -28),
        (12, -28),
        (15, -25),
        # Right side / tail area
        (20, -22),
        (25, -18),
        (28, -12),
        # Right bump (tail)
        (32, -8),
        (35, -3),
        (33, 2),
        (28, 5),
        # Top right area
        (25, 8),
        (30, 12),
        (35, 15),
        (38, 20),
        (35, 25),
        # Head area (right side)
        (30, 28),
        (25, 30),
        (20, 28),
        (15, 25),
        # Top middle - fluffy wool bumps
        (10, 28),
        (5, 32),
        (0, 35),
        (-5, 32),
        (-10, 30),
        (-15, 33),
        (-20, 30),
        # Left top
        (-25, 25),
        (-30, 20),
        (-32, 15),
        # Left side bumps
        (-35, 10),
        (-38, 5),
        (-35, 0),
        (-32, -5),
        # Back to bottom left
        (-30, -12),
        (-28, -18),
        (-25, -25),
    ]
    
    # Create the outer wire using spline
    outer = (
        cq.Workplane("XY")
        .polyline(sheep_pts)
        .close()
    )
    
    # Scale down inner profile for the cutter wall
    scale = 0.85
    inner_pts = [(x * scale, y * scale) for x, y in sheep_pts[:-1]]
    
    inner = (
        cq.Workplane("XY")
        .polyline(inner_pts)
        .close()
    )
    
    # Extrude outer shape
    outer_solid = (
        cq.Workplane("XY")
        .polyline(sheep_pts)
        .close()
        .extrude(12)
    )
    
    # Extrude inner shape to cut
    inner_solid = (
        cq.Workplane("XY")
        .polyline(inner_pts)
        .close()
        .extrude(12)
    )
    
    # Subtract inner from outer to make cookie cutter walls
    cutter = outer_solid.cut(inner_solid)
    
    # Add a base/bottom strip (thin bottom)
    base = (
        cq.Workplane("XY")
        .polyline(sheep_pts)
        .close()
        .extrude(1.5)
    )
    
    result = cutter.union(base)
    return result

# Alternative simpler approach using offset approach
def make_sheep_simple():
    # Simple sheep cookie cutter using basic shapes combined
    
    # Main body - ellipse approximated with scaled circle
    body = (
        cq.Workplane("XY")
        .ellipseArc(35, 22, 0, 360, 0)
        .close()
        .extrude(12)
    )
    
    # Create hollow body
    body_inner = (
        cq.Workplane("XY")
        .ellipseArc(30, 17, 0, 360, 0)
        .close()
        .extrude(12)
    )
    
    body_cutter = body.cut(body_inner)
    
    # Head
    head = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(30, 10, 0))
        .circle(12)
        .extrude(12)
    )
    head_inner = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(30, 10, 0))
        .circle(8)
        .extrude(12)
    )
    head_wall = head.cut(head_inner)
    
    result = body_cutter.union(head_wall)
    return result

# Use the polyline approach
try:
    result = make_sheep_cookie_cutter()
except:
    # Fallback to simple version
    result = make_sheep_simple()