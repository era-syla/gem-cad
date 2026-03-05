import cadquery as cq

# Parameters
front_flat = 20
arc_length = 30
back_flat = 20
width = 40
base_h = 10
arc_h = 5
rod_radius = 1.5
rod_diameter = rod_radius * 2

total_length = front_flat + arc_length + back_flat

# Build main body with arced roof
result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (total_length, 0),
        (total_length, base_h),
        (front_flat + arc_length, base_h),
        (front_flat + arc_length/2, base_h + arc_h),
        (front_flat, base_h),
        (0, base_h),
    ])
    .close()
    .extrude(width)
)

# Add two rods on the back flat region
rod_positions_x = [
    front_flat + arc_length + back_flat * 0.25,
    front_flat + arc_length + back_flat * 0.75,
]
for x in rod_positions_x:
    rod = (
        cq.Workplane("XZ")
        .transformed(offset=(x, 0, base_h + rod_radius))
        .cylinder(width, rod_radius)
    )
    result = result.union(rod)

# Emboss text on the front face
result = (
    result
    .faces("<X")
    .workplane(centerOption="CenterOfMass")
    .text("UNSLATE", 8, 1)
)

# Add a side pivot on the right side face
pivot = (
    cq.Workplane("YZ")
    .transformed(offset=(total_length, width/2, base_h/2))
    .circle(2)
    .extrude(4)
)
result = result.union(pivot)