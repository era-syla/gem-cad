import cadquery as cq

# Parametric Dimensions
length = 2000.0       # Total length of the frame
width = 1000.0        # Total width of the frame
height = 150.0        # Height of the rails
thickness = 25.0      # Thickness of the boards
cleat_height = 30.0   # Height of the inner support ledge
cleat_width = 25.0    # Width of the inner support ledge
cleat_top_offset = 35.0 # Distance from top of frame to top of cleat
hole_dia = 6.0        # Diameter of screw holes

# Calculated Dimensions
rail_inner_len = width - (2 * thickness)
cleat_len = length - (2 * thickness)
cleat_z_pos = (height / 2) - cleat_top_offset - (cleat_height / 2)
hole_offset_x = (length / 2) - (thickness / 2)
hole_spacing_z = height / 3.5

# Hole Pattern Coordinates (Local Face Plane)
# x corresponds to global X, y corresponds to global Z on the side faces
hole_locations = [
    (hole_offset_x, 0),                 # End 1 Middle
    (hole_offset_x, hole_spacing_z),    # End 1 Top
    (hole_offset_x, -hole_spacing_z),   # End 1 Bottom
    (-hole_offset_x, 0),                # End 2 Middle
    (-hole_offset_x, hole_spacing_z),   # End 2 Top
    (-hole_offset_x, -hole_spacing_z),  # End 2 Bottom
    (0, 0)                              # Center
]

# 1. Create Left Side Rail (Positive Y)
# We drill from the outside face (>Y) inwards
side_left = (
    cq.Workplane("XY")
    .box(length, thickness, height)
    .faces(">Y").workplane()
    .pushPoints(hole_locations)
    .hole(hole_dia, depth=thickness + 5) # Drill through + extra
    .translate((0, width/2 - thickness/2, 0))
)

# 2. Create Right Side Rail (Negative Y)
# We drill from the outside face (<Y) inwards
side_right = (
    cq.Workplane("XY")
    .box(length, thickness, height)
    .faces("<Y").workplane()
    .pushPoints(hole_locations)
    .hole(hole_dia, depth=thickness + 5)
    .translate((0, -(width/2 - thickness/2), 0))
)

# 3. Create Transverse Rails (End rails and Middle rail)
# These fit between the side rails
transverse_rail_geo = cq.Workplane("XY").box(thickness, rail_inner_len, height)

end_front = transverse_rail_geo.translate((length/2 - thickness/2, 0, 0))
end_back = transverse_rail_geo.translate((-length/2 + thickness/2, 0, 0))
mid_rail = transverse_rail_geo.translate((0, 0, 0))

# 4. Create Cleats (Inner support ledges)
# Attached to inner faces of side rails
cleat_geo = cq.Workplane("XY").box(cleat_len, cleat_width, cleat_height)

# Left cleat: inner face of left rail is at (W/2 - T). Cleat center is offset by cleat_width/2 inwards
cleat_left = cleat_geo.translate((0, (width/2 - thickness - cleat_width/2), cleat_z_pos))

# Right cleat: inner face of right rail is at -(W/2 - T).
cleat_right = cleat_geo.translate((0, -(width/2 - thickness - cleat_width/2), cleat_z_pos))

# 5. Assemble final result
result = (
    side_left
    .union(side_right)
    .union(end_front)
    .union(end_back)
    .union(mid_rail)
    .union(cleat_left)
    .union(cleat_right)
)