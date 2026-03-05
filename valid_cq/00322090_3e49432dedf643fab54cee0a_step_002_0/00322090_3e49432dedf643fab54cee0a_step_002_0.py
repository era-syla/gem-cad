import cadquery as cq

# --- Parametric Dimensions ---
# Cylinder dimensions
cyl_od = 25.0       # Outer diameter
cyl_id = 15.0       # Inner diameter (hole)
cyl_height = 20.0   # Total height

# Base plate dimensions
plate_width = 25.0  # Width of the rectangular tab (matching cylinder OD)
plate_length = 35.0 # Total length from center of cylinder
plate_thick = 3.0   # Thickness of the plate

# Rib (Gusset) dimensions
rib_thickness = 4.0
rib_height = 12.0   # Vertical height along the cylinder
rib_span = 15.0     # Horizontal length along the plate

# --- Modeling ---

# 1. Create the main cylinder
# Centered at (0,0) on the XY plane
cylinder = cq.Workplane("XY").circle(cyl_od / 2.0).extrude(cyl_height)

# 2. Create the rectangular base plate
# Positioned to start from the center (x=0) and extend along +X axis
# Using center(x, y) to shift the drawing plane origin
plate = (
    cq.Workplane("XY")
    .center(plate_length / 2.0, 0)
    .rect(plate_length, plate_width)
    .extrude(plate_thick)
)

# 3. Create the support rib
# Drawn on the XZ plane (side view)
# To ensure the rib merges cleanly with the curved cylinder surface,
# we extend the vertical edge slightly inside the cylinder (overlap).
overlap = 2.0 
pts = [
    (cyl_od / 2.0 - overlap, plate_thick),                 # Bottom-inner point
    (cyl_od / 2.0 - overlap, plate_thick + rib_height),    # Top-inner point
    (cyl_od / 2.0 + rib_span, plate_thick)                 # Outer tip point
]

rib = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(rib_thickness / 2.0, both=True) # Symmetric extrusion
)

# 4. Combine parts and cut the hole
# We union the solids first, then cut the hole to ensure 
# any internal material from the plate or rib is removed.
result = (
    cylinder
    .union(plate)
    .union(rib)
    .faces(">Z")    # Select the top face
    .workplane()
    .hole(cyl_id)   # Cut through-hole
)