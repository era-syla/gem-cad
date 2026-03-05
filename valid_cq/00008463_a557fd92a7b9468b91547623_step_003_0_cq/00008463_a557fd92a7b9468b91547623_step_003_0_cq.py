import cadquery as cq

# --- Parameter Definitions ---
# PCB Dimensions
pcb_thickness = 1.6
main_width = 80.0
main_height = 100.0
cutout_bottom_right_w = 20.0
cutout_bottom_right_h = 20.0
corner_radius = 2.0

# Connector/Header Dimensions (Top Left)
header_length = 50.0
header_width = 8.0
header_height = 8.0
pin_length = 10.0
pin_width = 0.6
num_pins = 12
pin_pitch = 2.54

# Large Component (Relay/Connector housing)
block_width = 20.0
block_depth = 25.0
block_height = 20.0
block_pos_x = -30  # Relative to center
block_pos_y = 15   # Relative to center

# Mounting Holes
mount_hole_dia = 3.2
mount_hole_pad_dia = 6.0
mount_hole_locations = [
    (-main_width/2 + 5, -main_height/2 + 5),   # Bottom Left
    (main_width/2 - 25, -main_height/2 + 5),   # Bottom Right (inset due to cutout)
    (main_width/2 - 5, main_height/2 - 25),    # Top Right (inset)
]

# Grid of via holes (simplified representation)
grid_hole_dia = 0.8
grid_spacing = 2.54
grid_cols = 20
grid_rows = 30

# --- Geometry Construction ---

# 1. Base PCB Shape
# Start with a rectangle and cut away the bottom right corner
pcb = (
    cq.Workplane("XY")
    .rect(main_width, main_height)
    .extrude(pcb_thickness)
)

# Create the cutout shape on the bottom right
cutout = (
    cq.Workplane("XY")
    .rect(cutout_bottom_right_w * 2, cutout_bottom_right_h * 2) # Make it large enough to intersect
    .translate((main_width/2, -main_height/2, 0))
    .extrude(pcb_thickness)
)

# Apply the cutout
pcb = pcb.cut(cutout)

# Add fillets to corners (simplified approach: selecting vertical edges)
# We need to be careful with selection to avoid filleting the cutout sharp corner if unintended,
# but usually PCBs have rounded outer corners.
try:
    pcb = pcb.edges("|Z").fillet(corner_radius)
except:
    pass # Sometimes fillet fails on complex topology, fallback to sharp corners

# 2. Add Mounting Holes
pcb = pcb.faces(">Z").workplane().pushPoints(mount_hole_locations).hole(mount_hole_dia)

# Add "tinned" pads around mounting holes (visual detail - slight extrusion)
pads = (
    cq.Workplane("XY")
    .pushPoints(mount_hole_locations)
    .circle(mount_hole_pad_dia/2)
    .extrude(pcb_thickness + 0.1) # Slightly taller than PCB
)
pcb = pcb.union(pads)
# Re-drill through pads
pcb = pcb.faces(">Z").workplane().pushPoints(mount_hole_locations).hole(mount_hole_dia)


# 3. Create the Header Component (Top Left)
# Main plastic body
header_body = (
    cq.Workplane("XY")
    .rect(header_length, header_width)
    .extrude(header_height)
    .translate((-main_width/2 + header_length/2 - 5, main_height/2 - header_width/2 + 5, pcb_thickness))
)

# Pins
pin_pts = []
start_x = -header_length/2 + pin_pitch/2
for i in range(num_pins):
    pin_pts.append((start_x + i * pin_pitch, 0))

pins = (
    cq.Workplane("XY")
    .pushPoints(pin_pts)
    .rect(pin_width, pin_width)
    .extrude(header_height + 4) # Stick out top
    .translate((-main_width/2 + header_length/2 - 5, main_height/2 - header_width/2 + 5, pcb_thickness))
)

# Right angle part of pins (sticking out side)
pins_side = (
    cq.Workplane("YZ")
    .pushPoints([(0, header_height/2)]) # Relative to local plane
    .rect(pin_width, pin_width)
    .extrude(5)
    .rotate((0,0,0), (0,0,1), 90) # Orient correctly
    # We create one and pattern/translate, or just bulk create. simpler to create a block of pins.
)
# Let's simplify the pin representation to just the vertical array for robustness
header_assembly = header_body.union(pins)

# Add detail to header (screw terminals visual)
screw_holes = (
    cq.Workplane("XY")
    .pushPoints(pin_pts)
    .circle(1.0)
    .extrude(header_height)
    .translate((-main_width/2 + header_length/2 - 5, main_height/2 - header_width/2 + 5, pcb_thickness + header_height - 2))
)
header_assembly = header_assembly.cut(screw_holes)


# 4. Create the Large Block Component (Relay/Socket)
# This sits perpendicular to the header
large_block = (
    cq.Workplane("XY")
    .box(block_width, block_depth, block_height, centered=(True, True, False))
    .translate((block_pos_x, block_pos_y, pcb_thickness))
)

# Add a smaller extension to the block (as seen in image)
block_ext = (
    cq.Workplane("XY")
    .box(block_width + 5, 10, 15, centered=(True, True, False))
    .translate((block_pos_x, block_pos_y + 10, pcb_thickness))
)
large_block = large_block.union(block_ext)

# 5. Grid of Small Holes (Vias/Proto-board area)
# We will create a pattern of small cylinders and cut them
# To optimize performance, we'll do a few distinct columns/groups rather than a massive 1000-hole array
via_columns_x = [-main_width/2 + 10, -main_width/2 + 20, 0, 10, main_width/2 - 10]
via_y_range = range(int(-main_height/2 + 15), int(main_height/2 - 30), 3)

via_locations = []
for x in via_columns_x:
    for y in via_y_range:
        via_locations.append((x, y))

# Add a specific group on the top right
for x in range(int(main_width/2 - 25), int(main_width/2 - 5), 3):
    for y in range(int(main_height/2 - 40), int(main_height/2 - 10), 3):
        via_locations.append((x, y))

pcb_with_holes = (
    pcb.faces(">Z").workplane()
    .pushPoints(via_locations)
    .hole(grid_hole_dia)
)

# 6. Combine all parts
result = pcb_with_holes.union(header_assembly).union(large_block)

# Export or Render
if 'show_object' in globals():
    show_object(result)