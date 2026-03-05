import cadquery as cq
import math

# --- Parameters ---
helix_radius = 5.0      # Radius of the helix (centerline)
wire_radius = 0.6       # Radius of the wire cross-section
pitch = 3.0             # Vertical rise per turn
turns = 10              # Total number of turns
height = pitch * turns  # Total height of the spring

# --- Path Generation ---
# Generate a list of 3D points to define the helical path
# We use a spline for a smooth approximation of the helix
points_per_turn = 32
num_points = int(turns * points_per_turn)
path_points = []

for i in range(num_points + 1):
    # Normalized parameter t ranges from 0 to 1
    t = i / num_points
    
    # Calculate angle (theta) and height (z)
    angle = t * turns * 2 * math.pi
    z = height * t
    
    # Parametric equations for a helix
    x = helix_radius * math.cos(angle)
    y = helix_radius * math.sin(angle)
    
    path_points.append((x, y, z))

# Create the helical path wire
path = cq.Workplane("XY").spline(path_points)

# --- Profile and Sweep ---
# We need to create a sketch plane perpendicular to the start of the helix.
# Start point is (helix_radius, 0, 0).
# The tangent vector at the start (angle=0) lies in the Y-Z plane.
# vector direction: (0, R, pitch/2pi)
start_point = path_points[0]
tangent_vector = (0, helix_radius, pitch / (2 * math.pi))

# Define a construction plane with the normal aligned to the tangent
profile_plane = cq.Plane(origin=start_point, normal=tangent_vector)

# Create the solid by sweeping a circle along the path
result = (
    cq.Workplane(profile_plane)
    .circle(wire_radius)
    .sweep(path, isFrenet=True)
)