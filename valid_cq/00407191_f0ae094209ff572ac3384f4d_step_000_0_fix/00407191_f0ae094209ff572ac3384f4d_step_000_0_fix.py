import cadquery as cq

# Parameters
rod_radius = 1.5
rod_length = 200.0
block_width = 6.0        # across X
block_length = 20.0      # along Z
block_height = 3.0       # in +Y from cylinder top
groove_width = 0.5
groove_spacing = 0.7
groove_depth = 1.0
num_grooves = 3

# Build the main cylindrical rod
rod = cq.Workplane("XY").circle(rod_radius).extrude(rod_length)

# Build the rail block on the side of the rod
# Place block so that its bottom touches the top of cylinder (at Y = rod_radius)
block = (
    cq.Workplane("XZ", origin=(0, rod_radius, 0))
      .rect(block_width, block_length)
      .extrude(block_height)
)

# Combine rod and block
result = rod.union(block)

# Cut longitudinal grooves on the top of the block
# We cut into the +Y face of the block (face normal +Y)
# The workplane on that face has local X = global X, local Y = global Z
# Prepare offsets for the grooves along X, centered in Z
x_start = -block_width/2 + groove_spacing + groove_width/2
x_offsets = [(x_start + i*(groove_width + groove_spacing), 0) for i in range(num_grooves)]

# Perform the cuts
result = (
    result
      .faces(">Y")
      .workplane(centerOption="CenterOfBoundBox")
      .pushPoints(x_offsets)
      .rect(groove_width, block_length + 1)   # length slightly longer to ensure full cut
      .cutBlind(-groove_depth)
)

# 'result' now holds the final solid
