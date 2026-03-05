import cadquery as cq

# --- Parameters ---
# PCB Dimensions
pcb_length = 80.0
pcb_width = 30.0
pcb_thickness = 1.6
corner_radius = 3.0

# Mounting Holes
hole_diameter = 3.2  # Approx for M3
hole_inset_x = 3.0
hole_inset_y = 3.0

# Pin Header Parameters (Standard 2.54mm pitch)
pitch = 2.54
pin_size = 0.64  # Square pin width
pin_height_top = 6.0
pin_height_bottom = 6.0
base_height = 2.5  # The black plastic insulator part
base_width = 2.54
base_length_multiplier = 2.54

# Connector/Block Component (The large boxy one)
block_length = 12.0
block_width = 10.0
block_height = 10.0
block_pos_x = -15.0 # Relative to center
block_pos_y = 5.0

# Header Configurations
# Group 1: 2x6 header on top
header1_rows = 2
header1_cols = 6
header1_pos_x = 5.0
header1_pos_y = -5.0

# Group 2: 2x6 header on top
header2_rows = 2
header2_cols = 6
header2_pos_x = 25.0
header2_pos_y = -5.0

# Group 3: 1x6 header on bottom (pointing down)
header3_rows = 1
header3_cols = 6
header3_pos_x = -32.0 # Near the edge
header3_pos_y = -10.0 # Near the bottom edge

# Small vias/holes line
via_diameter = 1.0
via_count = 6
via_start_x = -35.0
via_start_y = -12.0
via_spacing = 2.54

# --- Helper Functions ---

def create_pin_header(rows, cols, is_top=True):
    """Creates a block representing the plastic base and individual pins."""
    total_len = cols * pitch
    total_wid = rows * pitch
    
    # Plastic Base
    base = (cq.Workplane("XY")
            .box(total_len, total_wid, base_height)
            .translate((0, 0, base_height/2))
            )
    
    # Pins
    pin = (cq.Workplane("XY")
           .rect(pin_size, pin_size)
           .extrude(pin_height_top + base_height + (pin_height_bottom if not is_top else 0))
           )
    
    if not is_top:
        # If headers are on bottom, we need to shift the extrusion relative to the base
        # But here we are modeling top-side headers mostly based on the image, 
        # except the one sticking out the bottom.
        # Let's simplify: This function makes a "Top Side" header assembly.
        pass

    pins = cq.Assembly()
    
    # Create grid of pins
    pin_solid = pin.val()
    
    # We will union all pins into one object for performance
    all_pins = cq.Workplane("XY")
    
    for r in range(rows):
        for c in range(cols):
            # Calculate position relative to center of the header block
            x_offset = (c - (cols-1)/2) * pitch
            y_offset = (r - (rows-1)/2) * pitch
            
            # Add pin geometry
            # Shift pin up so it goes through base
            p = pin.translate((x_offset, y_offset, -1.0)) 
            all_pins = all_pins.union(p)

    final_header = base.union(all_pins)
    return final_header

def create_bottom_header(rows, cols):
    """Creates a header where pins point downwards."""
    total_len = cols * pitch
    total_wid = rows * pitch
    
    # Plastic Base (on bottom of PCB usually, but let's assume standard strip)
    # The image shows pins sticking out the bottom. Often the black plastic is on the bottom side too.
    base = (cq.Workplane("XY")
            .box(total_len, total_wid, base_height)
            .translate((0, 0, -base_height/2 - pcb_thickness)) # Below PCB
            )
            
    # Pins
    pin = (cq.Workplane("XY")
           .rect(pin_size, pin_size)
           .extrude(-(pin_height_bottom + base_height)) # Extrude downwards
           .translate((0, 0, -pcb_thickness))
           )

    all_pins = cq.Workplane("XY")
    for r in range(rows):
        for c in range(cols):
            x_offset = (c - (cols-1)/2) * pitch
            y_offset = (r - (rows-1)/2) * pitch
            p = pin.translate((x_offset, y_offset, 0)) 
            all_pins = all_pins.union(p)
            
    return base.union(all_pins)


# --- Build Geometry ---

# 1. PCB Substrate
pcb = (cq.Workplane("XY")
       .box(pcb_length, pcb_width, pcb_thickness)
       .edges("|Z")
       .fillet(corner_radius)
       )

# Mounting Holes
h_x = pcb_length/2 - hole_inset_x
h_y = pcb_width/2 - hole_inset_y

pcb = (pcb.faces(">Z").workplane()
       .pushPoints([(h_x, h_y), (h_x, -h_y), (-h_x, h_y), (-h_x, -h_y)])
       .hole(hole_diameter)
       )

# Small Via holes (row along the edge as seen in image)
via_points = []
for i in range(via_count):
    via_points.append((via_start_x + i * via_spacing, via_start_y))

pcb = (pcb.faces(">Z").workplane()
       .pushPoints(via_points)
       .hole(via_diameter)
       )


# 2. Large Component Block (The boxy one)
# It has a slight chamfer/slant on one face in the image
block = (cq.Workplane("XY")
         .box(block_length, block_width, block_height)
         .translate((block_pos_x, block_pos_y, block_height/2 + pcb_thickness/2))
         )
# Add the slant/chamfer to the block (shroud style)
# We slice a corner off
cutter = (cq.Workplane("XY")
          .workplane(offset=pcb_thickness/2 + block_height)
          .transformed(rotate=(0, 45, 0)) # Rotate cutting plane
          .box(20, 20, 20)
          .translate((block_pos_x - 5, block_pos_y, 0)) # Position cutter
          )
# Re-creating a cleaner chamfer using native chamfer operation
block_base = (cq.Workplane("XY")
         .box(block_length, block_width, block_height)
         .translate((block_pos_x, block_pos_y, block_height/2 + pcb_thickness/2))
         )
# Select edge to chamfer (top edge, negative x side)
# Finding the edge takes some logic, using a simple box for now is safer for robustness
# or applying chamfer to specific edge selector
try:
    block = block_base.edges(">Z and <X").chamfer(3.0)
except:
    block = block_base # Fallback if edge selection fails


# 3. Headers
# Create Header 1 (2x6)
h1_geo = create_pin_header(header1_rows, header1_cols)
h1_geo = h1_geo.translate((header1_pos_x, header1_pos_y, pcb_thickness/2))

# Create Header 2 (2x6)
h2_geo = create_pin_header(header2_rows, header2_cols)
h2_geo = h2_geo.translate((header2_pos_x, header2_pos_y, pcb_thickness/2))

# Create Header 3 (1x6 pointing down)
# Looking at the image, there are pins sticking out the bottom left.
# And corresponding solder pads/holes on top.
h3_geo = create_bottom_header(header3_rows, header3_cols)
h3_geo = h3_geo.translate((header3_pos_x, header3_pos_y, 0))

# Create holes in PCB for the bottom header
h3_hole_points = []
for r in range(header3_rows):
    for c in range(header3_cols):
        x_off = (c - (header3_cols-1)/2) * pitch
        y_off = (r - (header3_rows-1)/2) * pitch
        h3_hole_points.append((header3_pos_x + x_off, header3_pos_y + y_off))

pcb = (pcb.faces(">Z").workplane()
       .pushPoints(h3_hole_points)
       .hole(1.0) # Solder holes
       )


# 4. Combine everything
result = pcb.union(block).union(h1_geo).union(h2_geo).union(h3_geo)

# If running in CQ-editor this will show the result
# show_object(result)