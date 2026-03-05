import cadquery as cq

# Parameters
outer_radius = 50
inner_radius = 35
height = 20
small_hole_radius = 3
small_hole_depth = 15

# Create the main ring (annular cylinder)
result = (
    cq.Workplane("XY")
    .cylinder(height, outer_radius)
    .cut(
        cq.Workplane("XY")
        .cylinder(height + 2, inner_radius)
    )
)

# Add small holes on the side (radial holes) at 180 degrees apart
# First hole
hole1 = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, -height/4, 0))
    .circle(small_hole_radius)
    .extrude(outer_radius - inner_radius + 5)
)

# Create radial holes using transformed workplanes
mid_radius = (outer_radius + inner_radius) / 2

# Hole 1 at 0 degrees
hole_cutter1 = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, -(height/2 - height/4), outer_radius))
    .circle(small_hole_radius)
    .extrude(outer_radius - inner_radius + 2)
)

# Build the ring first
ring = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# Add small radial holes on the outer wall
# Position holes at the mid-height, at 0 and 180 degrees
hole_depth = outer_radius - inner_radius + 2

# Hole at angle 0 (positive X direction)
cutter1 = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, height/4, 0))
    .circle(small_hole_radius)
    .extrude(hole_depth)
    .translate((-outer_radius, 0, 0))
)

# Hole at angle 180 (negative X direction)
cutter2 = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, height/4, 0))
    .circle(small_hole_radius)
    .extrude(hole_depth)
    .translate((inner_radius - 2, 0, 0))
)

# Use shell-based approach with direct CadQuery operations
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# Cut radial holes from the side
# Hole 1: along X axis
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=-outer_radius)
    .transformed(offset=cq.Vector(0, height/4, 0))
    .circle(small_hole_radius)
    .extrude(outer_radius - inner_radius + 1)
)

# Hole 2: opposite side along X axis
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=inner_radius - 1)
    .transformed(offset=cq.Vector(0, height/4, 0))
    .circle(small_hole_radius)
    .extrude(outer_radius - inner_radius + 1)
)