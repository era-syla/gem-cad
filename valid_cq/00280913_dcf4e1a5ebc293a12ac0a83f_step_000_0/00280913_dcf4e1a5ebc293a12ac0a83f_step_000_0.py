import cadquery as cq

# Define dimensions for the pipe
outer_diameter = 20.0
inner_diameter = 14.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# Define points for the spline path in the XZ plane
# The shape consists of an upward curve, a downward trough, and another upward curve
path_points = [
    (0, 0),         # Start point
    (30, 30),       # First peak
    (60, -10),      # Middle trough
    (90, 30),       # Second peak
    (115, 0)        # End point
]

# Create the path wire
# We enforce a start tangent of (1, 0) (horizontal along X) 
# to ensure the profile defined on the YZ plane is perpendicular to the start of the path.
path = (
    cq.Workplane("XZ")
    .moveTo(path_points[0][0], path_points[0][1])
    .spline(
        path_points[1:],
        tangents=[(1, 0), (0.5, -1)], # Start horizontal, end pointing downwards
        includeCurrent=False
    )
)

# Create the profile on the YZ plane
# Since the path starts at (0,0,0) with a tangent along X, the YZ plane is the correct normal plane.
# We draw two concentric circles to form the hollow tube profile.
result = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .circle(inner_radius)
    .sweep(path)
)