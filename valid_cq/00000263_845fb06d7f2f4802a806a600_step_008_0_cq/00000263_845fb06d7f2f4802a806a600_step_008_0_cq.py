import cadquery as cq

# --- Parameter Definitions ---
# Shaft dimensions
shaft_diameter = 4.0
shaft_length = 12.0
shaft_tip_fillet = 0.5  # Slight rounding at the bottom of the shaft

# Washer/Flange dimensions
washer_diameter = 10.0
washer_thickness = 1.5

# Head dimensions (Pan head style)
head_diameter = 6.0
head_height = 2.0
head_fillet = 0.5 # Rounding on the top edge of the head

# Slot dimensions
slot_width = 1.0
slot_depth = 1.0

# --- Modeling ---

# 1. Create the main shaft
# We start from the origin and extrude upwards
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# Add a slight fillet to the bottom of the shaft for realism
shaft = shaft.faces("<Z").edges().fillet(shaft_tip_fillet)

# 2. Create the integrated washer (flange)
# It sits on top of the shaft
washer = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(washer_diameter / 2.0)
    .extrude(washer_thickness)
)

# 3. Create the screw head
# It sits on top of the washer
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length + washer_thickness)
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# Apply fillet to the top edge of the head for the "pan" shape
head = head.faces(">Z").edges().fillet(head_fillet)

# 4. Create the slot cut
# We create a rectangular profile and cut it through the top of the head
slot_cutter = (
    cq.Workplane("XZ")
    .workplane(offset=-slot_width / 2.0) # Center the slot width-wise
    .center(0, shaft_length + washer_thickness + head_height) # Move to top of head
    .rect(head_diameter + 2.0, slot_depth * 2, centered=True) # Oversize rect to ensure cut
    .extrude(slot_width)
)

# Combine the solid parts
solid_body = shaft.union(washer).union(head)

# Perform the cut
result = solid_body.cut(slot_cutter)

# Export or display (optional, but good for checking if running locally)
# show_object(result)