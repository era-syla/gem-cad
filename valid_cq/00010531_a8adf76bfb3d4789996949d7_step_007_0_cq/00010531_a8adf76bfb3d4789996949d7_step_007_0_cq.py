import cadquery as cq

# -- Parametric Dimensions --
plate_length = 60.0
plate_width = 30.0
plate_thickness = 5.0

block_length = 15.0
block_width = 15.0
block_height = 10.0 # Height above the plate surface (total height = 15)

hole_diameter = 6.0
hole_offset_x = 10.0 # Distance from the non-block end
hole_offset_y = 0.0  # Centered on width

# -- Modeling Steps --

# 1. Create the base plate
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Add the raised block on one end
# We select the top face, work relative to the far X edge, and extrude up
block = (
    base.faces(">Z")
    .workplane()
    .center(plate_length/2 - block_length/2, 0) # Move center to the right end
    .rect(block_length, block_width)            # Create the rectangle sketch
    .extrude(block_height)
)

# 3. Create the hole on the opposite end
# We select the main body, choose the top face, and cut
result = (
    block.faces(">Z").workplane() # Workplane on top of the block isn't right, let's go back to base level or use coordinates
    .workplane(offset=-block_height) # Go back down to the plate surface level
    .center(-plate_length/2 + hole_offset_x, hole_offset_y) # Move to the left end
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Alternatively, a cleaner single-chain approach:
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    
    # Add the block
    .faces(">Z")
    .workplane()
    .center(plate_length/2 - block_length/2, 0)
    .rect(block_length, block_length) # Assuming square block based on visual
    .extrude(block_height)
    
    # Add the hole
    .faces(">Z[1]") # Select the lower top face (the plate surface, not the block top)
    .workplane()
    .center(-plate_length/2 + hole_offset_x, 0)
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Export or visualization helper (standard practice for these requests)
# result variable is already set.