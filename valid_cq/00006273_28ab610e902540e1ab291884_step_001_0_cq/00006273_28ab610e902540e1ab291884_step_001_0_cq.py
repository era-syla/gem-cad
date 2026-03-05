import cadquery as cq

# Parametric dimensions
base_diameter = 40.0
base_height = 15.0
top_diameter = 25.0
top_height = 15.0
hex_width_across_flats = 14.0  # Typical size for this scale
hex_depth = 10.0
fillet_radius_base = 2.0  # Fillet at the transition between base and top
fillet_radius_top_edge = 2.0  # Fillet at the very top edge
fillet_radius_bottom_edge = 1.0 # Slight chamfer/fillet at bottom for aesthetics

# 1. Create the base cylinder
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

# 2. Create the top cylinder on top of the base
top = (
    base.faces(">Z")
    .workplane()
    .circle(top_diameter / 2)
    .extrude(top_height)
)

# 3. Create the hex recess (pocket)
# Using polygon(6) for hexagon. The size parameter for polygon is diameter of circumscribed circle.
# Relation between Width Across Flats (WAF) and circumscribed diameter (D): WAF = D * cos(30) => D = WAF / cos(30)
import math
hex_circum_diameter = hex_width_across_flats / math.cos(math.radians(30))

result = (
    top.faces(">Z")
    .workplane()
    .polygon(6, hex_circum_diameter)
    .cutBlind(-hex_depth)
)

# 4. Apply fillets
# Select the edge between the base and top cylinder
result = result.edges(cq.selectors.NearestToPointSelector((0, base_diameter/2, base_height))).fillet(fillet_radius_base)

# Select the top outer edge
result = result.edges(cq.selectors.NearestToPointSelector((0, top_diameter/2, base_height + top_height))).fillet(fillet_radius_top_edge)

# Select the bottom outer edge (optional but makes it look like the render)
result = result.edges(cq.selectors.NearestToPointSelector((0, base_diameter/2, 0))).fillet(fillet_radius_bottom_edge)