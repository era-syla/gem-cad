import cadquery as cq

# --- Parametric Dimensions ---
base_radius = 12.0        # Radius of the solid cylinder base
base_height = 30.0        # Height of the solid cylinder base
spring_height = 25.0      # Total height of the helical spring section
spring_turns = 4.5        # Number of turns in the spring
wire_radius = 2.0         # Cross-sectional radius of the spring wire

# Calculated Dimensions
# Helix radius adjusted so spring outer diameter aligns with base cylinder
helix_radius = base_radius - wire_radius
pitch = spring_height / spring_turns

# --- Geometry Construction ---

# 1. Create the cylindrical base
# Extrude a circle from the XY plane
base = cq.Workplane("XY").circle(base_radius).extrude(base_height)

# 2. Generate the helical path
# cq.Wire.makeHelix creates a wire for the path of the spring.
# It starts at (radius, 0, 0) relative to its origin.
helix_path = cq.Wire.makeHelix(
    pitch=pitch, 
    height=spring_height, 
    radius=helix_radius
)

# Translate the path to sit on top of the base cylinder
helix_path = helix_path.translate((0, 0, base_height))

# 3. Create the spring geometry (Sweep)
# Define the circular profile of the wire at the start of the helix.
# The helix starts at (helix_radius, 0, base_height).
# We establish a Workplane on the XZ plane centered at that start point
# to create a profile perpendicular to the path's initial tangent (approx Y-axis).
spring = (
    cq.Workplane("XZ", origin=(helix_radius, 0, base_height))
    .circle(wire_radius)
    .sweep(helix_path, isFrenet=True)
)

# 4. Combine base and spring into final object
result = base.union(spring)