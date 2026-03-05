import cadquery as cq

# Parametric dimensions
height = 60.0          # Total height of the cup/container
outer_diameter = 50.0  # Approximate outer diameter (flat-to-flat or corner-to-corner)
wall_thickness = 4.0   # Thickness of the walls
polygon_sides = 12     # Number of sides for the polygonal exterior (Dodecagon)

# Calculate inner radius based on outer dimension and wall thickness
# Assuming outer_diameter is the diameter of the circumscribed circle for the polygon
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the base shape
# 1. Create a polygon for the outer profile extruded to height
result = (
    cq.Workplane("XY")
    .polygon(polygon_sides, outer_diameter)
    .extrude(height)
)

# 2. Create the circular inner cut (the hole)
# We want a cylindrical hole, but leaving a bottom thickness
bottom_thickness = 3.0
cut_depth = height - bottom_thickness

result = (
    result.faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-cut_depth)
)

# 3. Add the top rim detail
# The image shows a small step or lip at the top rim. 
# It looks like the polygonal shape stops slightly below the top, 
# and a circular rim continues, or there is a chamfer/fillet.
# Looking closely, there is a circular ring on the top face.
# Let's add a small chamfer to the inner edge and outer edge of the top face for a nicer look,
# or simply model the rim as depicted which seems to be the polygon transitioning to a circle or just a flat face.
# The image actually shows the polygon outer shape going all the way up.
# Inside, there is a smooth cylindrical bore.
# On the top face, there is a distinct ring. This is likely just the flat top face of the wall.
# However, there is a faint line indicating a small recess or a lip.
# Let's add a small chamfer to the top inner edge to match the smooth entry look.
result = result.edges(">Z and (not %CIRCLE)").fillet(0.5) # Slight rounding of top outer polygon edges if desired, or skip.
result = result.edges(">Z and %CIRCLE").chamfer(1.0) # Chamfer the inner top edge

# Optional: Fillet the vertical edges of the polygon for a softer feel?
# The image shows sharp vertical lines, so we keep them sharp.

# Final check:
# - Exterior: Extruded Polygon (Dodecagon)
# - Interior: Cylindrical hole
# - Top: Flat rim with chamfered opening

# Note: If the top rim is actually a circular flange sitting on a polygon body, the code would be different.
# But visually it looks like the polygon goes all the way up.
# Let's refine the top face. There seems to be a circular inset line.
# Maybe the top face has a small circular pocket or the wall thickness varies.
# Let's stick to the simple hollow polygon interpretation which is robust.

# Execute the main generation again with clean logic
result = (
    cq.Workplane("XY")
    .polygon(polygon_sides, outer_diameter) # Outer polygonal shape
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle(inner_radius) # Inner cylindrical cut
    .cutBlind(-(height - 3.0)) # Leave 3mm bottom
)

# Add the small step/ring visible on top. 
# It looks like the hole might have a small counterbore or chamfer.
result = result.edges(">Z and %CIRCLE").chamfer(1.0) 

# Export or visualization would happen here in a real script