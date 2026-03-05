import cadquery as cq

def create_washer(inner_d, outer_d, thickness):
    """Creates a simple washer."""
    return cq.Workplane("XY").circle(outer_d / 2).circle(inner_d / 2).extrude(thickness)

def create_hex_nut(inner_d, outer_d, height):
    """Creates a simple hex nut."""
    # Outer diameter usually refers to across corners for hex polygon creation
    # or we can approximate standard metric sizing
    return (cq.Workplane("XY")
            .polygon(6, outer_d)
            .circle(inner_d / 2)
            .extrude(height))

def create_socket_head_cap_screw(thread_d, length, head_d, head_h):
    """Creates a socket head cap screw representation."""
    # Create the shaft
    shaft = cq.Workplane("XY").circle(thread_d / 2).extrude(length)
    
    # Create the head
    head = (cq.Workplane("XY")
            .workplane(offset=length - head_h) # Position head at top, but usually threads go down
            # Let's model it with head at Z=0 for simplicity, extruding shaft down
            )
    
    # Re-approach: Head at Z=0 to Z=head_h, shaft from Z=0 to Z=-length
    # This makes stacking easier
    
    head = (cq.Workplane("XY")
            .circle(head_d / 2)
            .extrude(head_h)
            )
    
    # Hex socket cut
    socket_w = thread_d * 0.8 # Approximation
    socket_d = head_h * 0.6
    
    head = (head.faces(">Z").workplane()
            .polygon(6, socket_w)
            .cutBlind(-socket_d))
            
    shaft = (cq.Workplane("XY")
             .circle(thread_d / 2)
             .extrude(-length))
             
    return head.union(shaft)

# --- Parameters ---
# Approximating sizes based on the image which looks like a "hardware kit" spread
# There are 4 distinct groups of items vertically.
# Top: Washers
# Middle-Top: Nuts
# Middle-Bottom: Short Bolts
# Bottom: Long Bolts

# Group 1: Washers (5 items)
washer_od = 10.0
washer_id = 5.0
washer_thk = 1.0
num_washers = 5

# Group 2: Nuts (6 items)
nut_size = 10.0 # Across corners
nut_id = 5.0
nut_h = 4.0
num_nuts = 6

# Group 3: Short Bolts (5 items of increasing size/length)
# Looking closely, they seem to be distinct sizes or lengths
bolt_diameters = [3, 4, 5, 6, 8]
bolt_lengths_short = [8, 10, 12, 16, 20]
head_diameters = [5.5, 7, 8.5, 10, 13]
head_heights = [3, 4, 5, 6, 8]

# Group 4: Medium/Long Bolts (similar progression)
bolt_lengths_long = [12, 16, 20, 25, 30]

# --- Assembly Logic ---
# We will create a list of objects and space them out vertically
parts = []

current_z = 0
spacing = 15.0 # Vertical spacing between centers or bases

# 1. Create Washers (Stacking downwards visually in code list, but positive Z)
for i in range(num_washers):
    w = create_washer(washer_id, washer_od, washer_thk)
    # Translate to position
    w = w.translate((0, 0, current_z))
    parts.append(w)
    current_z -= (washer_od + 2) # Space them out along Y or Z? 
    # The image shows them in a vertical column. Let's stack them vertically (Z-axis).
    # Actually, looking at the image, they are laid out flat on a surface, 
    # but viewed from top-down or isometric.
    # The prompt implies a single model. Let's arrange them linearly along the Y axis.

parts = []
current_y = 0
y_gap = 12.0

# --- Top Group: Washers ---
for i in range(num_washers):
    w = create_washer(washer_id, washer_od, washer_thk)
    w = w.translate((0, current_y, 0))
    parts.append(w)
    current_y -= (washer_od + 5)

current_y -= 10 # Extra gap between groups

# --- Second Group: Nuts ---
for i in range(num_nuts):
    n = create_hex_nut(nut_id, nut_size, nut_h)
    # Rotate to sit flat? They usually sit on the hexagonal face.
    n = n.translate((0, current_y, 0))
    parts.append(n)
    current_y -= (nut_size + 5)

current_y -= 10 # Extra gap

# --- Third Group: Short/Small Bolts ---
# The image shows varying sizes. Let's iterate through sizes.
for i in range(len(bolt_diameters)):
    # Bolts are lying on their side usually in these diagrams, 
    # but making them standing up is standard CAD practice.
    # Let's make them stand up (Z-axis) but arranged in the Y-line.
    b = create_socket_head_cap_screw(bolt_diameters[i], bolt_lengths_short[i], head_diameters[i], head_heights[i])
    
    # To match image appearance (lying "flat" in a column), we rotate them
    # Rotate around X axis by 90 degrees
    b = b.rotate((0,0,0), (1,0,0), -90)
    
    # Center adjustment so they line up nicely
    b = b.translate((0, current_y, head_diameters[i]/2))
    parts.append(b)
    current_y -= (head_diameters[i] + 8)

current_y -= 10 # Extra gap

# --- Fourth Group: Longer Bolts ---
# Repeating the sizes but longer lengths
for i in range(len(bolt_diameters)):
    b = create_socket_head_cap_screw(bolt_diameters[i], bolt_lengths_long[i], head_diameters[i], head_heights[i])
    b = b.rotate((0,0,0), (1,0,0), -90)
    b = b.translate((0, current_y, head_diameters[i]/2))
    parts.append(b)
    current_y -= (head_diameters[i] + 8)

# Combine all parts into one compound object
result = parts[0]
for p in parts[1:]:
    result = result.union(p)

# Orient the whole strip to match the vertical image orientation if desired,
# but the current logic creates a strip along the Y axis which matches the aspect ratio.