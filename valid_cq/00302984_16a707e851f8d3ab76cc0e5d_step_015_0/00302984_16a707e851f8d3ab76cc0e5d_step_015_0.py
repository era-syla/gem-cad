import cadquery as cq

# -- Parametric Dimensions --
plate_length = 120.0
plate_width = 40.0
plate_thickness = 4.0
corner_radius = 10.0

# Slot parameters
slot_length = 14.0  # Total length of the slot
slot_width = 7.0    # Diameter of the slot ends
# Calculate slot position relative to the plate center
# Positioning them inward from the ends based on corner radius approximation
slot_x_offset = (plate_length / 2.0) - corner_radius - 2.0

# Boss parameters (feature on the left back side)
boss_diameter = 13.0
boss_height = 6.0

# -- Modeling --

# 1. Create the base plate geometry
# Start with a simple box centered on the XY plane
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Apply fillets to the corners
# Select vertical edges (parallel to Z axis) and fillet them
result = result.edges("|Z").fillet(corner_radius)

# 3. Create the cylindrical boss on the back
# Select the bottom face (negative Z), create a new workplane
# Move to the position of the left slot and extrude the boss outwards
result = (result.faces("<Z").workplane()
          .moveTo(-slot_x_offset, 0)
          .circle(boss_diameter / 2.0)
          .extrude(boss_height))

# 4. Cut the slots
# Select the top face (positive Z)
# Use pushPoints to define centers for both the left and right slots
# Create 2D slot profiles and cut through the entire model (plate + boss)
result = (result.faces(">Z").workplane()
          .pushPoints([(-slot_x_offset, 0), (slot_x_offset, 0)])
          .slot2D(length=slot_length, diameter=slot_width, angle=0)
          .cutThruAll())