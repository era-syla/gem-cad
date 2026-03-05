import cadquery as cq
import math

# Parameters
outer_radius = 35
wall_thickness = 3
height = 60
opening_angle = 120  # degrees of opening at the front

# Create the main cup holder body
# It's a partial cylinder (like a C-shape) with a curved bottom

# Create outer cylinder shell
outer_cyl = cq.Workplane("XY").cylinder(height, outer_radius)
inner_radius = outer_radius - wall_thickness
inner_cyl = cq.Workplane("XY").cylinder(height + 2, inner_radius)

# Subtract inner from outer to get shell
shell = outer_cyl.cut(inner_cyl)

# Cut the front opening - a wedge to create the C-shape
# The opening is in the front (positive X direction)
half_angle = opening_angle / 2.0
cut_size = outer_radius * 3

# Create a cutting box for the front opening
# Opening faces the front, so we cut a sector
cut_wedge = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -height))
    .polygon(3, cut_size * 2)
    .extrude(height * 3)
)

# Use a simpler approach: cut with a box at front
front_cut = (
    cq.Workplane("XY")
    .box(outer_radius * 2 + 10, outer_radius * 2 + 10, height * 3)
    .translate((outer_radius + 5, 0, 0))
)

# Actually let's build the cross-section profile and extrude
# The cross section is a C-shape arc

# Build using wire approach
half_open_rad = math.radians(opening_angle / 2)

# The C-shape: arc from -half_open_rad to half_open_rad on the outer circle
# going the long way around (the back)

result_shell = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -height/2))
)

# Create a solid C-shaped body using revolve approach won't work easily
# Let's use extrude of a 2D C-profile

# Build 2D profile of C-shape cross section
ang_start = math.degrees(half_open_rad)  # e.g. 60 degrees
ang_end = 360 - math.degrees(half_open_rad)  # e.g. 300 degrees

# Create the C-shape as a face by building it with edges
# Outer arc from ang_start to ang_end (going counterclockwise = the back)
# Inner arc from ang_end back to ang_start

outer_r = outer_radius
inner_r = inner_radius

# Points on outer arc
p1_out = (outer_r * math.cos(math.radians(ang_start)), outer_r * math.sin(math.radians(ang_start)))
p2_out = (outer_r * math.cos(math.radians(ang_end)), outer_r * math.sin(math.radians(ang_end)))
p1_in = (inner_r * math.cos(math.radians(ang_start)), inner_r * math.sin(math.radians(ang_start)))
p2_in = (inner_r * math.cos(math.radians(ang_end)), inner_r * math.sin(math.radians(ang_end)))

# Create C-shape profile
c_profile = (
    cq.Workplane("XY")
    .moveTo(*p1_out)
    .threePointArc((0, -outer_r), p2_out)  # back arc (going through bottom)
    .lineTo(*p2_in)
    .threePointArc((0, -inner_r), p1_in)
    .close()
    .extrude(height)
)

# Add bottom plate with organic shape
bottom = (
    cq.Workplane("XY")
    .moveTo(*p1_out)
    .threePointArc((0, -outer_r), p2_out)
    .lineTo(*p2_in)
    .threePointArc((0, -inner_r), p1_in)
    .close()
    .extrude(wall_thickness)
)

body = c_profile.union(bottom.translate((0, 0, -wall_thickness)))

# Add a small ring/loop on the left side for hanging
loop_pos_x = inner_r * math.cos(math.radians(180))
loop_pos_y = inner_r * math.sin(math.radians(180))

ring_outer = 6
ring_inner = 4
ring_height = wall_thickness

loop = (
    cq.Workplane("YZ")
    .transformed(offset=(loop_pos_y, height * 0.4, loop_pos_x))
    .circle(ring_outer)
    .extrude(ring_height * 2)
    .cut(
        cq.Workplane("YZ")
        .transformed(offset=(loop_pos_y, height * 0.4, loop_pos_x))
        .circle(ring_inner)
        .extrude(ring_height * 2 + 2)
    )
)

result = body.union(loop)