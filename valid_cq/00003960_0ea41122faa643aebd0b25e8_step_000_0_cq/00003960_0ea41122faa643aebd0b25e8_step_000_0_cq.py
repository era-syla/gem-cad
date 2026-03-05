import cadquery as cq

# Parametric dimensions
inner_diameter = 15.0     # Inner bore diameter
outer_diameter = 25.0     # Outer diameter of the shaft section
flange_diameter = 35.0    # Outer diameter of the flange
total_length = 30.0       # Overall length of the bushing
flange_thickness = 5.0    # Thickness of the flange

# Create the bushing geometry
# We will create this by revolving a profile or stacking cylinders.
# Stacking cylinders is often simpler and more readable in CadQuery for this shape.

# 1. Create the main shaft (outer diameter)
shaft = cq.Workplane("XY").circle(outer_diameter / 2).extrude(total_length)

# 2. Create the flange at the base
# We create a larger cylinder at the origin with the flange thickness
flange = cq.Workplane("XY").circle(flange_diameter / 2).extrude(flange_thickness)

# 3. Combine the shaft and flange
# Since both start at Z=0, the union will create the correct stepped outer shape.
solid = shaft.union(flange)

# 4. Create the through-hole (inner diameter)
# We cut a hole through the entire length of the combined solid.
result = solid.faces("<Z").workplane().hole(inner_diameter, depth=total_length)

# Alternative method (Profile Revolution - cleaner for complex profiles, but cylinders are fine here):
# result = (
#     cq.Workplane("XZ")
#     .lineTo(outer_diameter / 2, 0)
#     .lineTo(outer_diameter / 2, total_length - flange_thickness)
#     .lineTo(flange_diameter / 2, total_length - flange_thickness)
#     .lineTo(flange_diameter / 2, total_length)
#     .lineTo(inner_diameter / 2, total_length)
#     .lineTo(inner_diameter / 2, 0)
#     .close()
#     .revolve()
# )

# The variable 'result' now contains the final geometry.