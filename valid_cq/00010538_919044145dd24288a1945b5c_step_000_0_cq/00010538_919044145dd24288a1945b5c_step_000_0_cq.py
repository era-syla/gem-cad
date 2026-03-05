import cadquery as cq

# Parametric dimensions
height = 20.0
max_diameter = 30.0
min_diameter = 18.0  # Diameter at the narrowest waist
hex_size = 6.0       # Distance across flats for the hex hole
hex_depth = 10.0     # Depth of the hex hole (can be 'height' for through-hole)

# Calculations for the profile arc
# We want an arc that starts at (max_radius, height/2), goes through (min_radius, 0), and ends at (max_radius, -height/2)
# Alternatively, simpler to just revolve a profile.
max_radius = max_diameter / 2.0
min_radius = min_diameter / 2.0

# Method: Create a 2D profile and revolve it.
# The profile is on the XZ plane.
# Points:
# 1. Top right: (max_radius, height)
# 2. Bottom right: (max_radius, 0)
# But the side is curved.
# Let's define points for a 3-point arc on the side:
# Start: (max_radius, height)
# Middle: (min_radius, height/2)
# End: (max_radius, 0)

# Create the main body by revolving a face
# We draw the right-half profile and revolve around Z axis
result = (
    cq.Workplane("XZ")
    .moveTo(max_radius, height)
    .lineTo(0, height)          # Top straight line to center
    .lineTo(0, 0)               # Center line down
    .lineTo(max_radius, 0)      # Bottom straight line out
    .threePointArc((min_radius, height / 2.0), (max_radius, height)) # Curved side back to start
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0)) # Revolve around the Z axis (which is the Y axis in this 2D plane context)
)

# Add the hexagonal hole
# We select the top face (which is at Z=height due to our revolve profile setup)
# Note: In the 2D profile above, Y corresponds to the Z height of the final object.
# Let's adjust coordinate system mental model. 
# Workplane("XZ") means X is horizontal, Z is vertical on screen.
# .revolve creates rotation around an axis. 
# Let's use a simpler approach: Revolve around Y axis of the workplane to align with Z of the world.

# Re-doing the construction for clarity and standard orientation (Z-up)
result = (
    cq.Workplane("XZ")
    # Define points for the profile
    .moveTo(0, 0)
    .lineTo(max_radius, 0)
    # Create the concave arc profile
    .threePointArc((min_radius, height / 2.0), (max_radius, height))
    .lineTo(0, height)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0)) # Revolve around local Y (global Z)
)

# Cut the hex hole
result = (
    result.faces(">Z")
    .workplane()
    .polygon(6, hex_size / 0.866025) # cadquery polygon uses outer radius (circumradius). hex_size is usually across flats. 
                                     # radius = (flat_to_flat / 2) / cos(30) = flat_to_flat / sqrt(3) ~= flat_to_flat / 1.732
                                     # Actually, let's use the explicit diameter arg if available or calc correctly.
                                     # polygon takes 'diameter' which is the diameter of the circumscribed circle.
                                     # diam = (hex_size / 2) / (sqrt(3)/2) * 2 = hex_size * 2 / sqrt(3)
    .cutBlind(-hex_depth)
)

# Correction on polygon sizing:
# hex_size variable is usually "width across flats".
# CadQuery's polygon method creates a polygon circumscribed by the given diameter (vertex to vertex).
# D_circumscribed = W_flats / cos(30deg) = W_flats / (sqrt(3)/2)
import math
circum_diameter = hex_size / (math.sqrt(3) / 2)

result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(max_radius, 0)
    .threePointArc((min_radius, height / 2.0), (max_radius, height))
    .lineTo(0, height)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
    .faces(">Z")
    .workplane()
    .polygon(6, circum_diameter)
    .cutBlind(-hex_depth)
)