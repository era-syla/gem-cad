import cadquery as cq

# --- Parameters ---

# Large Frame Parameters
lf_size = 200.0
lf_height = 15.0
lf_wall_thickness = 15.0
lf_fillet_radius = 20.0
lf_position = (100, 0, 0)

# Small Square Frame Parameters
sf_size = 45.0
sf_height = 12.0
sf_wall_thickness = 4.0
sf_position = (-40, 20, 0)

# Circular Ring Parameters
ring_diameter = 45.0
ring_height = 12.0
ring_wall_thickness = 4.0
ring_position = (-40, -35, 0)

# Small Block Parameters
block_length = 25.0
block_width = 10.0
block_height = 10.0
block_position = (-85, 20, 0)
hole_diameter = 2.0
hole_spacing = 6.0

# --- Geometry Construction ---

# 1. Large Rounded Frame
# Construct the outer shape with fillets
large_frame_outer = (
    cq.Workplane("XY")
    .rect(lf_size, lf_size)
    .extrude(lf_height)
    .edges("|Z")
    .fillet(lf_fillet_radius)
)

# Construct the inner cutter shape to maintain constant wall thickness
# Inner radius = Outer radius - Wall thickness
inner_fillet = lf_fillet_radius - lf_wall_thickness
if inner_fillet <= 0:
    inner_fillet = 0.1 # Ensure valid fillet radius

large_frame_inner = (
    cq.Workplane("XY")
    .rect(lf_size - 2 * lf_wall_thickness, lf_size - 2 * lf_wall_thickness)
    .extrude(lf_height)
    .edges("|Z")
    .fillet(inner_fillet)
)

# Create the hollow frame and move to position
large_frame = large_frame_outer.cut(large_frame_inner).translate(lf_position)

# 2. Small Square Frame (Sharp corners)
small_frame = (
    cq.Workplane("XY")
    .rect(sf_size, sf_size)
    .rect(sf_size - 2 * sf_wall_thickness, sf_size - 2 * sf_wall_thickness)
    .extrude(sf_height)
    .translate(sf_position)
)

# 3. Circular Ring
ring = (
    cq.Workplane("XY")
    .circle(ring_diameter / 2.0)
    .circle((ring_diameter / 2.0) - ring_wall_thickness)
    .extrude(ring_height)
    .translate(ring_position)
)

# 4. Small Block with Holes
# Create block centered at origin, then shift up so bottom is at Z=0
block_base = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
    .translate((0, 0, block_height / 2.0))
)

# Add holes to the top face
block = (
    block_base
    .faces(">Z").workplane()
    .rarray(hole_spacing, 1, 3, 1)  # Array of 3 holes along X
    .hole(hole_diameter)
    .translate(block_position)
)

# --- Final Assembly ---
result = large_frame.union(small_frame).union(ring).union(block)