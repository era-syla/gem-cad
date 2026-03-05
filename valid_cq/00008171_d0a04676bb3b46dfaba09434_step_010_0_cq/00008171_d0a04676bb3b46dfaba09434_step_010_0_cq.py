import cadquery as cq

# --- Parameter Definitions ---

# Main Body Dimensions
main_body_radius = 15.0
main_body_height = 40.0

# Top Hex Nut Dimensions
top_hex_flat_size = 18.0  # Distance across flats
top_hex_height = 5.0
top_hex_radius = top_hex_flat_size / (3**0.5) # Calculate radius for hexagon

# Top Cylinder (Stem) Dimensions
stem_radius = 5.0
stem_height = 15.0
stem_chamfer = 0.5
stem_base_radius = 6.0 # Small fillet/ridge at base of stem
stem_base_height = 1.0

# Top Hole Dimensions
top_hole_radius = 3.0
top_hole_depth = 12.0

# Bottom Geometry Dimensions
bottom_taper_height = 4.0
bottom_taper_radius = 10.0 # Ending radius of the taper
bottom_fitting_height = 10.0
bottom_fitting_radius = 8.0 
bottom_fitting_hex_height = 4.0 # A small hex section at the bottom fitting
bottom_fitting_hex_size = 14.0 # Across flats

# --- Geometry Construction ---

# 1. Main Cylindrical Body
main_body = cq.Workplane("XY").circle(main_body_radius).extrude(main_body_height)

# 2. Top Section
# Create the Hexagon Nut
top_hex = (
    cq.Workplane("XY")
    .workplane(offset=main_body_height)
    .polygon(6, top_hex_radius * 2) # CadQuery polygon takes diameter
    .extrude(top_hex_height)
)

# Create the Stem Base (small cylinder/fillet base)
stem_base = (
    cq.Workplane("XY")
    .workplane(offset=main_body_height + top_hex_height)
    .circle(stem_base_radius)
    .extrude(stem_base_height)
)

# Create the Main Stem
stem = (
    cq.Workplane("XY")
    .workplane(offset=main_body_height + top_hex_height + stem_base_height)
    .circle(stem_radius)
    .extrude(stem_height)
)

# Apply Chamfer to the top of the stem
stem = stem.edges(">Z").chamfer(stem_chamfer)

# 3. Bottom Section
# Tapered section
bottom_taper = (
    cq.Workplane("XY")
    .circle(main_body_radius)
    .workplane(offset=-bottom_taper_height)
    .circle(bottom_taper_radius)
    .loft(combine=True)
)

# Bottom Hex Section (fitting interface)
bottom_hex = (
    cq.Workplane("XY")
    .workplane(offset=-(bottom_taper_height))
    .polygon(6, bottom_fitting_hex_size * 2 / (3**0.5) * 2) 
    .extrude(-bottom_fitting_hex_height)
)

# Bottom Cylinder Section
bottom_cyl = (
    cq.Workplane("XY")
    .workplane(offset=-(bottom_taper_height + bottom_fitting_hex_height))
    .circle(bottom_fitting_radius)
    .extrude(-(bottom_fitting_height - bottom_fitting_hex_height))
)

# --- Combine and Refine ---

# Union all solid parts
result = (
    main_body
    .union(top_hex)
    .union(stem_base)
    .union(stem)
    .union(bottom_taper)
    .union(bottom_hex)
    .union(bottom_cyl)
)

# Cut the top hole
result = result.faces(">Z").workplane().hole(top_hole_radius * 2, top_hole_depth)

# Optional: Add small fillets between major transitions for realism
# Fillet between main body and top hex
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, main_body_height))).fillet(0.5)

# Fillet between top hex and stem base
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, main_body_height + top_hex_height))).fillet(0.5)