import cadquery as cq

# Dimensions based on image analysis
flange_diameter = 50
flange_thickness = 6

hub_diameter = 30
hub_length = 35

bore_diameter = 16

# Small tab/key on the outside of the hub
tab_width = 8
tab_height = 4
tab_length = 12

# Build the flange (large disk)
flange = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)

# Build the hub (cylinder extending from flange)
hub = (
    cq.Workplane("XY")
    .workplane(offset=flange_thickness)
    .circle(hub_diameter / 2)
    .extrude(hub_length)
)

# Combine flange and hub
body = flange.union(hub)

# Add a small rectangular tab/key on the side of the hub
# Tab sits on top of the hub cylinder
tab = (
    cq.Workplane("XY")
    .workplane(offset=flange_thickness + hub_length - tab_length)
    .center(hub_diameter / 2 - tab_height / 2 + tab_height, 0)
    .box(tab_height, tab_width, tab_length, centered=(True, True, False))
)

body = body.union(tab)

# Bore through the entire part (center hole)
body = (
    body
    .faces(">Z")
    .workplane()
    .circle(bore_diameter / 2)
    .cutThruAll()
)

result = body