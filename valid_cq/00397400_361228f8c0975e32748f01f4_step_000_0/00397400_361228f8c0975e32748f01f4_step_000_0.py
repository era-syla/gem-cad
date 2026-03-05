import cadquery as cq

# Parametric dimensions
height = 100.0       # Total length of the beam
width = 10.0         # Overall width of the cross section
thickness = 1.2      # Thickness of the walls

# Create the first solid component: A plate oriented along the X-axis
# box() creates a centered solid by default
plate_x = cq.Workplane("XY").box(width, thickness, height)

# Create the second solid component: A plate oriented along the Y-axis
plate_y = cq.Workplane("XY").box(thickness, width, height)

# Combine the two intersecting plates to form the cross/cruciform shape
result = plate_x.union(plate_y)