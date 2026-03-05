import cadquery as cq

# Parametric dimensions
block_length = 40.0   # Total length of the top block
block_width = 30.0    # Total width (depth) of the top block
block_height = 20.0   # Height of the top block section

tab_length = 15.0     # Length of the bottom tab protrusion
tab_width = block_width # Tab width matches block width in this view, or could be smaller. Assuming same depth.
tab_height = 10.0     # Height of the bottom tab protrusion

center_hole_diam = 14.0 # Diameter of the large vertical hole
side_hole_diam = 4.0    # Diameter of the small horizontal holes
side_hole_depth = 10.0  # Depth of side holes (or through, but visually look like blind/thru to center)

fillet_radius = 1.0   # Radius for edge fillets

# Create the main body
# We'll start with the top block
top_block = cq.Workplane("XY").box(block_length, block_width, block_height)

# Create the bottom tab
# We center it on the bottom face of the top block
bottom_tab = (
    cq.Workplane("XY")
    .workplane(offset=-block_height / 2 - tab_height / 2)
    .box(tab_length, tab_width, tab_height)
)

# Fuse the two parts
main_body = top_block.union(bottom_tab)

# Create the central vertical hole
# We cut through everything
with_center_hole = (
    main_body
    .faces(">Z")
    .workplane()
    .hole(center_hole_diam)
)

# Create the side holes
# Located on the +X and -X faces of the top block
result = (
    with_center_hole
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .hole(side_hole_diam)
    .faces("<X")
    .workplane(centerOption="CenterOfMass")
    .hole(side_hole_diam)
)

# Apply fillets to all outer edges
# We select all edges, usually excluding the hole circles to keep them sharp, 
# or just select specific outer edges. The image shows almost all outer edges are rounded.
result = result.edges("|Z or |X or |Y").fillet(fillet_radius)

# If the fillets break the geometry on the hole edges, a more specific selection strategy:
# result = result.edges("%FILLET").fillet(fillet_radius) 
# But simple orthogonal edge selection usually works best for boxy shapes.