import cadquery as cq
import math

# Parameters
bottom_radius = 30
top_radius = 45
height = 50
wall_thickness = 2.5
ring_thickness = 4
ring_height = 5
num_vertical_ribs = 12
num_horizontal_rings = 3
rib_width = 3

# Build the basket as a tapered shell with ribs

# Helper: radius at given height z (linear taper)
def radius_at_z(z):
    return bottom_radius + (top_radius - bottom_radius) * (z / height)

# Create the outer tapered shell (thin wall)
# We'll build it by revolving a profile, then cut slots

# Create outer cone frustum
outer_shell = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .add(
        cq.Solid.makeCone(bottom_radius, top_radius, height)
    )
)

# Create inner cone frustum (slightly smaller)
inner_r_bottom = bottom_radius - wall_thickness
inner_r_top = top_radius - wall_thickness

inner_cone = cq.Solid.makeCone(inner_r_bottom, inner_r_top, height)

# Shell = outer - inner
shell = (
    cq.Workplane("XY")
    .add(cq.Solid.makeCone(bottom_radius, top_radius, height))
    .cut(cq.Workplane("XY").add(inner_cone).val())
)

# Add bottom disk
bottom_disk = (
    cq.Workplane("XY")
    .circle(bottom_radius)
    .extrude(wall_thickness)
)

# Add top ring
top_ring = (
    cq.Workplane("XY")
    .workplane(offset=height - ring_height)
    .circle(top_radius + ring_thickness)
    .circle(top_radius - wall_thickness)
    .extrude(ring_height)
)

# Combine shell + bottom + top ring
result = shell.union(bottom_disk).union(top_ring)

# Cut vertical slot openings between ribs
# Each slot is an angular sector cut through the shell
angle_step = 360.0 / num_vertical_ribs
rib_half_angle = math.degrees(math.atan2(rib_width / 2, (bottom_radius + top_radius) / 2))
slot_angle = angle_step - rib_half_angle * 2

# Height bands for horizontal rings
ring_positions = []
band_height = (height - wall_thickness) / (num_horizontal_rings + 1)
for i in range(1, num_horizontal_rings + 1):
    ring_positions.append(i * band_height)

# Cut vertical slots (openings between vertical ribs)
for i in range(num_vertical_ribs):
    angle_center = i * angle_step
    angle_start = angle_center + rib_half_angle
    slot_ang = slot_angle
    if slot_ang <= 0:
        continue
    
    # Create a cutting wedge that removes material between ribs
    # Use a box approach rotated
    mid_r = (bottom_radius + top_radius) / 2 + 5
    slot_width_at_mid = 2 * mid_r * math.sin(math.radians(slot_ang / 2))
    
    # Build cutter as extruded arc segment
    cutter = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle_start + slot_ang / 2))
        .rect(slot_width_at_mid * 0.85, mid_r * 2.5)
        .extrude(height * 1.5)
        .translate((0, 0, -height * 0.1))
    )
    
    # Only cut the shell portion (not the ribs), leave horizontal bands
    # Cut each vertical slot region but leave horizontal ring strips
    slot_start_z = wall_thickness
    
    # Cut segments between horizontal rings
    ring_z = [wall_thickness] + ring_positions + [height - ring_height]
    for j in range(len(ring_z) - 1):
        z_lo = ring_z[j] + rib_width / 2
        z_hi = ring_z[j + 1] - rib_width / 2
        if z_hi <= z_lo:
            continue
        seg_height = z_hi - z_lo
        
        seg_cutter = (
            cq.Workplane("XY")
            .workplane(offset=z_lo)
            .transformed(rotate=(0, 0, angle_start + slot_ang / 2))
            .rect(slot_width_at_mid * 0.85, mid_r * 2.5)
            .extrude(seg_height)
        )
        result = result.cut(seg_cutter)