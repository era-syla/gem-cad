import cadquery as cq

# Dimensions
flange_diameter = 80
flange_thickness = 6
hub_diameter = 30
hub_height = 14
center_hole_diameter = 14
bolt_circle_diameter = 60
bolt_hole_diameter = 8
num_bolts = 6

# Base flange
result = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)

# Add hub on top of flange
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(hub_diameter / 2)
    .extrude(hub_height)
)

# Cut center hole through everything
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(center_hole_diameter / 2)
    .cutThruAll()
)

# Cut bolt holes in flange
result = (
    result
    .workplane(offset=-(hub_height + flange_thickness))
    .workplane(offset=flange_thickness)
    .polarArray(bolt_circle_diameter / 2, 0, 360, num_bolts)
    .circle(bolt_hole_diameter / 2)
    .cutThruAll()
)