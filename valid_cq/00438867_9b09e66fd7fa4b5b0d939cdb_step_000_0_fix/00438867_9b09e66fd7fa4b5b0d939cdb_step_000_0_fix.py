import cadquery as cq
import math

outer_radius = 20
inner_radius = 15
thickness = 6
gap_angle = 30  # degrees

# Create full ring
ring = cq.Workplane("XY").circle(outer_radius).circle(inner_radius).extrude(thickness)

# Cut out the gap as a triangular wedge
half_gap = math.radians(gap_angle / 2)
cut_radius = outer_radius * 1.2
p0 = (0, 0)
p1 = (cut_radius * math.cos(half_gap), cut_radius * math.sin(half_gap))
p2 = (cut_radius * math.cos(-half_gap), cut_radius * math.sin(-half_gap))
wedge = cq.Workplane("XY").polyline([p0, p1, p2]).close().extrude(thickness)
ring = ring.cut(wedge)

# Create the tapered tab as a triangular prism
radial_width = outer_radius - inner_radius
tab_length = radial_width * 1.5
h = radial_width
tab_p1 = (outer_radius, -h/2)
tab_p2 = (outer_radius + tab_length, 0)
tab_p3 = (outer_radius, h/2)
tab = cq.Workplane("XY").polyline([tab_p1, tab_p2, tab_p3]).close().extrude(thickness)

result = ring.union(tab)