import cadquery as cq

# Parametric dimensions
base_diameter = 50.0
base_height = 25.0

hex_flat_size = 28.0  # Distance flat-to-flat (approximate)
hex_height = 10.0

top_cyl_diameter = 20.0
top_cyl_height = 10.0

bore_diameter = 12.0

side_hole_diameter = 8.0
side_hole_position_z = 12.5  # Roughly halfway up the base

# 1. Create the Base Cylinder
result = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_height)

# 2. Create the Hexagonal Section
# CadQuery's polygon method uses the circumscribed radius or side count.
# For a hex, to get a specific flat-to-flat distance (d), the radius (r) is d / sqrt(3).
# We create a new workplane on top of the base.
result = result.faces(">Z").workplane().polygon(6, hex_flat_size / 0.866025).extrude(hex_height)

# 3. Create the Top Cylinder
result = result.faces(">Z").workplane().circle(top_cyl_diameter / 2.0).extrude(top_cyl_height)

# 4. Create the Through Bore (Vertical Hole)
# Cut through the entire stack
result = result.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

# 5. Create the Side Hole
# Create a workplane on the XZ plane (side view), move it to the correct height, and cut
# The hole goes through the center of the base cylinder.
result = result.faces(">Y").workplane(centerOption="CenterOfMass").center(0, -base_height/2 + side_hole_position_z).circle(side_hole_diameter/2).cutThruAll()

# Alternative robust way to place side hole if orientation matters relative to hex:
# result = result.workplane("XZ").center(0, side_hole_position_z).circle(side_hole_diameter / 2.0).cutThruAll()