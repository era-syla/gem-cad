import cadquery as cq

# --- Parametric Dimensions ---
# Overall Box Dimensions
box_width = 80.0
box_depth = 100.0
box_height = 20.0
chamfer_size = 3.0

# Split Line Position (relative to depth)
split_ratio = 0.4  # Split occurs roughly 40% along the depth
split_gap = 0.2    # Visual gap for the parting line

# LED Indicators (top surface)
led_width = 6.0
led_depth = 2.0
led_height = 0.5   # slightly raised or cutout
led_spacing = 4.0  # center-to-center spacing
num_leds = 3

# Front Port (USB-like)
port_width = 12.0
port_height = 6.0
port_rim_thickness = 1.0
port_depth = 2.0  # How deep the recess goes
tongue_width = 8.0
tongue_height = 1.5
tongue_protrusion = 1.0

# --- Geometry Construction ---

# 1. Base Block with Chamfered Edges
# Create the main box centered on XY plane
base = cq.Workplane("XY").box(box_width, box_depth, box_height)

# Apply chamfers to the vertical edges
# We select edges parallel to Z
base = base.edges("|Z").chamfer(chamfer_size)

# Apply smaller chamfers/fillets to top and bottom edges for a finished look
# Note: The image shows fairly sharp top/bottom edges, but the corners are chamfered.
# The corner chamfers are already done. 

# 2. Parting Line (The split across the top)
# We simulate this by cutting a very thin groove or just modeling it as a feature.
# Based on the image, it looks like a physical separation. Let's make a groove.
split_plane_y = (box_depth / 2) - (box_depth * split_ratio)

parting_line = (
    cq.Workplane("XY")
    .transformed(offset=(0, split_plane_y, box_height/2))
    .box(box_width + 10, split_gap, box_height/2) # Cut only top half for visual
)

# 3. LED Indicators
# Located on the top face, centered X, near the parting line
leds = (
    cq.Workplane("XY")
    .workplane(offset=box_height/2)
    .center(0, split_plane_y - 8.0) # Position slightly behind the split line
)

# Create the 3 rectangular cutouts/extrusions
led_cutout = (
    leds
    .rarray(1, led_spacing, 1, num_leds)
    .rect(led_width, led_depth)
    .extrude(-led_height) # Cut into the surface
)

# 4. Front Port (USB-A style recess)
# Locate on the front face (min Y)
front_face = base.faces("<Y").workplane()

# Create the main rectangular recess
port_recess = (
    front_face
    .rect(port_width + 2*port_rim_thickness, port_height + 2*port_rim_thickness)
    .extrude(-0.5) # Shallow rim cut
    .faces(">Z[1]") # Select the bottom of that shallow cut (technically local Z is inward)
    .workplane()
    .rect(port_width, port_height)
    .cutBlind(-port_depth) # Cut deeper
)

# Add the "tongue" inside the port
tongue = (
    front_face
    .workplane(offset=-port_depth) # Start deep inside
    .rect(tongue_width, tongue_height)
    .extrude(port_depth - 0.5) # Extrude back out, but not flush
)

# 5. Combine Operations
# Start with base
result = base

# Subtract the parting line groove (optional, visual detail)
# For a solid block representation, we might just cut it.
result = result.cut(parting_line)

# Subtract LEDs
result = result.cut(led_cutout)

# Create the Port feature
# We need to recreate the port logic on the modified 'result' object
# Or easier: create a separate "tool" for the port removal and addition

# Let's do the port cut directly on the result
result = (
    result
    .faces("<Y").workplane()
    .rect(port_width + 2*port_rim_thickness, port_height + 2*port_rim_thickness)
    .cutBlind(-0.5) # Rim depth
    .faces("<Y").workplane(offset=-0.5) # Move to new face depth
    .rect(port_width, port_height)
    .cutBlind(-port_depth) # Main cavity
)

# Add the tongue back in
# We need to orient correctly relative to the front face
tongue_obj = (
    cq.Workplane("XZ") # Front plane orientation
    .workplane(offset=-box_depth/2 + 0.5) # Align with inside of recess
    .rect(tongue_width, tongue_height)
    .extrude(port_depth - 0.5)
)

result = result.union(tongue_obj)

# Add the parting line on the side walls? The image shows the line going all around.
# Let's do a simple cut for the parting line across the whole object to look like two pieces assembled.
splitter = (
    cq.Workplane("XY")
    .transformed(offset=(0, split_plane_y, 0))
    .box(box_width + 20, split_gap, box_height + 20)
)
# Instead of fully splitting, let's just make a small indentation groove all around
groove_depth = 0.3
groove_cutter = (
    cq.Workplane("XY")
    .transformed(offset=(0, split_plane_y, 0))
    .box(box_width + 20, split_gap, box_height + 20)
)
# Create a shell of the cutter to subtract only the surface
inner_cutter = (
    cq.Workplane("XY")
    .transformed(offset=(0, split_plane_y, 0))
    .box(box_width + 20 - 2*groove_depth, split_gap, box_height + 20 - 2*groove_depth)
)
# Actually, a simple way is just to cut the shallow groove on top/sides
groove = (
    cq.Workplane("XY")
    .transformed(offset=(0, split_plane_y, 0))
    .box(box_width+10, split_gap, box_height+10)
)

# Re-apply the chamfer logic to the groove area to ensure clean cuts if needed, 
# but simple subtraction works best for visual.
# To keep it simple and robust:
result = result.cut(groove_cutter) # This splits it into two solids
# If we want one solid with a groove, we need to bridge them inside. 
# But for a CAD representation of an assembly, two solids is often correct.
# However, the prompt asks for "A variable called result containing the final geometry".
# CadQuery compounds can hold multiple solids.

# Refinement: The image shows a 'step' or seam.
# Let's assume it's a single solid with a cosmetic groove.
# We will create an inner core that connects them to keep it one object if desired, 
# or just leave it as a Compound of two solids. The variable 'result' handles compounds fine.
