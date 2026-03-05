import cadquery as cq

# Parametric dimensions
length = 60.0
width = 25.0
height = 20.0
fillet_radius = 5.0
hole_diameter = 4.0
hole_spacing = 40.0  # Distance between centers of the two top holes
hex_across_flats = 8.0  # Size of the hex hole (flat to flat)

# Create the main block
result = (
    cq.Workplane("XY")
    .box(length, width, height)
)

# Apply fillets to the top edges along the length
# We select edges that are parallel to the Y axis (width), are on the top face (Z max),
# but looking at the image, the fillets are actually along the X-axis edges on the top face.
# Let's refine the selection: Edges parallel to X, on the top face (Z>0).
result = result.edges("|X and >Z").fillet(fillet_radius)

# Create the two counterbored/countersunk holes on the top face
# Based on image, they look like simple through holes or shallow blind holes.
# Let's assume through holes for simplicity, or deep blind holes.
# They are positioned symmetrically along the length.
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .hole(hole_diameter)
)

# Create the hexagonal hole on the front face
# The hex hole goes through the width (Y axis) or at least deep into it.
result = (
    result.faces(">Y")
    .workplane()
    .center(0, 0)  # Centered on the face
    .polygon(6, hex_across_flats / (3**0.5), circumscribed=False) # circumscribed=False means side-to-side dimension usually
    # CadQuery's polygon uses radius. For a hex, radius = side length. 
    # If "across flats" is 'h', then side length 's' = h / sqrt(3).
    # Wait, CadQuery polygon takes diameter (outer circle) or radius? 
    # .polygon(nSides, diameter) usually implies the circumscribed circle diameter.
    # For a hex, distance across corners = 2 * (across_flats / sqrt(3)).
    # Let's stick to a simpler method: creating a polygon and cutting.
    .cutBlind(-width) # Cut through the entire width
)

# Note: polygon arguments: nSides, diameter (of circumcircle). 
# If hex_across_flats is 8mm. The circumradius R = (8/2) / (sqrt(3)/2) = 8/sqrt(3).
# The circumdiameter D = 16/sqrt(3).
hex_circum_diameter = (hex_across_flats / (3**0.5)) * 2

# Re-doing the hex cut with precise math
result = (
    result.faces(">Y")
    .workplane()
    .center(0, 0)
    .polygon(6, hex_circum_diameter)
    .cutBlind(-width) # Cut through
)