import cadquery as cq

# Define parametric dimensions
length = 40.0       # Total length of the extrusion
base_width = 30.0   # Width at the bottom
top_width = 10.0    # Width of the flat section at the top
height = 20.0       # Total height
fillet_radius = 5.0 # Radius for the top corners

# Create the 2D profile
# We'll draw half of the profile and mirror it, or draw the full shape.
# Let's draw the full trapezoidal shape and then fillet the top corners.

result = (
    cq.Workplane("XY")
    .moveTo(-base_width / 2, 0)
    .lineTo(base_width / 2, 0)      # Bottom edge
    .lineTo(top_width / 2, height)  # Right slope
    .lineTo(-top_width / 2, height) # Top edge
    .close()                        # Left slope back to start
    .extrude(length)
)

# Apply fillets to the top edges running along the length
# We select edges that are "Z" (vertical-ish) relative to the sketch plane is tricky after extrusion.
# It's better to select by position. The top edges are at Z > 0 in the sketch plane coordinate system,
# which becomes Y > 0 in the 3D world if we extruded along Z.
# Wait, let's look at the default orientation.
# Workplane("XY") means Z is up. Sketch is on XY plane. Extrude is along Z.
# So height is in Y direction of the sketch, but usually sketches are X-Y.
# Let's clarify:
# - Sketch is on XY plane.
# - Bottom edge is on Y=0.
# - Top edge is on Y=height.
# - Extrusion is along Z axis.

# So the edges to fillet are the ones corresponding to the top corners of the trapezoid.
# These edges run along the Z axis (the extrusion direction).
# We can select them using a selector that finds edges at Y=height.

result = result.edges(cq.selectors.NearestToPointSelector((0, height, length/2))).fillet(fillet_radius)

# Alternatively, a more robust way to select the two top edges for filleting:
# The edges are parallel to the Z axis (extrusion direction).
# They are located at the top of the profile (max Y in the local sketch coordinates).
# Let's select edges that are at the maximum Y coordinate.

# Re-generating with a cleaner selection strategy for robustness
result = (
    cq.Workplane("XY")
    .moveTo(-base_width / 2, 0)
    .lineTo(base_width / 2, 0)
    .lineTo(top_width / 2, height)
    .lineTo(-top_width / 2, height)
    .close()
    .extrude(length)
    .edges(f">Y") # Select edges with the highest Y coordinate (the top two parallel edges)
    .fillet(fillet_radius)
)