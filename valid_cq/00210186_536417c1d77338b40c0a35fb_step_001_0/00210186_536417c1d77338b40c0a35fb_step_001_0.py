import cadquery as cq

# Parametric dimensions
length = 90.0        # Total length of the part
width = 26.0         # Total width of the part
top_thickness = 2.5  # Thickness of the top flange
bot_thickness = 2.0  # Thickness of the bottom protrusion
step_inset = 2.0     # The offset distance for the bottom step
fillet_radius = 1.0  # Radius for the top edge fillet

# Create the top flange (wider stadium shape)
# slot2D creates a shape defined by total length and diameter (width)
top_flange = (
    cq.Workplane("XY")
    .slot2D(length, width)
    .extrude(top_thickness)
)

# Create the bottom protrusion (narrower stadium shape)
# Calculating dimensions to maintain a constant inset/step
# Extruding in negative Z direction to place it under the flange
bottom_protrusion = (
    cq.Workplane("XY")
    .slot2D(length - 2 * step_inset, width - 2 * step_inset)
    .extrude(-bot_thickness)
)

# Combine the parts and apply the fillet to the top edge
result = (
    top_flange
    .union(bottom_protrusion)
    .edges(">Z")  # Select the edges on the highest Z face
    .fillet(fillet_radius)
)