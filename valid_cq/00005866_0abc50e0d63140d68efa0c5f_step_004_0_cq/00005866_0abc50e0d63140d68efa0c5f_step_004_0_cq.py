import cadquery as cq

# Parameters for various hardware components
# Note: Dimensions are estimated based on visual proportions relative to each other

# 1. Long vertical dowel pin
dowel_long_dia = 2.0
dowel_long_length = 15.0
dowel_long_pos = (0, 10, 20)

# 2. Short vertical dowel pin
dowel_short_dia = 2.0
dowel_short_length = 10.0
dowel_short_pos = (5, 5, 15)

# 3. Socket Head Cap Screw (Vertical)
screw_head_dia = 4.0
screw_head_height = 2.5
screw_shank_dia = 2.5
screw_shank_length = 12.0
hex_socket_size = 1.5
hex_socket_depth = 1.5
screw_pos = (12, 0, 10)

# 4. Long nail/pin (Horizontal-ish)
nail_shank_dia = 1.0
nail_shank_length = 25.0
nail_head_dia = 2.5
nail_head_thickness = 0.5
nail_pos = (-10, -10, 0)
nail_rot = (0, 90, 45) # Rotate to lay flat

# 5. Medium rivet/button head (Horizontal-ish)
rivet_shank_dia = 3.0
rivet_shank_length = 6.0
rivet_head_dia = 5.0
rivet_head_thickness = 1.5
rivet_pos = (5, -5, 5)
rivet_rot = (0, 90, 30)

# 6. Small rivet (Horizontal-ish)
small_rivet_shank_dia = 1.0
small_rivet_shank_length = 4.0
small_rivet_head_dia = 2.0
small_rivet_head_thickness = 0.5
small_rivet_pos = (10, -2, 8)
small_rivet_rot = (0, 90, 60)


def create_dowel(diameter, length):
    return cq.Workplane("XY").circle(diameter/2).extrude(length)

def create_socket_head_screw(head_dia, head_h, shank_dia, shank_l, hex_s, hex_d):
    # Shank
    part = cq.Workplane("XY").circle(shank_dia/2).extrude(shank_l)
    # Head
    head = (cq.Workplane("XY")
            .workplane(offset=shank_l)
            .circle(head_dia/2)
            .extrude(head_h))
    # Combine
    part = part.union(head)
    # Hex Socket cut
    part = (part.faces(">Z")
            .workplane()
            .polygon(6, hex_s * 1.5) # simple approximation for hex size to flat-to-flat
            .cutBlind(-hex_d))
    return part

def create_headed_pin(shank_dia, shank_l, head_dia, head_thk):
    # Shank
    part = cq.Workplane("XY").circle(shank_dia/2).extrude(shank_l)
    # Head (using a slight dome for realism)
    part = (part.faces(">Z")
            .workplane()
            .circle(head_dia/2)
            .extrude(head_thk)
            .edges(">Z").fillet(head_thk * 0.4))
    return part

# --- Build Parts ---

# 1. Long Dowel
p1 = create_dowel(dowel_long_dia, dowel_long_length).translate(dowel_long_pos)

# 2. Short Dowel
p2 = create_dowel(dowel_short_dia, dowel_short_length).translate(dowel_short_pos)

# 3. Socket Head Screw
p3 = create_socket_head_screw(screw_head_dia, screw_head_height, 
                              screw_shank_dia, screw_shank_length, 
                              hex_socket_size, hex_socket_depth).translate(screw_pos)

# 4. Long Nail
p4 = create_headed_pin(nail_shank_dia, nail_shank_length, 
                       nail_head_dia, nail_head_thickness)
p4 = p4.rotate((0,0,0), (0,1,0), nail_rot[1]) # Rotate 90 deg around Y to lay flat
p4 = p4.rotate((0,0,0), (0,0,1), nail_rot[2]) # Rotate around Z for orientation
p4 = p4.translate(nail_pos)


# 5. Medium Rivet
p5 = create_headed_pin(rivet_shank_dia, rivet_shank_length, 
                       rivet_head_dia, rivet_head_thickness)
p5 = p5.rotate((0,0,0), (0,1,0), rivet_rot[1])
p5 = p5.rotate((0,0,0), (0,0,1), rivet_rot[2])
p5 = p5.translate(rivet_pos)

# 6. Small Rivet
p6 = create_headed_pin(small_rivet_shank_dia, small_rivet_shank_length, 
                       small_rivet_head_dia, small_rivet_head_thickness)
p6 = p6.rotate((0,0,0), (0,1,0), small_rivet_rot[1])
p6 = p6.rotate((0,0,0), (0,0,1), small_rivet_rot[2])
p6 = p6.translate(small_rivet_pos)


# Combine all parts into one result
result = p1.union(p2).union(p3).union(p4).union(p5).union(p6)