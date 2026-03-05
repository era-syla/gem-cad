import cadquery as cq

# Parameters
length_plate = 60
height_plate = 40
thickness_plate = 4
base_width = 10
base_thickness = 4
base_length = length_plate + 30
hole_flat = 5
boss_radius = 3
boss_length = base_width

# Build base
result = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Build vertical plate on top of base
result = result.faces(">Z").workplane().box(length_plate, thickness_plate, height_plate)

# Cut hexagonal holes through the plate
result = (
    result.faces(">Y")
          .workplane(centerOption="CenterOfMass")
          .pushPoints([(-15, 10), (15, 10), (-15, -10), (15, -10)])
          .polygon(6, hole_flat)
          .cutThruAll()
)

# Add half-cylindrical bosses on ends of the base (alternating sides)
result = (
    result.faces("<Y")
          .workplane()
          .center(-base_length/2, 0)
          .circle(boss_radius)
          .extrude(boss_length)
)
result = (
    result.faces(">Y")
          .workplane()
          .center( base_length/2, 0)
          .circle(boss_radius)
          .extrude(boss_length)
)