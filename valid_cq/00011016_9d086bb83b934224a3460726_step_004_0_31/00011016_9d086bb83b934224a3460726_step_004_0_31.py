import cadquery as cq
import math

# Parametric dimensions for the bolt
D = 10.0            # Nominal shaft diameter
pitch = 1.5         # Thread pitch
L = 40.0            # Total shaft length
thread_L = 32.0     # Length of the threaded portion
head_af = 16.0      # Hex head across flats
head_h = 6.4        # Hex head height

# Derived radii
major_r = D / 2.0
minor_r = major_r - 0.65 * pitch
head_radius = head_af / math.cos(math.pi / 6) / 2.0

# 1. Create the base solid (Shaft and Hex Head)
bolt = (
    cq.Workplane("XY")
    .circle(major_r)
    .extrude(L)
    .faces("<Z")
    .workplane()
    .polygon(6, head_radius * 2.0)
    .extrude(head_h)
)

# 2. Apply chamfers to head and tip
# Chamfer the top of the hex head (which is pointing downwards in our -Z construction)
bolt = bolt.faces("<Z").edges().chamfer(0.8)

# Chamfer the tip of the shaft
bolt = bolt.faces(">Z").edges().chamfer(pitch)

# 3. Generate the threads using a swept helical cut
helix_start = L - thread_L
helix_height = thread_L + pitch * 2.0  # Extend past the tip to ensure clean cut

# Create the helical path
path = cq.Wire.makeHelix(
    pitch=pitch,
    height=helix_height,
    radius=major_r
)
path = path.translate((0, 0, helix_start))

# Create the V-groove cutter profile on the XZ plane
# Width is slightly less than pitch to create flat crests (realistic and computationally robust)
cutter_w = pitch * 0.95
cutter_profile = (
    cq.Workplane("XZ")
    .moveTo(major_r + 1.0, helix_start - cutter_w / 2.0)
    .lineTo(minor_r, helix_start)
    .lineTo(major_r + 1.0, helix_start + cutter_w / 2.0)
    .close()
)

# Sweep the profile along the helix
thread_cut = cutter_profile.sweep(path, isFrenet=True)

# Subtract the swept thread cutter from the base bolt
result = bolt.cut(thread_cut)