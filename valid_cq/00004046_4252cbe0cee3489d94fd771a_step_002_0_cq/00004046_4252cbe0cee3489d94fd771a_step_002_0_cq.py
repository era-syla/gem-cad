import cadquery as cq

# Helper function to create a hex nut
def make_nut(size, height):
    # Determine dimensions based on size (simplified metric approximation)
    width_across_flats = size * 1.6  # Approx standard
    width_across_corners = width_across_flats * 1.1547
    
    nut = (
        cq.Workplane("XY")
        .polygon(6, width_across_corners)
        .extrude(height)
    )
    
    # Add chamfer to top and bottom faces (simulated by intersection with a cone or sphere, or simplified chamfer)
    # A simple chamfer on edges is often sufficient for visualization
    # But for a proper nut look, we intersect with a revolved shape or chamfer the outer edges
    # Let's just chamfer the outer edges
    nut = nut.edges("|Z").chamfer(height * 0.1)
    
    # Cut the hole
    hole = cq.Workplane("XY").circle(size / 2).extrude(height)
    nut = nut.cut(hole)
    
    # Add thread simulation (optional, skipped for performance/simplicity)
    return nut

# Helper function to create a washer
def make_washer(inner_dia, outer_dia, thickness):
    washer = (
        cq.Workplane("XY")
        .circle(outer_dia / 2)
        .circle(inner_dia / 2)
        .extrude(thickness)
    )
    return washer

# Helper function to create a socket head cap screw
def make_screw(thread_dia, length, head_dia, head_height):
    # Head
    head = (
        cq.Workplane("XY")
        .circle(head_dia / 2)
        .extrude(head_height)
    )
    
    # Hex socket
    socket_size = thread_dia * 0.8 # Approx
    socket = (
        cq.Workplane("XY")
        .workplane(offset=head_height)
        .polygon(6, socket_size)
        .extrude(-head_height * 0.6)
    )
    
    # Shaft
    shaft = (
        cq.Workplane("XY")
        .circle(thread_dia / 2)
        .extrude(-length)
    )
    
    screw = head.cut(socket).union(shaft)
    return screw

# --- Assembly Construction ---

parts = []
current_z = 0
spacing = 15  # Gap between parts

# 1. Top Section: Assorted Washers/Circlips
# Looks like ~5 thin washers or retaining rings
washer_specs = [
    (6, 12, 1.0),
    (6, 12, 1.0),
    (6, 12, 1.0),
    (6, 12, 1.0),
    (5, 10, 0.8), # Slightly smaller
]

for inner, outer, thick in washer_specs:
    part = make_washer(inner, outer, thick).translate((0, 0, current_z))
    parts.append(part)
    current_z -= (thick + spacing/2) # Tighter spacing for washers

current_z -= spacing # Extra gap

# 2. Second Section: Nuts
# A stack of about 6 hex nuts
nut_specs = [
    (6, 5), # M6
    (6, 5),
    (6, 5),
    (6, 5),
    (5, 4), # M5
    (5, 4),
]

for size, height in nut_specs:
    part = make_nut(size, height).translate((0, 0, current_z))
    parts.append(part)
    current_z -= (height + spacing)

current_z -= spacing

# 3. Third Section: Screws (Short to Medium)
# A group of socket head cap screws
screw_specs_1 = [
    (3, 10, 5.5, 3),   # M3x10
    (4, 12, 7, 4),     # M4x12
    (5, 16, 8.5, 5),   # M5x16
    (6, 20, 10, 6),    # M6x20
    (8, 30, 13, 8),    # M8x30 (The long one sticking out?) - actually looking at image, they are stacked vertically but rendered slightly offset? No, just vertically.
]

# The image has some screws that look different, maybe button head or countersunk, 
# but most look like socket head cap screws. Let's stick to SHCS.

for dia, length, h_dia, h_height in screw_specs_1:
    # Rotate screws so they lay flat or stand up? 
    # In the image, they are oriented vertically (shaft pointing down or up). 
    # Let's orient them shaft-down like the nuts.
    # The make_screw function builds head at z=0 to z=head_height, shaft going negative Z.
    
    # Align head top to current_z
    part = make_screw(dia, length, h_dia, h_height).translate((0, 0, current_z))
    parts.append(part)
    # Move down by total length of screw plus spacing
    current_z -= (length + spacing)

current_z -= spacing

# 4. Fourth Section: More Screws
screw_specs_2 = [
    (4, 10, 7, 4),
    (4, 12, 7, 4),
    (5, 15, 8.5, 5),
    (5, 20, 8.5, 5),
]

for dia, length, h_dia, h_height in screw_specs_2:
    part = make_screw(dia, length, h_dia, h_height).translate((0, 0, current_z))
    parts.append(part)
    current_z -= (length + spacing)

current_z -= spacing

# 5. Bottom Section: Larger Screws
screw_specs_3 = [
    (5, 12, 8.5, 5),
    (5, 16, 8.5, 5),
    (6, 20, 10, 6),
    (6, 25, 10, 6),
    (8, 30, 13, 8),
]

for dia, length, h_dia, h_height in screw_specs_3:
    part = make_screw(dia, length, h_dia, h_height).translate((0, 0, current_z))
    parts.append(part)
    current_z -= (length + spacing)

# Combine all parts into a single compound object
result = parts[0]
for p in parts[1:]:
    result = result.union(p)
