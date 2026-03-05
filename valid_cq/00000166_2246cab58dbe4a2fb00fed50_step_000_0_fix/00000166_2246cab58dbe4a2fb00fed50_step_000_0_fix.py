import cadquery as cq
import math

# Parameters
base_w = 80
base_d = 80
base_h = 10

stem_w = 20
stem_d = 20
stem_h = 40

top_radius = 70
top_angle = 90  # degrees (quarter circle fan shape)
top_h = 12

# Build the base (rectangular slab)
base = cq.Workplane("XY").rect(base_w, base_d).extrude(base_h)

# Build the stem (rectangular column on top of base)
stem = (cq.Workplane("XY")
        .workplane(offset=base_h)
        .rect(stem_w, stem_d)
        .extrude(stem_h))

# Build the fan-shaped top
# Quarter circle fan: from 0 to 90 degrees, radius = top_radius
# Center at origin, fan in the +X, +Y quadrant
# The fan top sits on top of the stem

top_z = base_h + stem_h

def make_fan_top(radius, angle_deg, height, z_offset):
    # Create a fan/sector shape
    # Points: origin, arc from 0 to angle_deg
    angle_rad = math.radians(angle_deg)
    
    # Create sector wire
    # Start at origin, line to (radius, 0), arc to (radius*cos(angle), radius*sin(angle)), line back to origin
    pts = [(0, 0)]
    
    # Add points along the arc
    n_pts = 20
    arc_pts = []
    for i in range(n_pts + 1):
        a = math.radians(angle_deg * i / n_pts)
        arc_pts.append((radius * math.cos(a), radius * math.sin(a)))
    
    # Build the sector as a closed wire
    result = (cq.Workplane("XY")
              .workplane(offset=z_offset)
              .moveTo(0, 0)
              .lineTo(arc_pts[0][0], arc_pts[0][1])
              .spline(arc_pts[1:])
              .lineTo(0, 0)
              .close()
              .extrude(height))
    return result

# Use a different approach: create the fan using a 2D polygon approximation
def make_sector(radius, angle_deg, height, z_offset):
    n = 30
    pts = [(0, 0)]
    for i in range(n + 1):
        a = math.radians(angle_deg * i / n)
        pts.append((radius * math.cos(a), radius * math.sin(a)))
    pts.append((0, 0))
    
    # Use Workplane polygon approach via wire
    wp = cq.Workplane("XY").workplane(offset=z_offset)
    wp = wp.polyline(pts).close().extrude(height)
    return wp

fan_top = make_sector(top_radius, top_angle, top_h, top_z)

# Center the fan: currently it's in +X+Y quadrant centered at origin
# We want it centered over the stem which is at origin
# Rotate fan by -45 degrees to center it symmetrically
fan_top = fan_top.rotate((0, 0, 0), (0, 0, 1), -45)

# Combine all parts
result = base.union(stem).union(fan_top)

# Add fillets to the base edges (top edges of base where it meets stem area)
# Add chamfer/fillet to top fan edges
try:
    result = result.edges("|Z").fillet(3)
except:
    pass