import cadquery as cq

# Dimensions based on image analysis
outer_radius_top = 45      # larger top section outer radius
inner_radius_top = 38      # inner radius of top cup section
outer_radius_bottom = 35   # smaller bottom cylinder outer radius
inner_radius_bottom = 28   # inner radius of bottom cylinder

height_top = 35            # height of the top cup section
height_bottom = 20         # height of the bottom cylinder section

wall_thickness = 7

# Build the bottom cylinder (smaller diameter)
bottom = (
    cq.Workplane("XY")
    .circle(outer_radius_bottom)
    .extrude(height_bottom)
)

# Hollow out the bottom cylinder
bottom = (
    bottom
    .faces(">Z")
    .workplane()
    .circle(inner_radius_bottom)
    .cutBlind(-height_bottom)
)

# Build the top section (larger diameter cup)
top = (
    cq.Workplane("XY")
    .workplane(offset=height_bottom)
    .circle(outer_radius_top)
    .extrude(height_top)
)

# Hollow out the top cup (open top)
top = (
    top
    .faces(">Z")
    .workplane()
    .circle(inner_radius_top)
    .cutBlind(-height_top)
)

# Union the two parts
result = bottom.union(top)