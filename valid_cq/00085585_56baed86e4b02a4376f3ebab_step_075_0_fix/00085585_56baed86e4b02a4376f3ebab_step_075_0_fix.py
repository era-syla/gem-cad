import cadquery as cq

# Parameters
plate_length = 80
plate_width = 20
plate_th = 2
plate_radius = plate_width / 2
hole_diam = 8
slot_length = 10
slot_width = 5

chan_length = 40
chan_width = 16
wall_th = 2
chan_height = 15

# Build top plate with semicircular ends
# Central rectangular portion
plate = (cq.Workplane("XY")
    .rect(plate_length - 2 * plate_radius, plate_width)
    .extrude(plate_th)
)
# Left semicircle
plate = plate.union(
    cq.Workplane("XY")
      .center(-plate_length/2 + plate_radius, 0)
      .circle(plate_radius)
      .extrude(plate_th)
)
# Right semicircle
plate = plate.union(
    cq.Workplane("XY")
      .center(plate_length/2 - plate_radius, 0)
      .circle(plate_radius)
      .extrude(plate_th)
)

# Holes at the ends
plate = (plate.faces(">Z")
    .workplane()
    .pushPoints([
        (-plate_length/2 + plate_radius, 0),
        ( plate_length/2 - plate_radius, 0)
    ])
    .hole(hole_diam)
)

# Center slot
plate = (plate.faces(">Z")
    .workplane()
    .rect(slot_length, slot_width)
    .cutThruAll()
)

# Build channel under the plate
chan_outer = (cq.Workplane("XY")
    .rect(chan_length, chan_width)
    .extrude(-chan_height)
)
chan_inner = (cq.Workplane("XY")
    .rect(chan_length - 2 * wall_th, chan_width - 2 * wall_th)
    .extrude(-chan_height)
)
channel = chan_outer.cut(chan_inner)

# Combine plate and channel
result = plate.union(channel)