import cadquery as cq

# Parametric dimensions
# Overall dimensions estimated based on visual proportions
head_diameter = 20.0
head_thickness = 4.0
shank_diameter = 12.0
shank_length = 5.0
hole_diameter = 6.0
fillet_radius = 2.0  # Radius for the rounded top edge

# Create the main body
# We start with the larger head cylinder
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_thickness)

# Add the fillet to the top edge of the head to create the rounded profile
# Selecting edges at the top face (Z-max)
head = head.edges(">Z").fillet(fillet_radius)

# Create the shank (smaller cylinder) underneath
# We workplane on the bottom face ("<Z") and extrude downwards
# Note: In CadQuery, extruding from a face usually adds material in the normal direction.
# Since we are on the bottom face (normal pointing down), a positive extrusion goes down.
shank = head.faces("<Z").workplane().circle(shank_diameter / 2).extrude(shank_length)

# Create the through-hole
# We select the top face and cut a hole all the way through
result = shank.faces(">Z").workplane().hole(hole_diameter)

# Alternative approach (Revolve) which might be cleaner for the profile, 
# but the constructive solid geometry (CSG) approach above is very readable.
# Let's stick with the CSG approach as it matches the standard workflow well.

# Final result variable as requested
result = result