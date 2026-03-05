import cadquery as cq

# Main plate dimensions
plate_length = 300
plate_width = 100
plate_thickness = 8

# Create the main base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Add connector slots on the left end (short edge)
slot_width = 4
slot_height = 6
slot_depth = 10
num_slots = 4
slot_spacing = plate_width / (num_slots + 1)

for i in range(num_slots):
    y_pos = -plate_width/2 + slot_spacing * (i + 1)
    result = (result
              .faces("<X")
              .workplane()
              .center(y_pos, 0)
              .rect(slot_width, slot_height)
              .cutBlind(-slot_depth))

# Add mounting holes near corners
hole_diameter = 4
hole_inset_x = 15
hole_inset_y = 12

hole_positions = [
    (-plate_length/2 + hole_inset_x, -plate_width/2 + hole_inset_y),
    (-plate_length/2 + hole_inset_x,  plate_width/2 - hole_inset_y),
    ( plate_length/2 - hole_inset_x, -plate_width/2 + hole_inset_y),
    ( plate_length/2 - hole_inset_x,  plate_width/2 - hole_inset_y),
]

result = (result
          .faces(">Z")
          .workplane()
          .pushPoints(hole_positions)
          .hole(hole_diameter))

# Add raised connector blocks on the top surface
# These are the T-shaped/arrow-shaped features visible in the image
connector_positions = [
    (20,  20),
    (20, -20),
    (60,  20),
    (60, -20),
    (0,    0),
    (100,  20),
    (100, -20),
    (-40,  20),
    (-40, -20),
]

block_w = 10
block_h = 10
block_t = 6

for (cx, cy) in connector_positions:
    # Main block body
    result = (result
              .faces(">Z")
              .workplane()
              .center(cx, cy)
              .rect(block_w, block_h)
              .extrude(block_t))
    
    # Add a smaller raised nub on top of each block
    nub_w = 5
    nub_h = 5
    nub_t = 3
    result = (result
              .faces(">Z")
              .workplane()
              .center(cx, cy)
              .rect(nub_w, nub_h)
              .extrude(nub_t))

# Add small wing features on the sides of some blocks (T-shape)
wing_positions = [
    (20,  20),
    (60,  20),
    (100, 20),
]

for (cx, cy) in wing_positions:
    # Left wing
    result = (result
              .faces(">Z")
              .workplane()
              .center(cx - block_w/2 - 3, cy)
              .rect(4, 4)
              .extrude(block_t))
    # Right wing
    result = (result
              .faces(">Z")
              .workplane()
              .center(cx + block_w/2 + 3, cy)
              .rect(4, 4)
              .extrude(block_t))

# Add small holes/dots on the plate surface (visible in image)
small_hole_positions = [
    (-100, 30),
    (-100, -30),
    (130, 30),
    (130, -30),
]

result = (result
          .faces(">Z")
          .workplane()
          .pushPoints(small_hole_positions)
          .hole(3, 4))