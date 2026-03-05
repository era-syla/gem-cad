import cadquery as cq

# Parameters for the geometry
width = 30.0          # Width of the vertical bracket face and arm
height = 50.0         # Height of the vertical section
thickness = 6.0       # General wall thickness
arm_length = 80.0     # Length of the horizontal arm from the back
arm_end_radius = 15.0 # Radius of the rounded end of the arm
flange_depth_top = 15.0 # Depth of the side stiffener at the top
flange_depth_bot = 40.0 # Depth of the side stiffener at the bottom
boss_height = 4.0     # Height of the boss around the slot
hole_diameter = 8.0   # Diameter of the hole in the vertical section
slot_width = 10.0     # Width of the slot
slot_length = 25.0    # Total length of the slot

# 1. Vertical Main Wall
# Create the back vertical plate. Positioned with back face at Y=0.
vertical_wall = (
    cq.Workplane("XY")
    .box(width, thickness, height, centered=False)
    .edges(">X and >Z") # Fillet the top-right corner
    .fillet(15.0)
)

# Create the hole in the vertical wall
vertical_wall = (
    vertical_wall.faces(">Y").workplane()
    .pushPoints([(width / 2, height - 15.0)])
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# 2. Horizontal Arm
# Create the horizontal arm extending from the wall.
# Sketch on XY plane.
arm_sketch = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(width, 0)
    .lineTo(width, arm_length - arm_end_radius)
    .radiusArc((0, arm_length - arm_end_radius), arm_end_radius)
    .close()
)
horizontal_arm = arm_sketch.extrude(thickness)

# 3. Side Stiffener / Flange
# Create the side rib that connects the vertical and horizontal parts.
# Sketch on YZ plane (Side view).
stiffener_sketch = (
    cq.Workplane("YZ")
    .moveTo(0, 0) # Bottom-back corner
    .lineTo(flange_depth_bot, 0) # Bottom point on arm
    .lineTo(flange_depth_bot, thickness) # Step up to top of arm
    .lineTo(flange_depth_top, height) # Slope up to top flange depth
    .lineTo(0, height) # Back to top corner
    .close()
)
# Extrude in X direction (thickness of the stiffener)
side_stiffener = stiffener_sketch.extrude(thickness)

# 4. Boss for the Slot
# Create the raised area around the slot.
slot_center_y = arm_length - arm_end_radius
boss_width = slot_width + 8.0
boss_len = slot_length + 8.0

boss_wire = (
    cq.Workplane("XY").workplane(offset=thickness)
    .moveTo(width / 2 - boss_width / 2, slot_center_y - boss_len / 2 + boss_width / 2)
    .lineTo(width / 2 - boss_width / 2, slot_center_y + boss_len / 2 - boss_width / 2)
    .radiusArc((width / 2 + boss_width / 2, slot_center_y + boss_len / 2 - boss_width / 2), boss_width / 2)
    .lineTo(width / 2 + boss_width / 2, slot_center_y - boss_len / 2 + boss_width / 2)
    .radiusArc((width / 2 - boss_width / 2, slot_center_y - boss_len / 2 + boss_width / 2), boss_width / 2)
    .close()
)
boss = boss_wire.extrude(boss_height)

# 5. Combine solids
result = vertical_wall.union(horizontal_arm).union(side_stiffener).union(boss)

# 6. Cut the Slot
# Define the slot profile
slot_wire = (
    cq.Workplane("XY")
    .moveTo(width / 2 - slot_width / 2, slot_center_y - slot_length / 2 + slot_width / 2)
    .lineTo(width / 2 - slot_width / 2, slot_center_y + slot_length / 2 - slot_width / 2)
    .radiusArc((width / 2 + slot_width / 2, slot_center_y + slot_length / 2 - slot_width / 2), slot_width / 2)
    .lineTo(width / 2 + slot_width / 2, slot_center_y - slot_length / 2 + slot_width / 2)
    .radiusArc((width / 2 - slot_width / 2, slot_center_y - slot_length / 2 + slot_width / 2), slot_width / 2)
    .close()
)
# Cut through the entire assembly
result = result.cut(slot_wire.extrude(height))

# 7. Add Fillets
# Fillet the internal corner between the vertical wall/stiffener and the arm
# We select edges near the intersection line (Y approx thickness, Z approx thickness)
try:
    result = result.edges(
        f"(|X or |Y) and (not >Z) and (not <Z) and (not >Y)"
    ).filter(lambda e: e.center().z < thickness + 1.0 and e.center().y < thickness + 1.0).fillet(3.0)
except:
    pass # Skip if specific edge selection is unstable

# Fillet the transition of the stiffener slope to the arm
try:
    result = result.edges(
        "|X"
    ).filter(lambda e: abs(e.center().y - flange_depth_bot) < 1.0 and abs(e.center().z - thickness) < 1.0).fillet(5.0)
except:
    pass

# Fillet the base of the boss
try:
    result = result.edges(f"(not >Z) and (not <Z)").filter(lambda e: e.center().z > thickness + 0.1).fillet(2.0)
except:
    pass