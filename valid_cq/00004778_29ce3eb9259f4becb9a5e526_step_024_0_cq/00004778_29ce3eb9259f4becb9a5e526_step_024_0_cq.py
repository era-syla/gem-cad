import cadquery as cq

# --- Parameter Definitions ---
plate_width = 152.0   # Estimated total width based on standard robotics parts (often ~120-160mm)
plate_height = 96.0   # Estimated total height (often ~80-100mm)
plate_thickness = 3.0 # Standard thickness for mounting plates
corner_radius = 4.0   # Radius for the outer corners

# Hole parameters
small_hole_diam = 3.2 # Clearance for M3 screws
large_hole_diam = 4.2 # Clearance for M4 screws or bearing fits
slot_width = 3.2      # Width of the slot cutouts
slot_length_long = 24.0
slot_length_short = 12.0

# --- Grid Logic ---
# The pattern appears to be based on an 8mm or 16mm grid, typical in robotics (like goBILDA or TETRIX).
# Let's break down the hole coordinates based on visual symmetry and common spacing.

# 1. Main 3x3 grid of large holes (center section)
# Center is (0,0). Let's assume an 8mm or 16mm pitch. 
# Looking at the density, 8mm spacing seems plausible for the small holes, 
# making the larger ones spaced wider (e.g., 32mm or 24mm).

large_hole_positions = [
    # Central column
    (0, 16), (0, 32),
    (0, -16), (0, -32),
    # Side columns (inner)
    (16, 8), (16, 24), (16, 40),
    (-16, 8), (-16, 24), (-16, 40),
    (-16, -8), (-16, -24), (-16, -40),
    (16, -8), (16, -24), (16, -40),
    # Far side columns
    (32, 16), (32, 32),
    (-32, 16), (-32, 32),
    (32, -16), (32, -32),
    (-32, -16), (-32, -32),
]

# There are larger holes on the far right/left edges too
edge_large_holes = [
    (64, 32), (64, 16), (64, -16), (64, -32),
    (-64, 32), (-64, 16), (-64, -16), (-64, -32),
]

# 2. Small Hole Grid
# These fill the gaps.
small_hole_positions = [
    # Center
    (0, 0),
    # Diagonal fillers
    (8, 0), (-8, 0),
    (8, 16), (-8, 16), (8, -16), (-8, -16),
    (8, 32), (-8, 32), (8, -32), (-8, -32),
    
    (24, 0), (-24, 0),
    (24, 16), (-24, 16), (24, -16), (-24, -16),
    (24, 32), (-24, 32), (24, -32), (-24, -32),
    
    (40, 0), (-40, 0),
    (40, 8), (-40, 8), (40, -8), (-40, -8),
    (40, 24), (-40, 24), (40, -24), (-40, -24),
    (40, 40), (-40, 40), (40, -40), (-40, -40),
    
    (48, 16), (-48, 16), (48, -16), (-48, -16),
    (48, 32), (-48, 32), (48, -32), (-48, -32),
    
    (56, 8), (-56, 8), (56, -8), (-56, -8),
    (56, 24), (-56, 24), (56, -24), (-56, -24),
    (56, 40), (-56, 40), (56, -40), (-56, -40),
    
    (72, 8), (-72, 8), (72, -8), (-72, -8),
    (72, 24), (-72, 24), (72, -24), (-72, -24),
]

# 3. Slots
# There are pairs of slots at the top and bottom center
slot_positions_long = [
    (0, 24), (0, -24) # These need to be horizontal slots, shifted slightly
]
# Adjusting slot positions based on image. The slots are above/below the central cluster.
# The slots look like they are centered horizontally at x=0.
top_long_slot_center = (0, 24) 
bottom_long_slot_center = (0, -24)

# Looking closer, the slots are actually spaced around the center column.
# Let's use specific coordinates for the slot centers.
slot_centers = [
    (0, 28), (0, -28),  # Central long slots
    (32, 44), (-32, 44), # Shorter outer slots top
    (32, -44), (-32, -44) # Shorter outer slots bottom
]

# --- Construction ---

# Base Plate
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Cut Large Holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(large_hole_positions)
    .hole(large_hole_diam)
    .pushPoints(edge_large_holes)
    .hole(large_hole_diam)
)

# Cut Small Holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(small_hole_positions)
    .hole(small_hole_diam)
)

# Cut Slots
# Central Long Slots
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(0, 28), (0, -28)])
    .slot2D(24, slot_width) # Length, diameter/width
    .cutThruAll()
)

# Diagonal/Side Short Slots (Top and Bottom)
# These slots are angled or just offset. In the image, they look horizontal but offset.
# Top left/right slots
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-24, 40), (24, 40), (-24, -40), (24, -40)])
    .slot2D(12, slot_width)
    .cutThruAll()
)

# Final refinement to match visual hole pattern exactly
# The previous coordinate generation was algorithmic, let's refine specific features seen in image.
# The image shows specific horizontal slots.

# Re-creating the slots specifically to match the image accurately
# There is a central horizontal slot pair.
# There are flanking horizontal slot pairs above/below the main block.

# Clean up previously defined slot cuts and re-do with explicit placements
# Re-importing logic to keep the code block clean for output

# Base Plate Reset
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# --- Detailed Coordinate Mapping based on 8mm/16mm standard spacing ---

# Group 1: The larger diameter holes (approx 4-5mm)
# These form a "cross" shape and outer edges
large_holes = [
    # Vertical Center Column
    (0, 16), (0, 32), (0, -16), (0, -32),
    # Inner Columns (x= +/- 16)
    (16, 8), (16, 24), (16, 40),
    (-16, 8), (-16, 24), (-16, 40),
    (16, -8), (16, -24), (16, -40),
    (-16, -8), (-16, -24), (-16, -40),
    # Mid Columns (x= +/- 32)
    (32, 0), (32, 16), (32, 32),
    (-32, 0), (-32, 16), (-32, 32),
    (32, -16), (32, -32),
    (-32, -16), (-32, -32),
    # Outer Columns (x= +/- 48) - mostly small holes, checking image...
    # Far Edge Columns (x= +/- 64 approx)
    (64, 32), (64, 24), (64, -24), (64, -32),
    (-64, 32), (-64, 24), (-64, -24), (-64, -32)
]

# Group 2: The smaller diameter holes (approx 3mm)
# These fill the grid pattern
small_holes = [
    (0, 0), # Center
    (0, 8), (0, -8), # Close center vertical
    # x = +/- 8
    (8, 0), (8, 16), (8, 32), (8, -16), (8, -32),
    (-8, 0), (-8, 16), (-8, 32), (-8, -16), (-8, -32),
    # x = +/- 24
    (24, 0), (24, 16), (24, 32), (24, -16), (24, -32),
    (-24, 0), (-24, 16), (-24, 32), (-24, -16), (-24, -32),
    # x = +/- 40
    (40, 0), (40, 8), (40, 24), (40, 40), (40, -8), (40, -24), (40, -40),
    (-40, 0), (-40, 8), (-40, 24), (-40, 40), (-40, -8), (-40, -24), (-40, -40),
    # x = +/- 48
    (48, 16), (48, 32), (48, -16), (48, -32),
    (-48, 16), (-48, 32), (-48, -16), (-48, -32),
    # x = +/- 56
    (56, 8), (56, 24), (56, 40), (56, -8), (56, -24), (56, -40),
    (-56, 8), (-56, 24), (-56, 40), (-56, -8), (-56, -24), (-56, -40),
    # x = +/- 72 (near edge)
    (72, 8), (72, 24), (72, -8), (72, -24),
    (-72, 8), (-72, 24), (-72, -8), (-72, -24),
]

# Apply Holes
result = result.faces(">Z").workplane().pushPoints(large_holes).hole(large_hole_diam)
result = result.faces(">Z").workplane().pushPoints(small_holes).hole(small_hole_diam)

# Apply Slots
# Central slots (horizontal)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(0, 24), (0, -24)])
    .slot2D(32, slot_width) # Central long slots
    .cutThruAll()
)

# Offset Slots (horizontal)
# Located roughly at x=+/- 24, y=+/- 42
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (24, 42), (-24, 42),
        (24, -42), (-24, -42)
    ])
    .slot2D(16, slot_width)
    .cutThruAll()
)