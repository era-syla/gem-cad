import cadquery as cq

# Dimensions for the long beam
beam_length = 150.0
beam_width = 8.0
beam_height = 8.0

# Dimensions for the rectangular block
block_length = 45.0
block_width = 25.0
block_height = 20.0

# Positioning coordinates (X, Y, Z)
# Beam is shifted to the right and towards the front (negative Y)
beam_position = (40, -30, 0)

# Block is shifted to the left and towards the back (positive Y)
block_position = (-20, 20, 0)

# Create the long beam geometry
beam = (cq.Workplane("XY")
        .box(beam_length, beam_width, beam_height)
        .translate(beam_position))

# Create the block geometry
block = (cq.Workplane("XY")
         .box(block_length, block_width, block_height)
         .translate(block_position))

# Combine the two objects into the final result
result = beam.union(block)