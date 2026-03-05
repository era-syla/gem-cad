import cadquery as cq

# Base dimensions
base_length = 80
base_width = 40
base_height = 10

# Upper block dimensions
upper_length = 80
upper_width = 20
upper_height = 20

# Slot dimensions (cut through the front of the base/upper)
slot_width = 40
slot_height = 20
slot_depth = 20  # depth into the shape from front

# Create the base block
base = cq.Workplane("XY").box(base_length, base_width, base_height, centered=(True, True, False))

# Create the upper block sitting on top of the base, centered in length, offset to back in width
upper = cq.Workplane("XY").box(upper_length, upper_width, upper_height, centered=(True, True, False))
upper = upper.translate((0, (base_width - upper_width) / 2, base_height))

# Combine base and upper
combined = base.union(upper)

# Create a slot cut - rectangular channel going through from front
# The slot is centered in X, open at the front face, cuts through base height into upper
slot = cq.Workplane("XY").box(slot_width, slot_depth, slot_height, centered=(True, True, False))
slot = slot.translate((0, -base_width/2, base_height))

# Cut the slot from the combined shape
result = combined.cut(slot)