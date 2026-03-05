import cadquery as cq

# --- Parametric Dimensions ---
length = 100.0         # Total length of the part
width = 12.0           # Width of the base
base_height = 5.0      # Height of the rectangular base section
radius = width / 2.0   # Radius of the top cylinder (matching base width)
cut_length = 30.0      # Length of the angled cut section
total_height = base_height + radius

# --- Geometry Construction ---

# 1. Create the rectangular base
# Oriented along the X-axis, centered on Y, sitting on Z=0
base = cq.Workplane("XY").box(length, width, base_height, centered=(False, True, False))

# 2. Create the cylindrical top section
# Defined on the YZ plane (side profile) and extruded along X
cylinder = (
    cq.Workplane("YZ")
    .center(0, base_height)  # Position center on top of the base
    .circle(radius)
    .extrude(length)
)

# 3. Create the raw stock by uniting base and cylinder
raw_part = base.union(cylinder)

# 4. Create the angled cut geometry
# We sketch a triangle on the XZ plane (side view) representing the material to remove.
# The triangle is formed by the tip (0,0), the top of the slope, and the top-front corner.
cutter = (
    cq.Workplane("XZ")
    .moveTo(0, 0)                       # Start at the origin (tip of the part)
    .lineTo(cut_length, total_height)   # Line to the top end of the slope
    .lineTo(0, total_height)            # Line to the top-front corner
    .close()                            # Close back to origin
    .extrude(width * 2, both=True)      # Extrude wider than the part to ensure a clean cut
)

# 5. Apply the cut to the raw part
result = raw_part.cut(cutter)