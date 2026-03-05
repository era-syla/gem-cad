import cadquery as cq

# Parametric dimensions
main_diameter = 20.0
main_height = 40.0
boss_diameter = 8.0
boss_height = 3.0
hole_diameter = 2.0
hole_depth = 5.0  # Depth of the hole from the top surface

# Create the main cylinder body
# Based on the image, there is a seam line, so we can model it as two stacked cylinders 
# or just one main body. For simplicity and robustness, we model the main body.
main_body = cq.Workplane("XY").circle(main_diameter / 2).extrude(main_height)

# Create the top boss
# Select the top face of the main body
boss = (
    main_body.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Create the center hole
# Select the top face of the boss (the highest Z face)
result = (
    boss.faces(">Z")
    .workplane()
    .hole(hole_diameter, hole_depth)
)

# Optional: If the seam line in the middle is geometrically significant (e.g., separate parts), 
# one would model two cylinders. But assuming it's a single solid part as per standard request:
# The result variable now holds the final geometry.