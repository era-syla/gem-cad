import cadquery as cq

# Parameters
length = 60        # length of the top bar
bar_width = 10     # width of the top bar
bar_thickness = 5  # thickness of the top bar
rail_height = 2    # height of the center rail above the bar
rail_width = 3     # width of the center rail
leg_height = 20    # height of the legs
leg_thickness = 5  # thickness of the legs
hole_dia = 4       # diameter of mounting holes

# Build top bar with center rail
top = (
    cq.Workplane("XY")
    .rect(length, bar_width)
    .extrude(bar_thickness + rail_height)
)

# Cut grooves on either side of the center rail
groove_depth = rail_height
groove_width = (bar_width - rail_width) / 2
top = (
    top
    .faces(">Z")
    .workplane()
    .rect(length - 2, groove_width)
    .cutBlind(-groove_depth)
    .faces(">Z")
    .workplane()
    .rect(length - 2, groove_width)
    .cutBlind(-groove_depth)
)

# Build one leg profile and position two copies
leg = cq.Workplane("XY").rect(leg_thickness, bar_width).extrude(-leg_height)
leg1 = leg.translate(( length/2 - leg_thickness/2, 0, bar_thickness + rail_height))
leg2 = leg.translate((-length/2 + leg_thickness/2, 0, bar_thickness + rail_height))
legs = leg1.union(leg2)

# Drill vertical holes through legs
legs = (
    legs
    .faces(">Z")
    .workplane()
    .pushPoints([
        ( length/2 - leg_thickness/2, 0),
        (-length/2 + leg_thickness/2, 0),
    ])
    .hole(hole_dia, leg_height + 1)
)

# Combine top bar and legs
result = top.union(legs)