import cadquery as cq

# Parametric dimensions for the model
height = 100.0         # Total length of the tube
outer_width = 20.0     # Side length of the outer square profile
wall_thickness = 2.5   # Thickness of the wall
outer_radius = 2.0     # Fillet radius for the outer corners

# Calculate inner width based on wall thickness
inner_width = outer_width - (2 * wall_thickness)

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # 1. Create the main solid block
    .rect(outer_width, outer_width)
    .extrude(height)
    # 2. Apply fillets to the four vertical outer edges
    .edges("|Z")
    .fillet(outer_radius)
    # 3. Create the hollow center
    .faces(">Z")
    .workplane()
    .rect(inner_width, inner_width)
    .cutBlind(-height)
)