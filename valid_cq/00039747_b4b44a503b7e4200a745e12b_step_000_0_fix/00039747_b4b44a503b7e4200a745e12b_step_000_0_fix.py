import cadquery as cq

# Parameters
band_radius = 50
band_width = 6
band_thickness = 1.5

plate_length = 70
plate_thickness = 10
plate_height = 10

screw_dia = 4
screw_length = plate_thickness + 4

# Create the band by revolving a rectangular profile around the Y-axis
band_profile = (
    cq.Workplane("XZ")
    .moveTo(band_radius, -band_width/2)
    .lineTo(band_radius + band_thickness, -band_width/2)
    .lineTo(band_radius + band_thickness, band_width/2)
    .lineTo(band_radius, band_width/2)
    .close()
)
ring = band_profile.revolve(360, axisStart=(0,0,0), axisEnd=(0,1,0))

# Create the mounting plate and position it under the band
plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_thickness, plate_height)
    .translate((0, 0, -(band_width/2 + plate_height/2)))
)

# Create a simple screw through the plate
screw = (
    cq.Workplane("ZX")
    .transformed(offset=(0, -plate_thickness/2, 0))
    .circle(screw_dia/2)
    .extrude(screw_length)
)

# Combine all parts
result = ring.union(plate).union(screw)