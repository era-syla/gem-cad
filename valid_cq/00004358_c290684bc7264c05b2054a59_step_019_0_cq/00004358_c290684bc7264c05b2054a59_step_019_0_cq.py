import cadquery as cq

# Parametric dimensions
height = 100.0   # Total length of the tube
outer_diameter = 40.0 # Outer diameter of the tube
wall_thickness = 5.0  # Thickness of the tube wall

# Calculated dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
inner_diameter = inner_radius * 2.0

# Create the hollow cylinder (tube)
# We create a solid cylinder first
result = cq.Workplane("XY").circle(outer_radius).extrude(height)

# Then we cut the inner hole
result = result.faces(">Z").workplane().hole(inner_diameter)

# Alternatively, a more direct way to make a tube:
# result = cq.Workplane("XY").circle(outer_radius).circle(inner_radius).extrude(height)

# Export the result for verification (optional in script, but 'result' variable is required)
# show_object(result)