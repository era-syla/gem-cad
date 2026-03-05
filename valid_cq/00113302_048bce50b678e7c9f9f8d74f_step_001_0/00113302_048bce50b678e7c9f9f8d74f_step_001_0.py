import cadquery as cq

# Parametric dimensions for the model
length = 300.0         # Total length of the strip
top_width = 30.0       # Width of the top flat surface
bottom_width = 24.0    # Width of the bottom base (creates the tapered sides)
thickness = 4.0        # Thickness of the main trapezoidal body
rib_radius = 1.5       # Radius of the semi-circular feet/ribs
rib_spacing = 14.0     # Distance between the centers of the two ribs

# Create the main body
# We define a trapezoidal profile on the YZ plane and extrude it along the X axis
# The points define the cross-section starting from top-left, clockwise
trapezoid_points = [
    (-top_width / 2.0, thickness),
    (top_width / 2.0, thickness),
    (bottom_width / 2.0, 0.0),
    (-bottom_width / 2.0, 0.0)
]

main_body = (
    cq.Workplane("YZ")
    .polyline(trapezoid_points)
    .close()
    .extrude(length)
)

# Create the bottom ribs
# These are cylindrical extrusions running along the length
# Centered at Z=0 to merge with the bottom of the main body
ribs = (
    cq.Workplane("YZ")
    .pushPoints([
        (-rib_spacing / 2.0, 0.0),
        (rib_spacing / 2.0, 0.0)
    ])
    .circle(rib_radius)
    .extrude(length)
)

# Union the main body and the ribs to create the final solid geometry
result = main_body.union(ribs)