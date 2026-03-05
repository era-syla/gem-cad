import cadquery as cq
import math

# Parameters
head_diameter = 16
head_height = 6
shank_diameter = 10
shank_length = 35
thread_pitch = 2
thread_depth = 0.7

# Create the bolt head (cylinder)
head = (
    cq.Workplane("XY")
    .cylinder(head_height, head_diameter / 2)
)

# Create the shank
shank = (
    cq.Workplane("XY")
    .workplane(offset=head_height)
    .cylinder(shank_length, shank_diameter / 2)
)

# Combine head and shank
bolt = head.union(shank)

# Add thread approximation using helical cuts
# We'll approximate threads by cutting grooves along the shank

# Build thread profile as a series of annular cuts
# Use a wire path approach - create thread as swept shape

# Create the threaded shank with approximate threads
# We'll do this by creating a helical path and sweeping a triangle profile

num_turns = int(shank_length / thread_pitch)

# Create base solid
base = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
)

shank_solid = (
    cq.Workplane("XY")
    .workplane(offset=head_height)
    .circle(shank_diameter / 2)
    .extrude(shank_length)
)

bolt_body = base.union(shank_solid)

# Add chamfer to top of shank
bolt_body = (
    bolt_body
    .edges(">Z")
    .chamfer(0.5)
)

# Add fillet between head and shank
bolt_body = (
    bolt_body
    .edges(cq.selectors.RadiusNthSelector(0))
    .fillet(0.8)
)

# Create thread groove profile
# We'll create a helix approximation by stacking rotated cuts
# Use a parametric approach with wire sweeping

# Create helical thread using points
def make_helix_thread(radius, pitch, height, thread_depth, n_points=120):
    """Create a helical wire"""
    import cadquery as cq
    from cadquery import Edge, Wire, Vertex
    import OCC.Core.BRepBuilderAPI as BRepBuilderAPI
    from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Circ
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
    from OCC.Core.GC import GC_MakeArcOfCircle
    from OCC.Core.BRep import BRep_Builder
    from OCC.Core.TopoDS import TopoDS_Wire
    
    points = []
    n = int(height / pitch * n_points)
    for i in range(n + 1):
        t = i / n
        angle = 2 * math.pi * (height / pitch) * t
        z = height * t + head_height
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y, z))
    return points

# Approximate threads with stacked torus cuts
result = bolt_body

# Create thread grooves by cutting torus shapes along the shank
for i in range(num_turns + 1):
    z_pos = head_height + i * thread_pitch + thread_pitch * 0.5
    if z_pos > head_height + shank_length - thread_pitch:
        break
    
    # Create a torus-like cut for thread groove
    groove = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(shank_diameter / 2 + 0.1)
        .workplane(offset=thread_pitch * 0.5)
        .circle(shank_diameter / 2 - thread_depth)
        .loft(combine=False)
    )
    
    groove2 = (
        cq.Workplane("XY")
        .workplane(offset=z_pos + thread_pitch * 0.5)
        .circle(shank_diameter / 2 - thread_depth)
        .workplane(offset=thread_pitch * 0.5)
        .circle(shank_diameter / 2 + 0.1)
        .loft(combine=False)
    )
    
    result = result.cut(groove).cut(groove2)