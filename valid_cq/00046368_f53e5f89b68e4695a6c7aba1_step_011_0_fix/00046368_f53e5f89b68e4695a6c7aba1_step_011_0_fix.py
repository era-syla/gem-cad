import cadquery as cq

# Parameters
length = 120.0
width = 40.0
base_thickness = 6.0
rail_height = 5.0
rail_width = 6.0
groove_width = 4.0
groove_depth = 3.0
hole_diameter = 6.0
hole_positions = [(-40, 0), (-15, 0), (15, 0), (40, 0)]

# Base plate
result = cq.Workplane("XY").box(length, width, base_thickness)

# Add side rails
y_offset = (width - rail_width) / 2.0
result = result.faces(">Z").workplane().transformed(offset=(0, y_offset, 0)).rect(length, rail_width).extrude(rail_height)
result = result.faces(">Z").workplane().transformed(offset=(0, -y_offset, 0)).rect(length, rail_width).extrude(rail_height)

# Cut central groove
result = result.faces(">Z").workplane().rect(length, groove_width).cutBlind(-groove_depth)

# Drill through holes
wp = result.faces(">Z").workplane()
for x, y in hole_positions:
    wp = wp.pushPoints([(x, y)])
result = wp.circle(hole_diameter / 2.0).cutThruAll()

# Final result
result = result.clean()