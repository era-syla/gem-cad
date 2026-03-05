import cadquery as cq
import math

# Gear parameters
num_teeth = 48
outer_radius = 45.0
tooth_height = 4.0
gear_thickness = 6.0
inner_rim_radius = 35.0
hub_radius = 5.0
spoke_width = 3.5
num_spokes = 5

# Build the gear disc (outer rim)
# Start with a solid cylinder for the rim
gear = cq.Workplane("XY").circle(outer_radius).extrude(gear_thickness)

# Subtract the interior to create just the rim ring
gear = gear.cut(
    cq.Workplane("XY").circle(inner_rim_radius).extrude(gear_thickness)
)

# Add spokes
spoke_length = inner_rim_radius - hub_radius
spoke_solid = cq.Workplane("XY")
for i in range(num_spokes):
    angle = i * 360.0 / num_spokes
    angle_rad = math.radians(angle)
    cx = (hub_radius + spoke_length / 2.0) * math.cos(angle_rad)
    cy = (hub_radius + spoke_length / 2.0) * math.sin(angle_rad)
    spoke_box = (
        cq.Workplane("XY")
        .center(cx, cy)
        .rect(spoke_length, spoke_width)
        .extrude(gear_thickness)
    )
    # Rotate the spoke box around Z axis
    spoke_box = spoke_box.rotate((0, 0, 0), (0, 0, 1), angle)
    gear = gear.union(spoke_box)

# Add central hub
hub = cq.Workplane("XY").circle(hub_radius).extrude(gear_thickness)
gear = gear.union(hub)

# Add small center hole
center_hole = cq.Workplane("XY").circle(2.0).extrude(gear_thickness)
gear = gear.cut(center_hole)

# Now add teeth around the outer rim
# Each tooth is a small triangular/trapezoidal prism
tooth_pts = []
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    next_angle = (i + 1) * 360.0 / num_teeth
    mid_angle = (angle + next_angle) / 2.0

    angle_rad = math.radians(angle)
    next_angle_rad = math.radians(next_angle)
    mid_angle_rad = math.radians(mid_angle)

    # Base points at outer_radius
    half_span = math.radians(360.0 / num_teeth / 2.0) * 0.7
    p1x = outer_radius * math.cos(angle_rad + half_span * 0.1)
    p1y = outer_radius * math.sin(angle_rad + half_span * 0.1)
    p2x = outer_radius * math.cos(next_angle_rad - half_span * 0.1)
    p2y = outer_radius * math.sin(next_angle_rad - half_span * 0.1)

    # Tip point
    tip_r = outer_radius + tooth_height
    ptx = tip_r * math.cos(mid_angle_rad)
    pty = tip_r * math.sin(mid_angle_rad)

    tooth = (
        cq.Workplane("XY")
        .polyline([(p1x, p1y), (p2x, p2y), (ptx, pty)])
        .close()
        .extrude(gear_thickness)
    )
    gear = gear.union(tooth)

result = gear