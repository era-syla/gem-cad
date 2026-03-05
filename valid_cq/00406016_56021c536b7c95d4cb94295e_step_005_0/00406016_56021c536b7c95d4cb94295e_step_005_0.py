import cadquery as cq

# Parametric dimensions
outer_radius = 25.0
height = 120.0
thickness = 3.0
cut_angle = 25.0
cut_z_pos = 90.0  # Vertical position where the cut plane intersects the Z-axis

# Create the base hollow cylinder (tube)
# We extrude it taller than the final height to ensure the cut is clean
tube_outer = cq.Workplane("XY").circle(outer_radius).extrude(height)
tube_inner = cq.Workplane("XY").circle(outer_radius - thickness).extrude(height)
base_tube = tube_outer.cut(tube_inner)

# Create a cutting tool (a box oriented at an angle) to slice the top
# We create a workplane at the cut height, rotate it by the cut angle,
# and define a box that extends upwards (local Z) from that plane.
cutter = (
    cq.Workplane("XY")
    .workplane(offset=cut_z_pos)
    .transformed(rotate=cq.Vector(cut_angle, 0, 0))
    .box(outer_radius * 4, outer_radius * 4, height, centered=(True, True, False))
)

# Subtract the cutting tool from the base tube to create the slanted top
result = base_tube.cut(cutter)