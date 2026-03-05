import cadquery as cq

# Parameters
width = 50.0
height = 110.0
thickness = 5.0

fillet_radius_top = 12.0
fillet_radius_bottom = 5.0

slot_width = 6.0
slot_length = 60.0
slot_overlap = 2.0  # Extra length to ensure clean cut through top edge

hole_diameter = 5.0
hole_spacing = 26.0
hole_height_from_bottom = 12.0

# 1. Create base plate centered on origin
result = cq.Workplane("XY").box(width, height, thickness)

# 2. Add fillets
# Select vertical edges (parallel to Z)
# Top corners are in positive Y, bottom in negative Y
result = result.edges("|Z and >Y").fillet(fillet_radius_top)
result = result.edges("|Z and <Y").fillet(fillet_radius_bottom)

# 3. Cut vertical slot
# Calculate center and size to cut from top edge downwards
# Top edge of part is at Y = height/2
# Slot bottom is at Y = height/2 - slot_length
# We add overlap to the top to ensure the slot is open
cut_height = slot_length + slot_overlap
cut_center_y = (height / 2) - (slot_length / 2) + (slot_overlap / 2)

result = (result.faces(">Z")
          .workplane()
          .moveTo(0, cut_center_y)
          .rect(slot_width, cut_height)
          .cutThruAll())

# 4. Cut mounting holes
hole_y_pos = (-height / 2) + hole_height_from_bottom

result = (result.faces(">Z")
          .workplane()
          .pushPoints([
              (-hole_spacing / 2, hole_y_pos),
              (hole_spacing / 2, hole_y_pos)
          ])
          .hole(hole_diameter))