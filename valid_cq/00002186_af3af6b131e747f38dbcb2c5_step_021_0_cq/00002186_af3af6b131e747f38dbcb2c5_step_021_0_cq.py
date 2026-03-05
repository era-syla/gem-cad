import cadquery as cq

# --- Parametric Dimensions ---
main_diameter = 100.0
main_height = 60.0

boss_diameter = 25.0
boss_height = 5.0

hole_diameter = 8.0
hole_depth = 20.0
hole_pattern_radius = 22.0  # Distance from center to the bolt circle
num_holes = 4

# --- Modeling Process ---

# 1. Create the main cylindrical body
base_cylinder = cq.Workplane("XY").circle(main_diameter / 2).extrude(main_height)

# 2. Create the central boss on top
# We select the top face of the base cylinder to sketch on
boss = (
    base_cylinder.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# 3. Create the pattern of four holes
# We select the top face of the main body (not the boss) again to drill into.
# Alternatively, we can use the top face of the resulting object (boss face),
# move down to the main surface level, and drill.
# A robust way is to select the base cylinder's top face reference.

result = (
    boss.faces("<Z") # Select the bottom face (XY plane) to reset reference
    .workplane(offset=main_height) # Move workplane to the top of the main cylinder
    .polarArray(hole_pattern_radius, 0, 360, num_holes) # Create polar arrangement
    .circle(hole_diameter / 2) # Draw the circles for the holes
    .cutBlind(-hole_depth) # Cut downwards
)

# Return the result
if __name__ == "__main__":
    try:
        from cadquery import show_object
        show_object(result)
    except ImportError:
        print("cq-editor not detected, result variable is ready.")