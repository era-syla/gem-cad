import cadquery as cq

# Parametric dimensions
total_length = 220.0     # Total length of the propeller/bar
blade_width = 12.0       # Width of the blade section
blade_thickness = 2.0    # Thickness of the blade
hub_diameter = 16.0      # Outer diameter of the central hub
hub_height = 8.0         # Height of the hub cylinder
hole_diameter = 6.0      # Diameter of the central hole

# 1. Create the central Hub
# Create a cylinder centered at the origin.
# We extrude it and then translate it so its center is at Z=0.
hub = (
    cq.Workplane("XY")
    .circle(hub_diameter / 2.0)
    .extrude(hub_height)
    .translate((0, 0, -hub_height / 2.0))
)

# 2. Create the Blades
# We use a simple box centered at the origin to represent the two blades.
# The box defaults to centered=True, so it spans [-length/2, length/2] etc.
blade = cq.Workplane("XY").box(total_length, blade_width, blade_thickness)

# 3. Combine the geometries
# Union the blade and the hub into a single solid object.
result = hub.union(blade)

# 4. Create the central hole
# Select the top face of the geometry and cut a hole through the entire part.
result = result.faces(">Z").workplane().hole(hole_diameter)