import cadquery as cq

# Parametric dimensions
# Front plate
front_width = 120.0
front_height = 50.0
front_thickness = 10.0

# Back block
back_width = 40.0
back_depth = 25.0
back_height = 30.0

# Slots
slot_width = 10.0
slot_height = 25.0
slot_offset_x = 40.0

# Pins
pin_radius = 3.5
pin_height = 12.0
pin_spacing = 20.0

# 1. Create the front plate
front_plate = cq.Workplane("XY").box(front_width, front_thickness, front_height)

# 2. Create the back block
# Calculate positions to make the top flush and back block directly behind the front plate
z_offset_back = (front_height - back_height) / 2.0
y_offset_back = (front_thickness + back_depth) / 2.0

back_block = (cq.Workplane("XY")
              .center(0, y_offset_back)
              .workplane(offset=z_offset_back)
              .box(back_width, back_depth, back_height))

# Combine main bodies
base_body = front_plate.union(back_block)

# 3. Cut the rectangular slots
result = (base_body.faces("<Y").workplane()
          .pushPoints([(-slot_offset_x, 0), (slot_offset_x, 0)])
          .rect(slot_width, slot_height)
          .cutThruAll())

# 4. Add the cylindrical pins
# Create a workplane at the top surface level (Z = front_height / 2)
# and center the pins on the back block's depth
pins = (cq.Workplane("XY")
        .workplane(offset=front_height / 2.0)
        .pushPoints([(-pin_spacing / 2.0, y_offset_back), (pin_spacing / 2.0, y_offset_back)])
        .circle(pin_radius)
        .extrude(pin_height))

# Final geometry
result = result.union(pins)