import cadquery as cq
import math

# Parameters
outer_radius = 40
inner_radius = 22
thickness = 8
gap_half_angle = 50  # degrees, the opening gap half-angle
hole_radius = 3
hole_offset = outer_radius - 8  # distance from center for mounting holes

# Create the C-shaped plate using extrusion of a 2D profile
# We'll build the profile using the Workplane sketch approach

# The C-shape: full annulus minus a wedge cutout on the right side
# Gap opens to the right (+X direction)
# Gap spans from -gap_half_angle to +gap_half_angle degrees

gap_angle_rad = math.radians(gap_half_angle)

# Create outer disk
outer = cq.Workplane("XY").circle(outer_radius).extrude(thickness)

# Create inner hole
inner_cut = cq.Workplane("XY").circle(inner_radius).extrude(thickness)

# Create the gap wedge - a box/extruded shape that cuts the opening
# The gap is centered on +X axis
# We need a wedge that removes the right side opening

# Build the gap as a polygon that covers the opening sector
# Points for the gap cutout (a pie slice + rectangle to ensure full cut)
gap_pts = [
    (0, 0),
    (outer_radius + 5, 0),
    (outer_radius + 5, (outer_radius + 5) * math.tan(gap_angle_rad)),
    (0, 0),
]

# Use a triangular/sector cut for the gap
# Create gap cutout as a wedge
p1x = (outer_radius + 5) * math.cos(math.radians(-gap_half_angle))
p1y = (outer_radius + 5) * math.sin(math.radians(-gap_half_angle))
p2x = (outer_radius + 5) * math.cos(math.radians(gap_half_angle))
p2y = (outer_radius + 5) * math.sin(math.radians(gap_half_angle))

gap_wire = [
    (0, 0),
    (p1x, p1y),
    (p2x, p2y),
]

gap_cut = (cq.Workplane("XY")
           .polyline(gap_wire)
           .close()
           .extrude(thickness))

# Combine: start with outer, subtract inner and gap
result = outer.cut(inner_cut).cut(gap_cut)

# Add mounting holes
# Holes are at approximately 45 degrees in each quadrant where material exists
# Top-right area and bottom-right area (near the gap edges), and left side
hole_positions = [
    # Upper left
    (-hole_offset * math.cos(math.radians(45)), hole_offset * math.sin(math.radians(45))),
    # Lower left  
    (-hole_offset * math.cos(math.radians(45)), -hole_offset * math.sin(math.radians(45))),
    # Upper right (near gap, but outside)
    (hole_offset * math.cos(math.radians(gap_half_angle - 15)), 
     hole_offset * math.sin(math.radians(gap_half_angle - 15))),
    # Lower right
    (hole_offset * math.cos(math.radians(gap_half_angle - 15)), 
     -hole_offset * math.sin(math.radians(gap_half_angle - 15))),
]

for (hx, hy) in hole_positions:
    hole = (cq.Workplane("XY")
            .transformed(offset=cq.Vector(hx, hy, 0))
            .circle(hole_radius)
            .extrude(thickness))
    result = result.cut(hole)