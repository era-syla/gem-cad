import cadquery as cq
import math

# Parameters
box_size = 100
box_height = 90
wall_thickness = 12
cylinder_outer_r = 35
cylinder_inner_r = 28
cylinder_height = 50
sphere_r = 27
notch_size = 15  # size of corner notches at top

# Start with the main box
result = cq.Workplane("XY").box(box_size, box_size, box_height, centered=(True, True, False))

# Cut the top opening (inner cavity) - square pocket from top
cavity_size = box_size - 2 * wall_thickness
cavity_depth = box_height - wall_thickness

result = (result
    .faces(">Z")
    .workplane()
    .rect(cavity_size, cavity_size)
    .cutBlind(-cavity_depth)
)

# Add cylindrical wall inside the cavity
# First add a cylinder that sits on the bottom of the cavity
cyl_bottom_z = wall_thickness  # bottom of cavity
cyl_total_height = cylinder_height

# Cut a circular hole for the cylinder interior (sphere housing)
result = (result
    .workplane(offset=wall_thickness)
    .circle(cylinder_inner_r)
    .cutBlind(cylinder_height)
)

# Add the cylinder ring - we need to add material, so let's build it differently
# Create the box with cavity, then union a cylinder ring

# Build cylinder ring as separate solid
cyl_ring = (cq.Workplane("XY")
    .workplane(offset=wall_thickness)
    .circle(cylinder_outer_r)
    .circle(cylinder_inner_r)
    .extrude(cylinder_height)
)

# The sphere inside
sphere_solid = (cq.Workplane("XY")
    .workplane(offset=wall_thickness)
    .sphere(sphere_r)
)

# Actually let's rebuild cleanly
# Main solid box
box = cq.Workplane("XY").box(box_size, box_size, box_height, centered=(True, True, False))

# Cut square cavity from top
box = (box
    .faces(">Z")
    .workplane()
    .rect(box_size - 2*wall_thickness, box_size - 2*wall_thickness)
    .cutBlind(-(box_height - wall_thickness))
)

# Add cylinder ring on the floor of cavity
cyl_ring = (cq.Workplane("XY")
    .circle(cylinder_outer_r)
    .extrude(cylinder_height)
    .translate((0, 0, wall_thickness))
)

box = box.union(cyl_ring)

# Cut sphere from inside cylinder
sphere_obj = (cq.Workplane("XY")
    .workplane(offset=wall_thickness + sphere_r * 0.1)
    .sphere(sphere_r)
)

box = box.cut(sphere_obj)

# Cut corner notches at top (triangular cuts at 4 corners)
# These are the diagonal cuts visible at corners of top opening
notch_depth = box_height - wall_thickness
half = box_size / 2

for sx, sy in [(1,1), (-1,1), (1,-1), (-1,-1)]:
    # Triangular prism cut at each corner
    pts = [
        (sx * half, sy * half),
        (sx * (half - notch_size), sy * half),
        (sx * half, sy * (half - notch_size)),
    ]
    notch = (cq.Workplane("XY")
        .workplane(offset=wall_thickness)
        .polyline(pts)
        .close()
        .extrude(notch_depth)
    )
    box = box.cut(notch)

result = box