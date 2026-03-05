import cadquery as cq

# Parameters
length_bot = 100.0
width_bot = 60.0
length_top = 90.0
width_top = 50.0
plate_thickness = 3.0
plate_spacing = 25.0

# Helper for rounded-front plate profile
def rounded_plate_profile(w, L):
    r = w/2.0
    flat = L/2.0 - r
    return (
        cq.Workplane("XY")
        .moveTo(-L/2.0, -w/2.0)
        .lineTo(flat, -w/2.0)
        .threePointArc((L/2.0, 0), (flat, w/2.0))
        .lineTo(-L/2.0, w/2.0)
        .close()
    )

# Bottom plate
bottom = (
    rounded_plate_profile(width_bot, length_bot)
    .extrude(plate_thickness)
)

# Top plate
top = (
    rounded_plate_profile(width_top, length_top)
    .extrude(plate_thickness)
    .translate((0, 0, plate_thickness + plate_spacing))
)

# Add cutouts and slots to top plate
top = (
    top.faces(">Z")
       .workplane()
       # Rectangular cutout
       .center(0, 0)
       .rect(20, 30)
       .cutBlind(-plate_thickness)
       # Two slots
       .center(0, 12)
       .rect(30, 3)
       .cutBlind(-plate_thickness)
       .center(0, -24)
       .rect(30, 3)
       .cutBlind(-plate_thickness)
       # Circular hole
       .center(20, 0)
       .circle(5)
       .cutBlind(-plate_thickness)
)

# Simple bracket as a rectangular block connecting plates at back
bracket_depth = 20.0
bracket = (
    cq.Workplane("XY")
      .box(bracket_depth, width_bot, plate_spacing)
      .translate((
          -length_bot/2.0 + bracket_depth/2.0,
          0,
          plate_thickness + plate_spacing/2.0
      ))
)

# Small mounting block on top plate
mount_block = (
    cq.Workplane("XY")
      .box(10, 10, 8)
      .translate((10, 10, plate_thickness + plate_spacing + 4))
)

# Combine all parts
result = bottom.union(top).union(bracket).union(mount_block)