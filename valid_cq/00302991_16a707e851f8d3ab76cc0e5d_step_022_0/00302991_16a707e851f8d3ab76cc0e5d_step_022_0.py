import cadquery as cq

# Geometric parameters
length = 300.0        # Length of the tubes
outer_diameter = 12.0 # Outer diameter of the tubes
wall_thickness = 1.5  # Thickness of the tube wall
spacing = 30.0        # Center-to-center distance between the tubes

# Derived parameters
inner_diameter = outer_diameter - (2 * wall_thickness)
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# Create the CAD model
# 1. Start a workplane on the YZ plane (drawing the cross-section)
# 2. Push two points for the centers of the parallel tubes
# 3. Draw outer and inner circles at both points to define the tube walls
# 4. Extrude along the X-axis to create the 3D geometry
result = (
    cq.Workplane("YZ")
    .pushPoints([(0, spacing / 2.0), (0, -spacing / 2.0)])
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)