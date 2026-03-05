import cadquery as cq

# Parametric dimensions based on visual estimation
outer_diameter = 100.0        # Outer diameter of the disk
inner_diameter = 40.0         # Diameter of the large central hole
thickness = 3.0               # Thickness of the plate
bolt_circle_diameter = 70.0   # Diameter of the circle on which small holes are placed
hole_diameter = 5.0           # Diameter of the small mounting holes
num_holes = 6                 # Number of mounting holes

# Create the model
# 1. Start a workplane on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle (creates the main ring shape)
# 4. Use polarArray to define the center points for the hole pattern
# 5. Draw the circles for the hole pattern
# 6. Extrude everything together (CadQuery automatically subtracts inner wires from outer wires)
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .polarArray(bolt_circle_diameter / 2.0, 0, 360, num_holes)
    .circle(hole_diameter / 2.0)
    .extrude(thickness)
)