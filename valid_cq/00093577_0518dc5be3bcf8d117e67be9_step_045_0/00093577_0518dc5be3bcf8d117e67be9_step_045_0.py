import cadquery as cq

# Parametric dimensions
outer_diameter = 100.0    # Diameter of the outer edge
inner_diameter = 50.0     # Diameter of the large central hole
thickness = 3.0           # Thickness of the plate
bolt_circle_diam = 75.0   # Diameter of the circle on which small holes are placed
hole_diameter = 12.0      # Diameter of the small peripheral holes
num_holes = 8             # Number of small holes

# Generate the CAD model
result = (
    cq.Workplane("XY")
    # Draw the outer boundary
    .circle(outer_diameter / 2.0)
    # Draw the inner hole boundary
    .circle(inner_diameter / 2.0)
    # Create a polar array for the surrounding holes
    .polarArray(bolt_circle_diam / 2.0, 0, 360, num_holes)
    # Draw the small holes at the array locations
    .circle(hole_diameter / 2.0)
    # Extrude the sketch (CadQuery automatically subtracts inner profiles)
    .extrude(thickness)
)