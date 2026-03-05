import cadquery as cq
import math

# Geometric Parameters for the Coiled Spring Pin
length = 50.0         # Length of the pin
diameter = 20.0       # Nominal outer diameter
thickness = 1.5       # Thickness of the material strip
turns = 2.25          # Number of windings (approximate for standard pins)
gap = 0.1             # Small gap between layers for visual definition
chamfer_size = 1.0    # Size of the chamfer on the ends

# Spiral Calculation Parameters
# We define an Archimedean spiral: r = a + b * theta
# The outer radius should reach the target diameter/2 at the end of the winding.
r_max = diameter / 2.0

# Define growth per radian (b) based on strip thickness and gap
# Pitch is the radial growth per full turn (2*pi)
pitch = thickness + gap
b = pitch / (2 * math.pi)

# Total angle of the spiral
total_angle = turns * 2 * math.pi

# To ensure a clean intersection with the outer cylindrical envelope, 
# we make the raw spiral slightly larger than the final diameter.
overshoot = 0.5
r_outer_end_raw = r_max + overshoot

# Calculate the starting radius of the outer curve (working backwards)
r_outer_start = r_outer_end_raw - b * total_angle

# Generate points for the spiral cross-section
pts_outer = []
pts_inner = []
resolution = 200 # Number of points for smoothness

for i in range(resolution + 1):
    # Parameter t goes from 0 to 1
    t = i / resolution
    theta = t * total_angle
    
    # Calculate radius for the outer surface of the strip
    r_out = r_outer_start + b * theta
    
    # Calculate radius for the inner surface of the strip
    r_in = r_out - thickness
    
    # Convert polar to cartesian
    x_out = r_out * math.cos(theta)
    y_out = r_out * math.sin(theta)
    pts_outer.append((x_out, y_out))
    
    x_in = r_in * math.cos(theta)
    y_in = r_in * math.sin(theta)
    pts_inner.append((x_in, y_in))

# Construct the closed wire profile for the spiral strip
# Sequence: Outer points -> End Cap -> Inner points (reversed) -> Start Cap
profile_pts = pts_outer + pts_inner[::-1]

# 1. Create the raw spiral extrusion
raw_spiral = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(length)
)

# 2. Create a bounding envelope (a perfect cylinder with chamfered ends)
# This trims the uneven spiral outer edge and applies the chamfers cleanly
envelope = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
    .faces(">Z or <Z") # Select top and bottom faces
    .chamfer(chamfer_size)
)

# 3. Intersect the spiral with the envelope to get the final shape
# This results in a solid coiled pin with a perfect OD and chamfered ends
result = raw_spiral.intersect(envelope)