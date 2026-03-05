import cadquery as cq
from math import cos, sin, pi

def helix_path(radius, height, pitch, resolution=50):
    """
    Generates points for a helical path.
    radius: The radius of the helix
    height: The total height of the helix
    pitch: The vertical distance per turn
    resolution: Number of points per turn
    """
    points = []
    num_turns = height / pitch
    total_steps = int(num_turns * resolution)
    
    for i in range(total_steps + 1):
        t = i / resolution  # Current turn fraction
        angle = t * 2 * pi
        z = t * pitch
        x = radius * cos(angle)
        y = radius * sin(angle)
        points.append((x, y, z))
        
    return points

# --- Parameters ---
cyl_radius = 20.0
cyl_height = 30.0
pipe_radius = 2.0
pipe_pitch = 8.0  # Vertical distance between coil turns
# Adjust helix radius so the pipe sits on the surface of the cylinder
# The center of the pipe needs to be at cyl_radius + pipe_radius (if external)
# or cyl_radius (if centered on surface). The image shows it partially embedded or flush.
# Let's assume the pipe's centerline is tangent to the cylinder surface for a clean look,
# or slightly embedded. Based on the image, the coil looks fully external but wrapping tight.
# Let's place the coil centerline at cyl_radius + pipe_radius so it touches the cylinder.
# Looking closer at the top, the coil seems to end flush with the top surface.
helix_radius = cyl_radius + pipe_radius * 0.8 # Slightly embedded for better union

# --- Create the Central Cylinder ---
cylinder = cq.Workplane("XY").cylinder(cyl_height, cyl_radius)

# --- Create the Helical Coil ---
# 1. Generate the 3D path points
path_points = helix_path(helix_radius, cyl_height, pipe_pitch)

# 2. Create the path wire
# We start slightly below z=0 and end slightly above z=cyl_height if we wanted to cut,
# but here we are adding material.
path = cq.Workplane("XY").spline(path_points).val()

# 3. Create the profile to sweep (a circle)
# We need to position the profile plane normal to the start of the path.
# However, CadQuery's sweep can automatically handle orientation if we just provide the profile.
# A simple way is to create a sketch on a plane perpendicular to the start of the path.
# Or, simpler: just create a standalone solid wire and sweep a circle along it.
# The `sweep` method in CQ usually requires a profile at the start of the path.

# Let's use the solid construction method which is robust:
coil = (
    cq.Workplane("XY")
    .workplane(offset=path_points[0][2]) # Move to Z start
    .moveTo(path_points[0][0], path_points[0][1]) # Move to XY start
    .circle(pipe_radius) # Create the profile
    .sweep(path, isFrenet=True) # Sweep along the spline path
)

# --- Combine Geometries ---
# Center the cylinder vertically to match typical origin placement or shift coil
# The coil generation started at Z=0. The cylinder default center is Z=0.
# We need to shift the cylinder to start at Z=0 (move up by height/2)
cylinder = cylinder.translate((0, 0, cyl_height / 2))

# Union the cylinder and the coil
result = cylinder.union(coil)