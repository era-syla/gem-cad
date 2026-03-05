import cadquery as cq

# ==========================================
# Parameters
# ==========================================

# Head Section Dimensions
head_len_fwd = 28.0      # Distance from boss center to front tip
head_len_back = 18.0     # Distance from boss center to back face
head_width_max = 24.0    # Maximum width of the head
head_width_tip = 8.0     # Width at the front tip
head_width_neck = 12.0   # Width at the back face (connection to shaft)
thickness = 8.0          # Thickness of the main body

# Shaft Section Dimensions
shaft_length = 50.0
shaft_width = 8.0

# Tail Section Dimensions
tail_length = 16.0
tail_width = 12.0
tail_chamfer_size = 3.0

# Feature Dimensions
boss_dia = 18.0          # Top boss diameter
boss_height = 2.0        # Top boss height
pivot_dia = 12.0         # Bottom pivot diameter
pivot_height = 8.0       # Bottom pivot length
hole_dia = 4.0           # Front hole diameter
hole_depth = 20.0        # Front hole depth

# ==========================================
# Geometry Construction
# ==========================================

# 1. Define Head Profile (Polyline)
# Coordinates are relative to origin (0,0) at the center of the boss/pivot
x_taper_start = -12.0    # X coord where the front taper ends and max width begins
x_taper_end = 8.0        # X coord where max width ends and back taper begins

head_pts = [
    (-head_len_fwd, head_width_tip / 2.0),      # Front Tip Top
    (x_taper_start, head_width_max / 2.0),      # Widest Section Start Top
    (x_taper_end, head_width_max / 2.0),        # Widest Section End Top
    (head_len_back, head_width_neck / 2.0),     # Neck Top
    (head_len_back, -head_width_neck / 2.0),    # Neck Bottom
    (x_taper_end, -head_width_max / 2.0),       # Widest Section End Bottom
    (x_taper_start, -head_width_max / 2.0),     # Widest Section Start Bottom
    (-head_len_fwd, -head_width_tip / 2.0)      # Front Tip Bottom
]

# Create Head Solid
head = cq.Workplane("XY").polyline(head_pts).close().extrude(thickness)

# 2. Create Shaft
# Shaft extends from the back of the head
# We position the rect center calculated from the head end
shaft_x_pos = head_len_back + shaft_length / 2.0
shaft = (cq.Workplane("XY")
         .moveTo(shaft_x_pos, 0)
         .rect(shaft_length, shaft_width)
         .extrude(thickness))

# 3. Create Tail
# Tail extends from the end of the shaft
tail_x_pos = head_len_back + shaft_length + tail_length / 2.0
tail = (cq.Workplane("XY")
        .moveTo(tail_x_pos, 0)
        .rect(tail_length, tail_width)
        .extrude(thickness))

# 4. Combine Basic Shapes
body = head.union(shaft).union(tail)

# 5. Add Features

# Chamfer the end of the tail
# Select the face at the extreme positive X and chamfer its edges
body = body.faces(">X").edges().chamfer(tail_chamfer_size)

# Add Top Boss (Cylinder on top face)
# Positioned absolutely at (0,0) on top of the thickness
boss = (cq.Workplane("XY")
        .workplane(offset=thickness)
        .circle(boss_dia / 2.0)
        .extrude(boss_height))

# Add Bottom Pivot (Cylinder on bottom face)
# Positioned absolutely at (0,0), extruding downwards (-Z)
pivot = (cq.Workplane("XY")
         .circle(pivot_dia / 2.0)
         .extrude(-pivot_height))

# Union Bosses with Body
result = body.union(boss).union(pivot)

# Cut Front Hole
# Select the front face (min X), create workplane, cut blind hole
result = (result.faces("<X").workplane()
          .circle(hole_dia / 2.0)
          .cutBlind(hole_depth))