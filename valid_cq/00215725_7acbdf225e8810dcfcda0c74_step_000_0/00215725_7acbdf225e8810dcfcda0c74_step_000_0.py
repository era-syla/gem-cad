import cadquery as cq

# Parametric dimensions for the ring
outer_diameter = 100.0  # The total diameter of the ring
band_height = 8.0       # The width/height of the ring (extrusion depth)
wall_thickness = 2.0    # The thickness of the material

# Calculate radii based on diameter and thickness
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder (ring) geometry
result = (
    cq.Workplane("XY")
    .circle(outer_radius)   # Define outer edge
    .circle(inner_radius)   # Define inner edge to create the hollow center
    .extrude(band_height)   # Extrude to create the 3D form
)