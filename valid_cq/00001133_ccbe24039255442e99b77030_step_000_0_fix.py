import cadquery as cq

# Create a roll cage / tube frame structure for an off-road vehicle
# Using tubes (pipes) along defined paths

tube_r = 0.8  # tube outer radius
wall = 0.15   # tube wall thickness

def make_tube(start, end, r=tube_r):
    """Create a cylindrical tube between two points"""
    import math
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dz = end[2] - start[2]
    length = math.sqrt(dx**2 + dy**2 + dz**2)
    if length < 0.01:
        return None
    
    # Create cylinder along Z, then orient
    cyl = cq.Workplane("XY").circle(r).extrude(length)
    
    # Direction vector
    import cadquery as cq2
    from cadquery import Vector
    
    # Use CadQuery's built-in transformation
    # Place cylinder at origin pointing up, then transform
    zv = Vector(0, 0, 1)
    dv = Vector(dx/length, dy/length, dz/length)
    
    # Get rotation axis and angle
    cross = zv.cross(dv)
    dot = zv.dot(dv)
    
    shape = cyl.val()
    
    if cross.Length < 1e-6:
        if dot < 0:
            shape = shape.rotate(cq.Vector(1,0,0), cq.Vector(-1,0,0).add(cq.Vector(0,0,0)), 180)
        # Already aligned
    else:
        import math
        angle = math.degrees(math.acos(max(-1, min(1, dot))))
        ax_start = (0, 0, 0)
        ax_end = (cross.x, cross.y, cross.z)
        shape = shape.rotate(cq.Vector(*ax_start), cq.Vector(*ax_end), angle)
    
    # Translate to start point
    shape = shape.translate(cq.Vector(*start))
    return shape

# Define key frame points for a buggy/UTV roll cage
# Scale: roughly 30 units long, 15 wide, 12 tall

# Bottom frame points (ground level, z=0)
# Front section
BFL = (-14, -5, 0)   # bottom front left
BFR = (-14, 5, 0)    # bottom front right
# Middle section  
BML = (-2, -7, 0)    # bottom mid left
BMR = (-2, 7, 0)     # bottom mid right
BML2 = (6, -7, 0)
BMR2 = (6, 7, 0)
# Rear section
BRL = (14, -5, 0)    # bottom rear left
BRR = (14, 5, 0)     # bottom rear right

# Top frame points
TFL = (-12, -5, 8)
TFR = (-12, 5, 8)
TML = (0, -7, 10)
TMR = (0, 7, 10)
TML2 = (7, -6, 9)
TMR2 = (7, 6, 9)
TRL = (12, -4, 7)
TRR = (12, 4, 7)

# Additional points for cage structure
MFL = (-8, -6, 5)
MFR = (-8, 6, 5)

# Define all tube segments as (start, end) pairs
segments = [
    # Bottom perimeter
    (BFL, BFR),
    (BFL, BML), (BFR, BMR),
    (BML, BML2), (BMR, BMR2),
    (BML2, BRL), (BMR2, BRR),
    (BRL, BRR),
    
    # Top perimeter
    (TFL, TFR),
    (TFL, TML), (TFR, TMR),
    (TML, TML2), (TMR, TMR2),
    (TML2, TRL), (TMR2, TRR),
    (TRL, TRR),
    
    # Vertical/diagonal uprights
    (BFL, TFL), (BFR, TFR),
    (BML, TML), (BMR, TMR),
    (BML2, TML2), (BMR2, TMR2),
    (BRL, TRL), (BRR, TRR),
    
    # Cross braces top
    (TFL, TMR), (TFR, TML),
    (TML2, TRR), (TMR2, TRL),
    
    # Side diagonals
    (MFL, TML), (MFR, TMR),
    (BFL, MFL), (BFR, MFR),
    (MFL, BML), (MFR, BMR),
    
    # Front nose
    (BFL, (-18, 0, 2)), (BFR, (-18, 0, 2)),
    (TFL, (-16, 0, 6)),
    ((-18, 0, 2), (-16, 0, 6)),
    
    # Additional cross members
    (BML, BMR),
    (BML2, BMR2),
    (TML, TMR),
    (TML2, TMR2),
]

# Build the result by unioning all tubes
shapes = []
for seg in segments:
    s = make_tube(seg[0], seg[1], tube_r)
    if s is not None:
        shapes.append(s)

# Union all shapes
from cadquery import Compound
import cadquery as cq

result = cq.Workplane("XY")
combined = shapes[0]
for s in shapes[1:]:
    try:
        combined = combined.fuse(s)
    except:
        pass

result = cq.Workplane("XY").add(combined)