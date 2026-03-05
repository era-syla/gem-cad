import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
width = 50.0       # Width of the square footprint
depth = 50.0       # Depth of the square footprint
total_height = 100.0 # Approximate total height

# Base block dimensions
base_height = 50.0 

# Top block (main body) dimensions
top_block_height = 40.0

# Cap dimensions
cap_height = 10.0

# Bolt hole parameters (for the cap)
bolt_diameter = 5.0
bolt_inset = 8.0   # Distance from edge to hole center
bolt_depth = 15.0  # Depth of the hole

# Side port parameters (circular protrusion)
side_port_diameter = 25.0
side_port_stickout = 5.0
side_port_z_offset = base_height + (top_block_height / 2.0) # Centered on top block

# Front hole parameters
front_hole_diameter = 8.0
front_hole_z_offset = base_height / 2.0 # Centered on base block

# --- Geometry Construction ---

# 1. Base Block
base = cq.Workplane("XY").box(width, depth, base_height)

# 2. Top Block (Body)
# Positioned on top of the base
top_body = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2 + top_block_height/2)
    .box(width, depth, top_block_height)
)

# 3. Top Cap
# Positioned on top of the top block
cap = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2 + top_block_height + cap_height/2)
    .box(width, depth, cap_height)
)

# 4. Combine the main blocks
result = base.union(top_body).union(cap)

# 5. Add Side Port (Protrusion)
# On the left face (looking from standard isometric view in CadQuery)
# Let's assume standard view: X is right-front, Y is left-back. 
# Based on the image, there is a protrusion on the left side.
result = (
    result.faces("<X")
    .workplane(centerOption="CenterOfMass")
    .center(0, (top_block_height/2 + cap_height + base_height)/2 - side_port_z_offset) # Adjustment to align with top block vertical center
    .circle(side_port_diameter / 2)
    .extrude(side_port_stickout)
)

# 6. Add Bolt Holes on Top Cap
# Pattern of 4 holes
result = (
    result.faces(">Z")
    .workplane()
    .rect(width - 2*bolt_inset, depth - 2*bolt_inset, forConstruction=True)
    .vertices()
    .hole(bolt_diameter, depth=bolt_depth)
)

# 7. Add Front Hole
# Small circular hole on the lower block front face
result = (
    result.faces(">Y") # Front face usually corresponds to >Y or <Y depending on orientation, picking >Y based on visual logic of 'front'
    .workplane(centerOption="CenterOfMass")
    .center(0, -(total_height/2 - front_hole_z_offset)) # Move down to the base block center
    .circle(front_hole_diameter / 2)
    .cutBlind(-width/2) # Cut into the block
)

# If the "front" hole is actually on the side face relative to the protrusion:
# The image shows the protrusion on the left (-X usually) and the small hole on the right face visible (+Y usually).
# The code above aligns with this: Protrusion on <X, Hole on >Y.