import cadquery as cq
import math

# Parameters
outer_radius = 50
inner_radius = 40
ring_height = 8
fin_height = 45
fin_width = 8
gap_angle = 30  # degrees gap in the ring

# Create the main ring (partial torus/ring shape)
# Ring is mostly complete with a gap at the top

# Create outer cylinder
outer = cq.Workplane("XY").circle(outer_radius).extrude(ring_height)
# Create inner cylinder to subtract
inner = cq.Workplane("XY").circle(inner_radius).extrude(ring_height)
# Subtract to make ring
ring = outer.cut(inner)

# Cut a gap in the ring
gap_half = gap_angle / 2
# Create a box to cut the gap
gap_cutter = (cq.Workplane("XY")
    .transformed(rotate=cq.Vector(0, 0, 90 - gap_half))
    .box(outer_radius * 2 + 10, outer_radius * 2 + 10, ring_height + 2, centered=True)
)

# Actually use a wedge/sector approach for the gap
# Create a sector to cut out the gap at the top (around 270 degrees)
# Gap is at the top (90 degrees position)
gap_angle_rad = math.radians(gap_angle)

# Create the gap cutter as a 2D sector
def make_sector(radius, start_angle, end_angle, height):
    """Make a solid sector (pie slice)"""
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    pts = [(0, 0)]
    n_pts = 20
    for i in range(n_pts + 1):
        angle = start_rad + (end_rad - start_rad) * i / n_pts
        pts.append((radius * math.cos(angle), radius * math.sin(angle)))
    pts.append((0, 0))
    
    return (cq.Workplane("XY")
            .polyline(pts)
            .close()
            .extrude(height))

# Gap at top (around 90 degrees), gap_angle degrees wide
gap_sector = make_sector(outer_radius + 5, 90 - gap_half, 90 + gap_half, ring_height + 4)
gap_sector = gap_sector.translate((0, 0, -2))

ring = ring.cut(gap_sector)

# Now create two fins/triangular supports
# Fins are on either side of the gap, rising up
def make_fin(angle_deg):
    """Create a triangular fin at given angle"""
    angle_rad = math.radians(angle_deg)
    
    # Fin base is at the ring outer edge, pointing outward and upward
    # Base width = fin_width, located at angle_deg
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Fin profile: triangle in the radial-vertical plane
    # Base: from inner to outer radius at ring top
    # Apex: at outer radius + some extension, at fin_height
    
    r_mid = (outer_radius + inner_radius) / 2
    
    # Create fin as a loft or extrusion
    # Simple approach: create a triangular prism
    half_w = fin_width / 2
    
    # Points for the fin triangle in local coordinates
    # Bottom base at ring top surface
    p1 = cq.Vector(-half_w, inner_radius, ring_height)
    p2 = cq.Vector(half_w, inner_radius, ring_height)
    p3 = cq.Vector(half_w, outer_radius, ring_height)
    p4 = cq.Vector(-half_w, outer_radius, ring_height)
    # Top apex
    p5 = cq.Vector(0, outer_radius, ring_height + fin_height)
    
    pts_bottom = [(-half_w, inner_radius), (half_w, inner_radius), 
                  (half_w, outer_radius), (-half_w, outer_radius)]
    
    fin = (cq.Workplane("XY")
           .workplane(offset=ring_height)
           .polyline([(-half_w, inner_radius), (half_w, inner_radius), 
                      (half_w, outer_radius), (-half_w, outer_radius)])
           .close()
           .extrude(1))
    
    # Better: make triangular fin using vertices
    # Create as a shell of faces
    fin = (cq.Workplane("XY")
           .workplane(offset=ring_height)
           .rect(fin_width, outer_radius - inner_radius, centered=True)
           .workplane(offset=fin_height)
           .rect(1, 1, centered=True)
           .loft())
    
    fin = fin.translate((0, (outer_radius + inner_radius) / 2, 0))
    
    # Rotate to angle
    fin = fin.rotate((0, 0, 0), (0, 0, 1), angle_deg - 90)
    
    return fin

# Fins at sides of gap
fin_left = make_fin(90 - gap_half)
fin_right = make_fin(90 + gap_half)

# Also create a large back fin/wing
back_fin_angle = 270  # opposite to gap
angle_rad = math.radians(back_fin_angle)

# Large triangular wing spanning most of the back
wing = (cq.Workplane("XY")
        .workplane(offset=ring_height)
        .polyline([(-outer_radius * 0.8, 0), (outer_radius * 0.8, 0),
                   (0, outer_radius * 0.7)])
        .close()
        .extrude(fin_height * 0.8))

wing = wing.rotate((0, 0, 0), (0, 0, 1), 180)
wing = wing.translate((0, 0, 0))

# Combine all parts
result = ring.union(fin_left).union(fin_right)