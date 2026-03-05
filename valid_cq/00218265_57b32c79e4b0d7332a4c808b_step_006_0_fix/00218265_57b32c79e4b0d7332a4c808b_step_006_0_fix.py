import cadquery as cq

# Define the sweep path in the XZ plane (X is horizontal, Z is vertical)
path_points = [(0, 0), (25, 15), (50, -10), (75, 20), (100, 0)]
path = cq.Workplane("XZ").spline(path_points).wire()

# Sweep a circular profile along the path to create the S-shaped tube
tube = cq.Workplane("XY").circle(2).sweep(path, isFrenet=True)

# Create a separate small cylinder above and to the right of the tube
cylinder = (
    cq.Workplane("XY")
    .workplane(offset=30)     # raise the base of the cylinder 30 units in Z
    .center(120, 0)           # position it at X=120, Y=0
    .circle(5)                # radius 5
    .extrude(10)              # height 10
)

# Combine both solids into the final result
result = tube.union(cylinder)