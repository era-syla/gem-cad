import cadquery as cq

# Model Parameters
unit_size = 10.0      # Width and height of the blocks
pitch = 10.0          # Spacing between hole centers
hole_diameter = 5.2   # Diameter of the through-holes
gap = 15.0            # Spacing between the blocks

# Configuration: Number of holes for each block in the sequence
block_definitions = [4, 3, 2, 1]

solids = []
current_position_offset = 0.0

for n_holes in block_definitions:
    length = n_holes * pitch
    
    # 1. Create the base rectangular block
    # Centered at (0,0,0) locally
    block = cq.Workplane("XY").box(length, unit_size, unit_size)
    
    # 2. Calculate hole center coordinates relative to the block center
    # Evenly spaced by 'pitch' and centered along the length (X-axis)
    hole_x_positions = [(i - (n_holes - 1) / 2.0) * pitch for i in range(n_holes)]
    hole_points = [(x, 0) for x in hole_x_positions]
    
    # 3. Create vertical holes (Z-axis)
    # Select the top face (>Z), push points, and cut through
    block = block.faces(">Z").workplane().pushPoints(hole_points).hole(hole_diameter)
    
    # 4. Create horizontal holes (Y-axis)
    # Select the front/back face (>Y), push points, and cut through
    block = block.faces(">Y").workplane().pushPoints(hole_points).hole(hole_diameter)
    
    # 5. Position the block in the assembly
    # Calculate the center position for the current block along a diagonal
    center_dist = current_position_offset + length / 2.0
    
    # Translate the block to its final position (x, y, 0)
    # We offset X and Y equally to create the diagonal arrangement shown in the image
    block = block.translate((center_dist, center_dist, 0))
    
    solids.append(block)
    
    # Update the starting offset for the next block
    current_position_offset += length + gap

# Combine all generated solids into a single Compound object
result = solids[0]
for s in solids[1:]:
    result = result.union(s)