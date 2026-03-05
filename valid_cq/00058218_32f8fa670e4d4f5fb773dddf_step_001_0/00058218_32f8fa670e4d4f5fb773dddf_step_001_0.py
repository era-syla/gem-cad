import cadquery as cq

# -- Model Parameters --
part_diameter = 100.0      # Overall outer diameter
part_thickness = 5.0       # Total thickness of the main disk
rim_width = 15.0           # Width of the outer rim
recess_depth = 2.5         # Depth of the central recess
pin_diameter = 6.0         # Diameter of the locating pins
pin_height = 2.0           # Height of the pins above the rim

# -- Derived Dimensions --
outer_radius = part_diameter / 2.0
inner_radius = outer_radius - rim_width
pin_radius = pin_diameter / 2.0
# Center the pins on the rim width
pin_orbit_radius = inner_radius + (rim_width / 2.0)

# -- Geometry Generation --

# 1. Create the base cylinder
result = cq.Workplane("XY").circle(outer_radius).extrude(part_thickness)

# 2. Cut the central recess
# Select the top face (>Z), create a workplane, draw the inner circle, 
# and cut blindly downwards.
result = (
    result.faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-recess_depth)
)

# 3. Add the alignment pins
# Select the new top face (the rim surface is the highest face >Z).
# Use polarArray to create two positions 180 degrees apart.
# 135 degrees is used as start angle to match the visual orientation in the image.
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=pin_orbit_radius, startAngle=135, angle=360, count=2)
    .circle(pin_radius)
    .extrude(pin_height)
)