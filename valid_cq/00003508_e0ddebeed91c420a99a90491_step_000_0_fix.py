import cadquery as cq
import math

# This looks like a headband/arch component with cylindrical pins at one end
# Parameters
outer_radius = 50
inner_radius = 42
band_width = 18
thickness = 4
arc_angle = 150  # degrees

# Create the main arch band using revolve
# The band is a curved rectangular cross-section revolved around an axis

# Build the arch as a swept solid
# Cross section of the band
def make_arch():
    # Create arch using loft along a path approach
    # Use revolve of a rectangular cross-section
    
    # The cross section rectangle
    w = band_width  # width of band
    t = thickness   # thickness
    
    # Create a 2D profile to revolve
    # The profile is in the XZ plane, offset from Z axis
    r_mid = (outer_radius + inner_radius) / 2  # 46
    r_half = (outer_radius - inner_radius) / 2  # 4
    
    # Profile: rectangle centered at r_mid from origin
    profile = (
        cq.Workplane("XZ")
        .transformed(offset=(r_mid, 0, 0))
        .rect(w, t)
    )
    
    # Revolve around Z axis by arc_angle degrees
    arch = profile.revolve(arc_angle, (0, 0, 0), (0, 0, 1))
    
    return arch

arch = make_arch()

# Now create the connector/pin end at the bottom
# Looking at the image, one end has two cylindrical pins with a connector bracket

# Get the end position of the arch
# At angle 0, the end is at (r_mid, 0, 0)
# At angle arc_angle, the end is at (r_mid*cos(150), r_mid*sin(150), 0)

r_mid = (outer_radius + inner_radius) / 2
angle_rad = math.radians(arc_angle)

# End point at angle=0 side (the pin end)
end_x = r_mid  # at angle 0
end_y = 0
end_z = 0

# Create the bracket/connector at angle=0 end
# Two small cylinders (pins) extending downward from the arch end

pin_radius = 2.5
pin_length = 8
pin_spacing = 5

# Create bracket plate connecting arch to pins
bracket = (
    cq.Workplane("XY")
    .transformed(offset=(end_x, 0, -thickness/2))
    .box(band_width * 0.6, thickness * 1.2, thickness * 1.5)
)

# Two pins
pin1 = (
    cq.Workplane("YZ")
    .transformed(offset=(0, pin_spacing/2, end_x - pin_length/2))
    .circle(pin_radius)
    .extrude(pin_length)
)

pin2 = (
    cq.Workplane("YZ")
    .transformed(offset=(0, -pin_spacing/2, end_x - pin_length/2))
    .circle(pin_radius)
    .extrude(pin_length)
)

# Connector block between pins
connector = (
    cq.Workplane("XY")
    .transformed(offset=(end_x - pin_length * 0.7, 0, -thickness * 2))
    .box(pin_length * 0.6, pin_spacing * 2.5, thickness * 0.8)
)

# Small cylinder pins at the very tip
tip_pin1 = (
    cq.Workplane("XY")
    .transformed(offset=(end_x - pin_length, pin_spacing, -thickness * 2.2))
    .circle(pin_radius * 0.9)
    .extrude(thickness * 0.5)
)

tip_pin2 = (
    cq.Workplane("XY")
    .transformed(offset=(end_x - pin_length, -pin_spacing, -thickness * 2.2))
    .circle(pin_radius * 0.9)
    .extrude(thickness * 0.5)
)

# Combine arch with bracket elements
result = arch.union(bracket).union(connector).union(tip_pin1).union(tip_pin2)

# Add edge fillets to smooth the arch
result = result.edges("|Z").fillet(1.0)