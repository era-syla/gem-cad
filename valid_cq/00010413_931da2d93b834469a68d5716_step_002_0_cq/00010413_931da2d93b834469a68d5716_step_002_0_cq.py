import cadquery as cq

# --- Parametric Dimensions ---
# Standard M6 nut dimensions (approximate) for realistic proportions
nut_height = 5.0      # Thickness of the nut
flat_to_flat = 10.0   # Width across flats
hole_diameter = 6.0   # Diameter of the central hole (nominal thread size)
chamfer_radius = 0.5  # Size of the chamfer on the hole edge

# Calculate radius for circumscribed circle (needed for polygon construction)
# For a hexagon, radius = flat_to_flat / sqrt(3)
import math
radius = flat_to_flat / math.sqrt(3)

# --- Geometry Construction ---

# 1. Create the base hexagonal prism
# Create a workplane, sketch a regular polygon (hexagon), and extrude it
base_nut = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=flat_to_flat / math.cos(math.pi/6)) # CadQuery polygon uses outer diameter (corner-to-corner) often, or circumscribed radius. Let's use the standard polygon method.
    # Actually, cq.Workplane.polygon takes diameter as the diameter of the circle *circumscribing* the polygon.
    # The relationship is: flat_to_flat = diameter * cos(30 degrees) => diameter = flat_to_flat / cos(30)
    .extrude(nut_height)
)

# 2. Create the central hole
# Cut a cylinder through the center
nut_with_hole = base_nut.faces(">Z").workplane().hole(hole_diameter)

# 3. Add the countersink/chamfer to the top hole edge
# Select the top face, then the circular edge of the hole
# Based on the image, the top edge of the hole is rounded or chamfered.
# It looks like a spherical depression or a heavy fillet. Let's apply a fillet to the inner top edge.
result = (
    nut_with_hole
    .faces(">Z")
    .edges(cq.selectors.RadiusNthSelector(0)) # Select the inner hole edge (smallest radius)
    .fillet(chamfer_radius) # Using fillet to give it that smooth, rounded entry look seen in the render
)

# Alternative interpretation: If it's a standard nut, it usually has a conical chamfer on the outer hex edges too,
# but the image shows sharp outer edges and a very pronounced smooth entry to the hole.
# The code above targets specifically the hole feature shown.

# Export or display
# show_object(result) # This would be used in CQ-editor