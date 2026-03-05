import cadquery as cq

# Parameters for the U-channel bracket
length = 400.0         # Total length
width = 50.0           # Width of the top face
height = 10.0          # Height of the side flanges
thickness = 2.5        # Material thickness
bend_radius = 4.0      # Exterior corner radius
hole_diameter = 4.0    # Mounting hole diameter

# Derived parameters
w_half = width / 2.0
inner_radius = max(0.0, bend_radius - thickness)

# 1. Create the C-channel/U-profile
# We draw the profile on the YZ plane (facing the X-axis) and extrude along X.
# The top surface is aligned with Z=0, legs point down to Z=-height.
profile_sketch = (
    cq.Workplane("YZ")
    .workplane(offset=-length / 2.0)  # Start extrusion at -L/2
    
    # Outer profile
    .moveTo(w_half, -height)
    .lineTo(w_half, -bend_radius)
    .radiusArc((w_half - bend_radius, 0), bend_radius)
    .lineTo(-(w_half - bend_radius), 0)
    .radiusArc((-w_half, -bend_radius), bend_radius)
    .lineTo(-w_half, -height)
    
    # Bottom thickness close
    .lineTo(-w_half + thickness, -height)
    
    # Inner profile (reversed direction)
    .lineTo(-w_half + thickness, -bend_radius)
)

# Handle inner corner arcs
if inner_radius > 0:
    profile_sketch = profile_sketch.radiusArc(
        (-(w_half - bend_radius), -thickness), -inner_radius
    )
else:
    profile_sketch = profile_sketch.lineTo(-(w_half - bend_radius), -thickness)

profile_sketch = profile_sketch.lineTo(w_half - bend_radius, -thickness)

if inner_radius > 0:
    profile_sketch = profile_sketch.radiusArc(
        (w_half - thickness, -bend_radius), -inner_radius
    )
else:
    profile_sketch = profile_sketch.lineTo(w_half - thickness, -bend_radius)

# Close shape
profile_sketch = profile_sketch.lineTo(w_half - thickness, -height).close()

# Extrude to create the main solid
body = profile_sketch.extrude(length)

# 2. Define Hole Locations
# Pattern: Two pairs at each end, two single holes in the middle section
holes = []

# Spacing parameters
end_distance_1 = 20.0
end_distance_2 = 50.0
mid_distance = 60.0
pair_width_spacing = 24.0 # Distance between holes in a pair (transverse)
y_offset = pair_width_spacing / 2.0

# Generate coordinates
# End groups (Pairs)
for x_base in [length/2 - end_distance_1, length/2 - end_distance_2]:
    # Right side pairs
    holes.append((x_base, y_offset))
    holes.append((x_base, -y_offset))
    # Left side pairs (symmetric)
    holes.append((-x_base, y_offset))
    holes.append((-x_base, -y_offset))

# Middle holes (Single centered)
holes.append((mid_distance, 0))
holes.append((-mid_distance, 0))

# 3. Create Holes
result = (
    body
    .faces(">Z") # Select the top face (Z=0)
    .workplane()
    .pushPoints(holes)
    .hole(hole_diameter)
)