import cadquery as cq

def make_washer(od=10.0, id=5.3, thickness=1.0):
    """
    Creates a simple washer geometry.
    """
    return (cq.Workplane("XY")
            .circle(od / 2.0)
            .circle(id / 2.0)
            .extrude(thickness))

def make_nut(size=5.0):
    """
    Creates a hexagonal nut geometry.
    """
    # Approximate dimensions for an M-series nut
    width_across_corners = size * 2.0 
    height = size * 0.8
    
    return (cq.Workplane("XY")
            .polygon(6, width_across_corners)
            .circle(size / 2.0)
            .extrude(height))

def make_screw(size=5.0, length=12.0):
    """
    Creates a Socket Head Cap Screw (SHCS) geometry.
    """
    head_dia = size * 1.7
    head_height = size
    shaft_dia = size
    socket_across_flats = size * 0.8
    socket_dia = socket_across_flats / 0.866025  # Convert flat-to-flat to corner-to-corner
    
    # Create the cylindrical head
    head = (cq.Workplane("XY")
            .circle(head_dia / 2.0)
            .extrude(head_height))
            
    # Cut the hex socket into the head
    head = (head.faces(">Z").workplane()
            .polygon(6, socket_dia)
            .cutBlind(-head_height * 0.6))
            
    # Create the threaded shaft extending downwards
    shaft = (cq.Workplane("XY")
             .circle(shaft_dia / 2.0)
             .extrude(-length))
             
    return head.union(shaft)

# --- Assembly Construction ---
parts = []
current_z = 0.0
vertical_spacing_small = 2.0
vertical_spacing_large = 6.0
group_gap = 10.0

# 1. Stack of Washers (5 items)
for _ in range(5):
    washer = make_washer().translate((0, 0, current_z))
    parts.append(washer)
    current_z -= (1.0 + vertical_spacing_small) # washer thickness + gap

current_z -= group_gap

# 2. Stack of Nuts (5 items)
for _ in range(5):
    nut = make_nut().translate((0, 0, current_z))
    parts.append(nut)
    current_z -= (4.0 + vertical_spacing_large) # nut height + gap

current_z -= group_gap

# 3. Stack of Screws - Group 1 (Mixed lengths: 3 short, 1 long, 1 short)
lengths_g1 = [12.0, 12.0, 12.0, 35.0, 12.0]
for l in lengths_g1:
    # Screw origin is at base of head. Shaft goes -Z, Head goes +Z.
    # We position it so the head is at current_z
    screw = make_screw(length=l).translate((0, 0, current_z))
    parts.append(screw)
    # Move down by length of shaft + head height of next screw + visual gap
    current_z -= (l + 5.0 + vertical_spacing_large)

current_z -= group_gap

# 4. Stack of Screws - Group 2 (4 short items)
for _ in range(4):
    l = 14.0
    screw = make_screw(length=l).translate((0, 0, current_z))
    parts.append(screw)
    current_z -= (l + 5.0 + vertical_spacing_large)

current_z -= group_gap

# 5. Stack of Screws - Group 3 (5 medium items)
for _ in range(5):
    l = 16.0
    screw = make_screw(length=l).translate((0, 0, current_z))
    parts.append(screw)
    current_z -= (l + 5.0 + vertical_spacing_large)

# Combine all independent parts into a single compound object
if parts:
    result = parts[0]
    for part in parts[1:]:
        result = result.union(part)
else:
    result = cq.Workplane("XY")