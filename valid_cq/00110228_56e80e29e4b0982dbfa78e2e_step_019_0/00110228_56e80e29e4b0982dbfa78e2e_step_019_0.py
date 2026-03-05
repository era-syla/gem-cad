import cadquery as cq

# Parameters defining the geometry
plate_length = 90.0
plate_width = 30.0
plate_thickness = 3.0

block_length = 36.0
block_width = 20.0
block_height = 14.0

# Calculate geometric offsets
# Block is positioned on the left side of the plate and offset to the back
# to leave room for the mounting holes on the front ledge.
block_center_x = -plate_length/2 + 10 + block_length/2  # Left-aligned with margin
block_center_y = plate_width/2 - block_width/2          # Flush with back edge

hole_diameter = 5.0
hole_spacing = 26.0
# Holes are centered on the front ledge strip
hole_y_pos = ((-plate_width/2) + (block_center_y - block_width/2)) / 2 

# 1. Create the base plate
# Centered at origin, so Z extends from -plate_thickness/2 to +plate_thickness/2
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the rectangular block
# Positioned on the top face of the plate (Z = plate_thickness/2)
block = (cq.Workplane("XY")
         .workplane(offset=plate_thickness/2)
         .center(block_center_x, block_center_y)
         .box(block_length, block_width, block_height, centered=(True, True, False)))

# 3. Combine base and block
result = base.union(block)

# 4. Cut the mounting holes
# Define hole locations relative to the block position
hole_locations = [
    (block_center_x - hole_spacing/2, hole_y_pos),
    (block_center_x + hole_spacing/2, hole_y_pos)
]

# Select the bottom face and drill through
result = (result
          .faces("<Z")
          .workplane()
          .pushPoints(hole_locations)
          .hole(hole_diameter))
