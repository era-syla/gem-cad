import cadquery as cq
import math

# Chainring parameters
num_teeth = 32
outer_radius = 47.0
inner_radius = 35.0
tooth_height = 4.0
tooth_width_base = 3.5
tooth_width_tip = 2.0
ring_thickness = 3.5
pitch_radius = (outer_radius + inner_radius) / 2.0

# Build the base ring as a 2D profile, then extrude
# We'll create the ring with teeth using a polar pattern approach

# First create the base annular ring profile
base_ring = (
    cq.Workplane("XY")
    .circle(outer_radius - tooth_height)
    .circle(inner_radius)
    .extrude(ring_thickness)
)

# Create tooth profile
def make_tooth(angle_deg):
    angle_rad = math.radians(angle_deg)
    
    # Tooth center position on pitch circle
    cx = (outer_radius - tooth_height/2) * math.cos(angle_rad)
    cy = (outer_radius - tooth_height/2) * math.sin(angle_rad)
    
    # Tooth oriented radially
    # Half angular width
    r_outer = outer_radius
    r_base = outer_radius - tooth_height
    
    half_tip = tooth_width_tip / 2.0
    half_base = tooth_width_base / 2.0
    
    # Points of tooth trapezoid in local coords, then rotate
    # Local: x = radial, y = tangential
    def rot(px, py):
        rx = px * math.cos(angle_rad) - py * math.sin(angle_rad)
        ry = px * math.sin(angle_rad) + py * math.cos(angle_rad)
        return (rx, ry)
    
    p1 = rot(r_base, -half_base)
    p2 = rot(r_base, half_base)
    p3 = rot(r_outer, half_tip)
    p4 = rot(r_outer, -half_tip)
    
    tooth = (
        cq.Workplane("XY")
        .polyline([p1, p2, p3, p4])
        .close()
        .extrude(ring_thickness)
    )
    return tooth

# Build teeth
teeth_solid = None
for i in range(num_teeth):
    angle = i * (360.0 / num_teeth)
    t = make_tooth(angle)
    if teeth_solid is None:
        teeth_solid = t
    else:
        teeth_solid = teeth_solid.union(t)

# Combine base ring with teeth
chainring = base_ring.union(teeth_solid)

# Now cut lightening holes between teeth
# Holes positioned at mid-radius, between teeth
hole_radius_pos = (outer_radius - tooth_height + inner_radius) / 2.0 + 2.0
hole_size_r = 2.8  # radial extent
hole_size_t = 4.0  # tangential extent

lightening = cq.Workplane("XY")
for i in range(num_teeth):
    angle = (i + 0.5) * (360.0 / num_teeth)
    angle_rad = math.radians(angle)
    
    cx = hole_radius_pos * math.cos(angle_rad)
    cy = hole_radius_pos * math.sin(angle_rad)
    
    # Create elongated hole (ellipse approximated by a box rotated)
    # Use a rotated rectangle
    hole = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(cx, cy, 0), rotate=cq.Vector(0, 0, angle))
        .rect(hole_size_r * 1.5, hole_size_t)
        .extrude(ring_thickness + 1)
    )
    chainring = chainring.cut(hole)

# Add slight chamfer to top edges of teeth for realism
# Apply fillet to the overall outer top edges
try:
    chainring = chainring.edges("|Z").fillet(0.3)
except:
    pass

result = chainring