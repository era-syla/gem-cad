import cadquery as cq

# Parameters for dimensions based on visual estimation
rod_height = 120.0
rod_width = 4.0
rod_depth = 4.0
loop_major_r = 30.0   # Major radius of the ellipse
loop_minor_r = 18.0   # Minor radius of the ellipse
wire_radius = 1.5     # Radius of the wire forming the loop
clamp_size = 5.0      # Width of the connection block
clamp_height = 6.0    # Height of the connection block

# 1. Create the vertical rod
# Centered at the origin
rod = cq.Workplane("XY").box(rod_width, rod_depth, rod_height)

# 2. Create the connector clamp
# A slightly larger box at the center where the loop connects
clamp = cq.Workplane("XY").box(clamp_size, clamp_size, clamp_height)

# 3. Create the elliptical loop
# First, define the path wire. We center the ellipse at the origin initially.
path = cq.Workplane("XY").ellipse(loop_major_r, loop_minor_r).val()

# Define the profile for the sweep. 
# The ellipse starts at (major_r, 0, 0). The tangent there is along the Y axis.
# We define the profile circle on the XZ plane (Normal Y), centered at the start point.
ring = (
    cq.Workplane("XZ", origin=(loop_major_r, 0, 0))
    .circle(wire_radius)
    .sweep(path)
)

# Translate the ring so it extends outwards from the rod
# Moving by loop_major_r aligns the "left" edge of the ring with the origin (where the rod is)
ring = ring.translate((loop_major_r, 0, 0))

# 4. Combine all geometry into a single solid
result = rod.union(clamp).union(ring)