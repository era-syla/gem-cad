import cadquery as cq

# Parametric dimensions
outer_diameter = 100.0    # Diameter of the outer disk
inner_diameter = 50.0     # Diameter of the central hole
thickness = 5.0           # Thickness of the flange
bolt_circle_diameter = 75.0 # Diameter of the circle on which mounting holes are placed
hole_diameter = 8.0       # Diameter of the mounting holes
num_holes = 4             # Number of mounting holes

# Create the flange geometry
result = (
    cq.Workplane("XY")
    # Draw the main ring (outer and inner circles)
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
    # Select the top face to place mounting holes
    .faces(">Z")
    .workplane()
    # Create the pattern of holes
    .polarArray(radius=bolt_circle_diameter / 2.0, startAngle=0, angle=360, count=num_holes)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)