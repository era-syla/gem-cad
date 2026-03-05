import cadquery as cq
import math

# Parameters for the model dimensions
block_size = 40.0
main_hole_dia = 15.0
slot_width = 24.0
slot_height = 10.0
small_hole_dia = 2.5
hex_flat_size = 6.0  # Distance across flats
hex_length = 60.0

# 1. Create the Main Block
# Start with a cube centered at the origin
block = cq.Workplane("XY").box(block_size, block_size, block_size)

# 2. Create the Circular Bore
# Select the right face (+X) and cut a hole through the block
block = block.faces(">X").workplane().hole(main_hole_dia)

# 3. Create the Rectangular Slot
# Select the left face (-Y) and cut a rectangular slot through the block
# This cuts perpendicular to the main bore, creating the internal intersection seen in the image
block = block.faces("<Y").workplane().rect(slot_width, slot_height).cutThruAll()

# 4. Create the Small Hole
# Select the right face (+X) again
# Shift the center diagonally to position the small hole (offset from the main bore)
block = block.faces(">X").workplane().center(8, 8).hole(small_hole_dia, depth=10)

# 5. Create the Hexagonal Shaft
# Calculate the diameter of the circumscribed circle for the hexagon
# Diameter = (Distance across flats) / cos(30 degrees)
hex_outer_dia = hex_flat_size / math.cos(math.radians(30))

# Create the shaft geometry
# Align it along the X-axis (parallel to the main bore) by sketching on YZ plane
shaft = cq.Workplane("YZ").polygon(6, hex_outer_dia).extrude(hex_length)

# Position the shaft
# Translate it to be "floating" near the block as shown in the image
# (Offset in X, Y, and Z relative to the block center)
shaft = shaft.translate((10, 50, 30))

# 6. Combine parts into the final result
result = block.union(shaft)