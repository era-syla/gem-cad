import cadquery as cq

# Parametric definitions for dimensions
disc_radius = 50.0
disc_thickness = 20.0

pin_radius = 2.5
pin_height = 12.0
pin_offset_x = 75.0      # Distance from disc center to pins
pin_spacing_y = 25.0     # Distance between the two pins

# Create the main large disc geometry
# Centered at the origin on the XY plane
main_disc = cq.Workplane("XY").circle(disc_radius).extrude(disc_thickness)

# Create the two smaller floating pins
# Defined by pushing two points to the right of the disc
pins = (
    cq.Workplane("XY")
    .pushPoints([
        (pin_offset_x, pin_spacing_y / 2.0),
        (pin_offset_x, -pin_spacing_y / 2.0)
    ])
    .circle(pin_radius)
    .extrude(pin_height)
)

# Combine the disc and pins into a single model
result = main_disc.union(pins)