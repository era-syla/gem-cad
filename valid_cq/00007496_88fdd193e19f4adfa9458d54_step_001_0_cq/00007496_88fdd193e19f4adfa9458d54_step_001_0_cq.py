import cadquery as cq

# Parametric dimensions
base_diameter = 50.0   # Diameter of the larger cylinder
base_height = 40.0     # Height/length of the larger cylinder
boss_diameter = 25.0   # Diameter of the smaller cylinder (the protrusion)
boss_height = 20.0     # Height/length of the smaller cylinder

# Create the base cylinder
# We start by drawing a circle on the XY plane and extruding it
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

# Create the smaller cylinder (boss) on top of the base
# We select the top face of the base cylinder (the face with highest Z value)
# Then draw the smaller circle and extrude it
result = (
    base.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Alternatively, using union of two separate cylinders
# cylinder_1 = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)
# cylinder_2 = cq.Workplane("XY").workplane(offset=base_height).circle(boss_diameter / 2).extrude(boss_height)
# result = cylinder_1.union(cylinder_2)