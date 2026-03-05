import cadquery as cq
import math

# Parameters
length = 200.0
width = 8.0
thickness = 3.0
curve_height = 15.0  # how much the strip curves upward
num_holes = 14
hole_diameter = 3.0
hole_spacing = length / (num_holes + 1)

# Create a curved plate using a swept profile along a curved path
# The plate curves slightly along its length

# Define the curved path using a spline/arc in the XZ plane
# The strip is long, thin, with a slight curve and holes along it

# Create path points for the curve
num_path_pts = 20
path_pts = []
for i in range(num_path_pts + 1):
    t = i / num_path_pts
    x = t * length - length / 2
    # Slight parabolic curve in z
    z = curve_height * 4 * t * (1 - t)
    path_pts.append((x, 0, z))

# Build the path as a spline wire
path_wire = (
    cq.Workplane("XZ")
    .moveTo(path_pts[0][0], path_pts[0][2])
    .spline([(pt[0], pt[2]) for pt in path_pts[1:]])
    .val()
)

# Create a rectangular cross-section profile perpendicular to the start of the path
# Profile in YZ plane at start of path
profile = (
    cq.Workplane("YZ")
    .rect(width, thickness)
)

# Sweep the profile along the curved path
result = profile.sweep(path_wire)

# Now add holes along the strip
# We need to cut holes along the length of the strip
# Approximate hole positions along the curve

# Cut holes by working on the result
# Place holes at evenly spaced positions along the path
for i in range(num_holes):
    t = (i + 1) / (num_holes + 1)
    x = t * length - length / 2
    z = curve_height * 4 * t * (1 - t)
    
    # Normal to curve at this point
    dt = 0.001
    t1 = max(0, t - dt)
    t2 = min(1, t + dt)
    x1 = t1 * length - length / 2
    z1 = curve_height * 4 * t1 * (1 - t1)
    x2 = t2 * length - length / 2
    z2 = curve_height * 4 * t2 * (1 - t2)
    
    dx = x2 - x1
    dz = z2 - z1
    length_tangent = math.sqrt(dx**2 + dz**2)
    tx = dx / length_tangent
    tz = dz / length_tangent
    
    # Normal in XZ plane (perpendicular to tangent)
    nx = -tz
    nz = tx
    
    # Create a cutting cylinder at this position
    # The cylinder axis should be along Y (through the width)
    cyl = (
        cq.Workplane("XY")
        .transformed(offset=(x, 0, z))
        .circle(hole_diameter / 2)
        .extrude(width * 2, both=True)
    )
    
    result = result.cut(cyl)

# Round the ends slightly
try:
    result = result.edges("|Y").fillet(0.5)
except:
    pass