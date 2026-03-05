import cadquery as cq

# Parametric dimensions for the frame
length = 150.0         # Outer length of the frame
width = 100.0          # Outer width of the frame
thickness = 12.0       # Thickness of the part
frame_width = 18.0     # Width of the frame border
outer_radius = 5.0     # Radius of the outer corner fillets
hole_diameter = 5.0    # Diameter of the corner holes

# 1. Create the base solid block
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Apply fillets to the four vertical outer edges
result = result.edges("|Z").fillet(outer_radius)

# 3. Create the central rectangular cutout
# Calculate inner dimensions based on frame width
inner_length = length - 2 * frame_width
inner_width = width - 2 * frame_width

result = (
    result.faces(">Z")
    .workplane()
    .rect(inner_length, inner_width)
    .cutBlind(-thickness)
)

# 4. Drill the mounting holes
# Calculate position so holes are centered on the frame border strip
# Dimensions for the construction rectangle defining hole centers
hole_rect_width = length - frame_width
hole_rect_height = width - frame_width

result = (
    result.faces(">Z")
    .workplane()
    .rect(hole_rect_width, hole_rect_height, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)