import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the visual reference
h_base = 7.0           # Height of the smooth lower section
h_grip = 9.0           # Height of the knurled upper section
d_base = 24.0          # Diameter of the smooth section
d_grip = 30.0          # Diameter of the knurled section
d_bore = 20.0          # Inner diameter (through hole)
d_groove = 4.0         # Diameter of the scalloped cutouts
n_grooves = 20         # Number of knurl grooves
chamfer_size = 0.75    # Size of the chamfers

# --- Modeling ---

# 1. Base Structure
# Create the smooth base cylinder
result = cq.Workplane("XY").circle(d_base / 2.0).extrude(h_base)

# Create the larger grip cylinder on top of the base
result = result.faces(">Z").workplane().circle(d_grip / 2.0).extrude(h_grip)

# 2. Internal Geometry
# Cut the central bore through the entire part
result = result.faces(">Z").workplane().circle(d_bore / 2.0).cutThruAll()

# 3. Edge Treatments (Chamfers)
# Apply chamfer to the top inner edge (bore entrance)
# We select the edge with the smallest radius on the top face (the bore)
result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(chamfer_size)

# Apply chamfer to the bottom outer edge (base)
result = result.faces("<Z").edges().chamfer(chamfer_size)

# 4. Knurling (Scallops)
# Create the cutting tools for the side grooves
# We position cylinders centered on the perimeter of the grip section
cutters = (
    cq.Workplane("XY")
    .workplane(offset=h_base)  # Start at the junction of base and grip
    .polarArray(radius=d_grip / 2.0, startAngle=0, angle=360, count=n_grooves)
    .circle(d_groove / 2.0)
    .extrude(h_grip)
)

# Subtract the cutters from the main body to create the scalloped pattern
result = result.cut(cutters)