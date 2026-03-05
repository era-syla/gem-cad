import cadquery as cq

# --- Parametric Dimensions ---
height_right = 160.0    # Overall height at the right edge
height_left = 140.0     # Overall height at the left edge
width = 40.0            # Width of the main web
thickness = 2.0         # Thickness of the web plate
rib_depth = 8.0         # Depth of stiffeners protruding from the web
rib_thickness = 2.0     # Thickness of the stiffeners/ribs
tab_length = 6.0        # Length of the mounting tabs extending beyond width
hole_diameter = 2.5     # Diameter of mounting holes
num_ribs = 4            # Total number of horizontal ribs (including top/bottom)
mid_stiffener_x = 15.0  # Position of the middle vertical stiffener from left

# --- Helper Logic ---
# Calculate slope of the top edge
slope = (height_right - height_left) / width

def get_top_y(x):
    """Returns the Y coordinate of the slanted top edge at a given X."""
    return height_left + slope * x

# --- 1. Base Web Generation ---
# Create the main back plate (trapezoidal shape)
pts = [
    (0, 0),
    (width, 0),
    (width, height_right),
    (0, height_left)
]
web = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# --- 2. Vertical Stiffeners ---
# We create oversized vertical bars and then cut them to match the top slant.
stiffeners_plane = cq.Workplane("XY").workplane(offset=thickness)

# Middle Stiffener
vs_mid = (
    stiffeners_plane
    .moveTo(mid_stiffener_x, 0)
    .rect(rib_thickness, height_right + 50, centered=(True, False))
    .extrude(rib_depth)
)

# Right Edge Stiffener (Flush with the right edge)
vs_right = (
    stiffeners_plane
    .moveTo(width - rib_thickness/2, 0)
    .rect(rib_thickness, height_right + 50, centered=(True, False))
    .extrude(rib_depth)
)

verticals = vs_mid.union(vs_right)

# Define cutting tool for the top slant
# Polygon covering the area above the top edge
cut_pts = [
    (0, height_left),
    (width + tab_length + 10, get_top_y(width + tab_length + 10)),
    (width + tab_length + 10, height_right + 100),
    (0, height_right + 100)
]
cutter = cq.Workplane("XY").polyline(cut_pts).close().extrude(100)

# Cut the verticals
verticals = verticals.cut(cutter)

# --- 3. Horizontal Ribs (Bottom & Middle) ---
# Calculate Y spacing
spacing = height_right / (num_ribs - 1)
y_locs = [i * spacing for i in range(num_ribs)]

# Sketch horizontal ribs on the web face
h_ribs_sketch = cq.Workplane("XY").workplane(offset=thickness)

for i, y in enumerate(y_locs[:-1]): # Iterate all except the top one
    # Determine center Y (Bottom rib is flush, others centered)
    if i == 0:
        cy = rib_thickness / 2
    else:
        cy = y
    
    # Determine length (Web width + Tab extension)
    total_len = width + tab_length
    cx = total_len / 2
    
    h_ribs_sketch = h_ribs_sketch.moveTo(cx, cy).rect(total_len, rib_thickness)

h_ribs = h_ribs_sketch.extrude(rib_depth)

# --- 4. Top Slanted Rib ---
# Construct a polygon that follows the top edge and extends to the tab
p1 = (0, height_left)
p2 = (width + tab_length, get_top_y(width + tab_length))
# Offset downwards by rib_thickness to form the rib body
p3 = (p2[0], p2[1] - rib_thickness)
p4 = (p1[0], p1[1] - rib_thickness)

top_rib = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .polyline([p1, p2, p3, p4])
    .close()
    .extrude(rib_depth)
)

# --- 5. Assemble Geometry ---
result = web.union(verticals).union(h_ribs).union(top_rib)

# --- 6. Mounting Holes ---
# Calculate centers for holes on the tabs
hole_x = width + tab_length / 2
hole_centers = []

for i, y in enumerate(y_locs):
    if i == 0:
        # Bottom hole
        hole_centers.append((hole_x, rib_thickness/2))
    elif i == num_ribs - 1:
        # Top hole (centered on the slanted rib)
        hole_centers.append((hole_x, get_top_y(hole_x) - rib_thickness/2))
    else:
        # Middle holes
        hole_centers.append((hole_x, y))

# Cut the holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_centers)
    .hole(hole_diameter)
)

# --- 7. Final Detailing (Fillets on Tabs) ---
# Select vertical edges of the tabs (x > width) and fillet them
try:
    result = result.edges("|Z").select(lambda e: e.center().x > width + 0.1).fillet(tab_length/2.5)
except Exception:
    pass # Skip fillet if geometry prevents it