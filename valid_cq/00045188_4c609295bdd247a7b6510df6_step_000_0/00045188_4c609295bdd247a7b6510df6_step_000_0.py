import cadquery as cq

# Parameters for the geometry
shaft_length = 120.0
shaft_od = 10.0        # Outer diameter
shaft_id = 8.0         # Inner diameter (hollow tube)
fin_span = 12.0        # Radial height of fins
fin_root_chord = 35.0  # Length of fin at the base
fin_tip_chord = 20.0   # Length of fin at the tip
fin_thickness = 1.0    # Thickness of the fin plate
num_fins = 3           # Number of fins

# Derived dimensions
shaft_radius = shaft_od / 2.0
shaft_inner_radius = shaft_id / 2.0

# 1. Create the central hollow shaft
# Aligned along the Z-axis, starting at Z=0
shaft = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .circle(shaft_inner_radius)
    .extrude(shaft_length)
)

# 2. Define the geometry for a single fin
# We sketch the profile on the XZ plane.
# To ensure a robust boolean union with the curved shaft surface, 
# we embed the fin root slightly into the shaft wall (overlap).
overlap = 0.5  # Embed depth
p1 = (shaft_radius - overlap, 0)                  # Root, trailing edge (at Z=0)
p2 = (shaft_radius + fin_span, 0)                 # Tip, trailing edge
p3 = (shaft_radius + fin_span, fin_tip_chord)     # Tip, leading edge
p4 = (shaft_radius - overlap, fin_root_chord)     # Root, leading edge

fin_single = (
    cq.Workplane("XZ")
    .polyline([p1, p2, p3, p4])
    .close()
    .extrude(fin_thickness / 2.0, both=True)  # Extrude symmetrically
)

# 3. Create the array of fins by rotating and uniting
fins = fin_single
for i in range(1, num_fins):
    angle = i * (360.0 / num_fins)
    # Rotate around the Z-axis: rotate(axis_start, axis_end, angle)
    rotated_fin = fin_single.rotate((0, 0, 0), (0, 0, 1), angle)
    fins = fins.union(rotated_fin)

# 4. Combine the shaft and the fin assembly
result = shaft.union(fins)