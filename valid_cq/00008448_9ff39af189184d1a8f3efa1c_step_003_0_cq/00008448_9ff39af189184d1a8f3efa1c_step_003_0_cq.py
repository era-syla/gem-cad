import cadquery as cq

# Parameters
base_width = 40.0         # Width of the square base
base_height = 4.0         # Thickness of the bottom square base
mid_section_height = 8.0  # Height of the dark middle section (looks like a seal or spacer)
top_hex_height = 12.0     # Height of the top hexagonal block
hex_flat_to_flat = 36.0   # Width of the hexagon (flat to flat)
stem_diameter = 4.0       # Diameter of the long vertical stem
stem_height = 40.0        # Height of the stem relative to the top of the hex block
stem_bore_dia = 2.0       # Inner hole diameter of the stem

# 1. Create the square base
# Centered square base plate
base = cq.Workplane("XY").box(base_width, base_width, base_height)

# 2. Create the middle section
# This looks like a slightly smaller extrusion, possibly a square or a hexagon, 
# sitting on top of the base. Based on the cutaway view, it seems to follow the 
# contour of the top hexagon but sits on the square base. 
# Let's model it as a hexagon matching the top block, but darkened in the render.
# We create a new workplane on top of the base.
mid_section = (
    base.faces(">Z").workplane()
    .polygon(6, hex_flat_to_flat) # 6 sides, diameter is usually circumcircle, but let's approximate
    .extrude(mid_section_height)
)

# 3. Create the top hexagonal block
# This sits on top of the middle section.
top_block = (
    mid_section.faces(">Z").workplane()
    .polygon(6, hex_flat_to_flat)
    .extrude(top_hex_height)
)

# 4. Create the vertical stem
# A long cylinder centered on top of the hex block.
stem = (
    top_block.faces(">Z").workplane()
    .circle(stem_diameter / 2.0)
    .extrude(stem_height)
)

# 5. Create the bore (hole) through the stem
# The hole seems to go through the stem. We'll drill it through the stem.
# Depending on the design intent, it might go deeper, but looking at the top face,
# it definitely exists.
result = (
    stem.faces(">Z").workplane()
    .circle(stem_bore_dia / 2.0)
    .cutBlind(-stem_height) # Cut down through the stem
)

# Optional: Add the cutaway feature if intended to match the image precisely geometry-wise.
# The image shows a cutaway view (quarter section removed) to reveal internal details.
# However, usually, when asked to model "this object", one models the whole object.
# The prompt asks for "this 3D CAD model", which usually implies the full solid.
# But the image *is* a section view. 
# Looking closely at the image, there is a visible rectangular pocket/cutout on the front face
# that cuts through the black section and partly into the base and top.
# It looks like a quarter cut (section view).
# To reproduce the visual result of the geometry exactly as shown (with the cutout):

# Create a large box to subtract one quadrant (Front-Right quadrant)
cutout_size = 100.0 # Arbitrary large number
result = result.faces(">Z").workplane().rect(cutout_size, cutout_size, centered=False).cutBlind(-100)

# Wait, looking closer at the bottom "black" section. It's inset from the square base corners.
# The cutaway reveals the inside. 
# Let's refine the geometry slightly based on the visual cues.
# It seems to be: Square Base -> Hex Spacer (Black) -> Hex Top (Grey) -> Stem.
# And there is a 90-degree wedge cut out to show the section.

# Re-assembling the logic to ensure the "result" variable holds the final cut object.
# I will apply the cut at the very end.

# --- Refined Modeling Steps ---

# Base
res = cq.Workplane("XY").box(base_width, base_width, base_height)

# Middle Hex (Black part)
res = res.faces(">Z").workplane().polygon(6, hex_flat_to_flat * 1.155).extrude(mid_section_height) 
# Note: polygon takes the circumradius diameter usually, or diagonal. 
# For a flat-to-flat of 36, diagonal is ~41.5. Let's stick to standard Polygon usage.
# If circumradius = r, flat-to-flat = r * sqrt(3). r = f2f / sqrt(3). 
# CadQuery polygon size argument is diameter of circumscribing circle.
circum_dia = hex_flat_to_flat / (3**0.5 / 2) 

# Re-doing the extrusions to ensure correct hex sizing
res = cq.Workplane("XY").box(base_width, base_width, base_height)
res = res.faces(">Z").workplane().polygon(6, circum_dia).extrude(mid_section_height)
res = res.faces(">Z").workplane().polygon(6, circum_dia).extrude(top_hex_height)
res = res.faces(">Z").workplane().circle(stem_diameter / 2.0).extrude(stem_height)

# Hollow out the stem
res = res.faces(">Z").workplane().circle(stem_bore_dia / 2.0).cutBlind(-stem_height)

# Create the section cut (Removing the front-right quadrant to match the image style)
# We position a cutting box at the center (0,0) extending into +X, -Y (Front Right in standard CAD view depends on orientation,
# but usually +X, -Y is Quadrant 4. In the image, the cut is the corner facing the viewer).
# Let's assume standard ISO view. The corner closest to camera is usually +X, -Y or +X, +Y depending on "Front".
# Let's cut the corner defined by X>0 and Y<0.
cut_box = cq.Workplane("XY").workplane(offset=-10).rect(base_width, base_width, centered=False).extrude(100)
# Shift the cut box to the correct quadrant (e.g., origin to +X, -Y)
cut_box = cut_box.translate((0, -base_width, 0))

# Apply the cut
result = res.cut(cut_box)