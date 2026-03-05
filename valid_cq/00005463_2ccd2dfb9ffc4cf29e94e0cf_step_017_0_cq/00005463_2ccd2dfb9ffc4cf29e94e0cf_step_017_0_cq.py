import cadquery as cq

# Parametric definitions
outer_diameter = 50.0
inner_diameter = 25.0
thickness = 20.0
groove_radius = 4.0
num_grooves = 8

# Create the base cylinder
base = cq.Workplane("XY").circle(outer_diameter / 2).extrude(thickness)

# Create the center hole
base = base.faces(">Z").workplane().circle(inner_diameter / 2).cutThruAll()

# Create the grooves around the circumference
# We create one cutting cylinder and rotate it around the center
cutting_tool = (
    cq.Workplane("XY")
    .workplane(offset=thickness / 2)  # Center vertically
    .moveTo(outer_diameter / 2, 0)    # Move to the edge
    .circle(groove_radius)            # Profile of the groove
    .extrude(thickness * 1.5)         # Make it long enough to cut through
    .translate((0, 0, -thickness * 0.75)) # Adjust position to cut full height
)

# Subtract the grooves in a polar array pattern
for i in range(num_grooves):
    angle = i * (360.0 / num_grooves)
    # Rotate the cutting tool around the Z-axis
    rotated_tool = cutting_tool.rotate((0, 0, 0), (0, 0, 1), angle)
    base = base.cut(rotated_tool)

result = base