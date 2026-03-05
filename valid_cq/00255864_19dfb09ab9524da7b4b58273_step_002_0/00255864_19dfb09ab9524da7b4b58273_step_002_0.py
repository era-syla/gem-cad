import cadquery as cq

# ==========================================
# Parametric Definitions
# ==========================================
rod_length = 80.0       # Final length of the rod
rod_diameter = 6.0      # Major diameter of the thread
pitch = 1.5             # Thread pitch
thread_angle = 60.0     # Thread angle in degrees

# Derived parameters
radius = rod_diameter / 2.0
# Approximate thread depth for visualization (0.6 * pitch is standard-ish for metric)
thread_depth = 0.6 * pitch
minor_radius = radius - thread_depth

# Generate extra length to ensure clean cuts at both ends
buffer = pitch * 2.0
gen_length = rod_length + buffer

# ==========================================
# 1. Base Geometry Generation
# ==========================================

# Create the inner core cylinder (minor diameter)
# Extruded longer than final length to be trimmed later
core = cq.Workplane("XY").circle(minor_radius).extrude(gen_length)

# Create the Helix Path
# We generate a helix wire starting at (minor_radius, 0, 0)
helix_path = cq.Wire.makeHelix(pitch=pitch, height=gen_length, radius=minor_radius)

# ==========================================
# 2. Thread Profile & Sweep
# ==========================================

# We need to define the thread cross-section perpendicular to the start of the helix.
# Start point of helix
p0 = helix_path.positionAt(0)
# Tangent vector at start
t0 = helix_path.tangentAt(0)

# Create a local plane for the profile sketch.
# Origin at helix start, Normal along helix tangent.
# xDir aligned with global X (radial direction) to orient the triangle correctly.
profile_plane = cq.Plane(origin=p0, normal=t0, xDir=cq.Vector(1, 0, 0))

# Define the triangular thread profile
# Coordinates are local to profile_plane:
# X axis is Radial Outward.
# Y axis is perpendicular to Radial and Tangent.
# We add a small overlap into the core to ensure a valid boolean union.
overlap = 0.05
tri_width = pitch * 0.95  # Slightly less than pitch to prevent self-intersection

# Points for the triangle (Counter-Clockwise)
pts = [
    (-overlap, -tri_width / 2.0),  # Base Bottom-Left (inside core)
    (thread_depth, 0.0),           # Tip (Major Diameter)
    (-overlap, tri_width / 2.0)    # Base Top-Left (inside core)
]

# Create the profile and sweep it along the helix
thread_coil = (
    cq.Workplane(profile_plane)
    .polyline(pts)
    .close()
    .sweep(helix_path, isFrenet=True, transition='round')
)

# ==========================================
# 3. Final Assembly
# ==========================================

# Fuse the thread coil onto the core
raw_rod = core.union(thread_coil)

# Cut the rod to the final specific length.
# We define a bounding cylinder of the exact target length.
# We shift the raw_rod down by 'pitch' to cut off the tapered start of the helix.
cutter_volume = (
    cq.Workplane("XY")
    .circle(rod_diameter * 2.0)  # Large radius to enclose the whole rod
    .extrude(rod_length)         # Exact final length
)

# Translate raw rod to align valid section with cutter, then intersect
result = raw_rod.translate((0, 0, -pitch)).intersect(cutter_volume)