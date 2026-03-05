import cadquery as cq

# Create a bundle of 4 vertical rods/cylinders arranged in a 2x2 pattern
rod_radius = 3
rod_height = 200
spacing = 5

result = (
    cq.Workplane("XY")
    .cylinder(rod_height, rod_radius)
    .union(
        cq.Workplane("XY")
        .center(spacing, 0)
        .cylinder(rod_height, rod_radius)
    )
    .union(
        cq.Workplane("XY")
        .center(0, spacing)
        .cylinder(rod_height, rod_radius)
    )
    .union(
        cq.Workplane("XY")
        .center(spacing, spacing)
        .cylinder(rod_height, rod_radius)
    )
)