import cadquery as cq

# Parametric definitions
tube_diameter = 5.0
tube_radius = tube_diameter / 2.0

# Define the control points for the spline path to match the organic shape
# Coordinates are estimated to reproduce the hook/loop geometry visualized in the image
spline_points = [
    (35, 18),    # Start at the inner 'floating' end (left-center)
    (20, 23),    # Curve towards the left hook
    (2, 30),     # The tightest part of the left bend (nose)
    (12, 42),    # Rising to the top section
    (50, 46),    # Middle of the top arch
    (85, 36),    # Beginning of the large downward curve on the right
    (98, 16),    # Furthest right point
    (90, 0)      # End point at the bottom right
]

# Create the path wire on the XY plane using a spline for smooth continuity
path = cq.Workplane("XY").spline(spline_points)

# To sweep correctly, we need a profile perpendicular to the start of the path.
# We extract the tangent vector at the start of the wire to define the profile plane.
path_wire = path.val()
start_loc = path_wire.positionAt(0)
start_dir = path_wire.tangentAt(0)

# Create a workplane defined by the start position and tangent direction
# The normal of the plane is aligned with the start tangent of the path
profile_plane = cq.Plane(origin=start_loc, normal=start_dir)

# Create the circular profile on the constructed plane and sweep it along the path
result = (
    cq.Workplane(profile_plane)
    .circle(tube_radius)
    .sweep(path)
)