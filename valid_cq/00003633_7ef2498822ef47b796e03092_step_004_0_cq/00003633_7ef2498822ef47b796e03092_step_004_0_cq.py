import cadquery as cq

# Parametric dimensions
base_diameter = 50.0   # Diameter of the larger flange/base
base_thickness = 10.0  # Thickness of the larger flange/base
boss_diameter = 25.0   # Diameter of the protruding boss
boss_height = 20.0     # Height of the protruding boss (from the face of the base)
hole_diameter = 12.0   # Diameter of the central through-hole

# Create the model
result = (
    cq.Workplane("XY")
    # 1. Create the base cylinder
    .circle(base_diameter / 2)
    .extrude(base_thickness)
    # 2. Select the top face of the base to draw the boss
    .faces(">Z")
    .workplane()
    # 3. Create the boss cylinder
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    # 4. Create the through-hole
    # We select the top-most face to start the hole from, ensuring it goes through everything
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)