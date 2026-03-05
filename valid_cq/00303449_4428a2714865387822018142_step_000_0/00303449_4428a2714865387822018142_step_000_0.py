import cadquery as cq

# Parametric dimensions
base_diameter = 24.0
base_thickness = 1.2
boss_diameter = 10.0
boss_height = 5.0
pin_diameter = 5.0
pin_height = 4.0
part_spacing = 35.0

# --- Create Part 1 (Male/Stud) ---
# Create the base disc
male_part = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_thickness)

# Extrude the intermediate boss
male_part = (
    male_part.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
)

# Extrude the top pin
male_part = (
    male_part.faces(">Z")
    .workplane()
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)

# --- Create Part 2 (Female/Socket) ---
# Create the base disc
female_part = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_thickness)

# Extrude the boss
female_part = (
    female_part.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
)

# Cut the center hole (through all)
female_part = (
    female_part.faces(">Z")
    .workplane()
    .circle(pin_diameter / 2.0)
    .cutBlind(-(boss_height + base_thickness + 1.0))
)

# Translate the female part to sit next to the male part
female_part = female_part.translate((part_spacing, 0, 0))

# Combine both parts into the final result
result = male_part.union(female_part)