import cadquery as cq

# --- Parameters ---
length = 200.0          # Total length of the main beam
width = 20.0            # Width of the beam (Y direction)
height_left = 28.0      # Height at the left end
height_pivot = 38.0     # Height at the pivot point
height_right = 16.0     # Height at the right end
pivot_x = 70.0          # X position of the pivot peak
wall_th = 2.0           # Wall thickness
truss_th = 3.0          # Thickness of the truss struts
num_bays_left = 3       # Number of truss bays left of pivot
num_bays_right = 6      # Number of truss bays right of pivot

# --- 1. Create Main Hull ---
# Define profile points for the side view (XZ plane)
pts_hull = [
    (0, 0),
    (0, height_left),
    (pivot_x, height_pivot),
    (length, height_right),
    (length, 0)
]

# Extrude the solid block
hull = cq.Workplane("XZ").polyline(pts_hull).close().extrude(width/2.0, both=True)

# Create Inner Void for hollowing (using 2D offset)
inner_void = (
    cq.Workplane("XZ")
    .polyline(pts_hull)
    .close()
    .offset2D(-wall_th)
    .extrude(width/2.0 - wall_th, both=True)
)

# Create the hollow beam structure
beam = hull.cut(inner_void)

# --- 2. Create Side Truss Pattern (X-Bracing) ---
# We define a helper function to create triangular cutouts for the X-brace pattern
def add_truss_bays(wp, x_start, x_end, h_start, h_end, num_bays):
    dx = (x_end - x_start) / num_bays
    slope = (h_end - h_start) / (x_end - x_start)
    
    for i in range(num_bays):
        # Calculate X boundaries for this bay
        bx0 = x_start + i * dx
        bx1 = bx0 + dx
        
        # Calculate cut boundaries (inset by strut thickness/walls)
        # Use wall_th for the very ends of the beam, truss_th for internal struts
        pad_l = wall_th + truss_th/2 if (i == 0 and x_start == 0) else truss_th/2
        pad_r = wall_th + truss_th/2 if (i == num_bays-1 and x_end == length) else truss_th/2
        
        vx0 = bx0 + pad_l
        vx1 = bx1 - pad_r
        
        # Calculate Y boundaries (interpolating slope)
        y_top_0 = h_start + slope * (vx0 - x_start) - wall_th
        y_top_1 = h_start + slope * (vx1 - x_start) - wall_th
        y_bot = wall_th
        
        # Center point of the X
        cx = (vx0 + vx1) / 2
        cy = (y_top_0 + y_top_1)/2 / 2 + y_bot/2
        
        # Gap size to define the strut width roughly
        gap = truss_th / 2.5
        
        # Define 4 triangular cutouts per bay to leave an X-brace
        # Top Triangle
        wp = wp.polyline([(vx0 + gap, y_top_0), (vx1 - gap, y_top_1), (cx, cy + gap)]).close()
        # Bottom Triangle
        wp = wp.polyline([(vx0 + gap, y_bot), (vx1 - gap, y_bot), (cx, cy - gap)]).close()
        # Left Triangle
        wp = wp.polyline([(vx0, y_bot + gap), (vx0, y_top_0 - gap), (cx - gap, cy)]).close()
        # Right Triangle
        wp = wp.polyline([(vx1, y_bot + gap), (vx1, y_top_1 - gap), (cx + gap, cy)]).close()
        
    return wp

# Initialize Workplane for the cutter
truss_cutter_sketch = cq.Workplane("XZ")

# Add bays for Left Section
truss_cutter_sketch = add_truss_bays(
    truss_cutter_sketch, 0, pivot_x, height_left, height_pivot, num_bays_left
)
# Add bays for Right Section
truss_cutter_sketch = add_truss_bays(
    truss_cutter_sketch, pivot_x, length, height_pivot, height_right, num_bays_right
)

# Extrude the cutter sketch through the beam
truss_tool = truss_cutter_sketch.extrude(width + 10, both=True)
beam = beam.cut(truss_tool)

# --- 3. Top Lightening Holes ---
# Left Section Holes
for i in range(num_bays_left):
    t = (i + 0.5) / num_bays_left
    cx = pivot_x * t
    cz = height_left + (height_pivot - height_left) * t
    # Cut a rectangular hole
    beam = beam.cut(
        cq.Workplane("XY")
        .rect(12, 10, centered=True)
        .extrude(20)
        .translate((cx, 0, cz - 10))
    )

# Right Section Holes
for i in range(num_bays_right):
    t = (i + 0.5) / num_bays_right
    cx = pivot_x + (length - pivot_x) * t
    cz = height_pivot + (height_right - height_pivot) * t
    # Cut a rectangular hole
    beam = beam.cut(
        cq.Workplane("XY")
        .rect(15, 10, centered=True)
        .extrude(20)
        .translate((cx, 0, cz - 10))
    )

# --- 4. Attachments ---

# Left Handle (Loop)
handle_pts = [
    (0, height_left),
    (-40, height_left),
    (-60, height_left/2),
    (-40, 0),
    (0, 0)
]
handle = cq.Workplane("XZ").polyline(handle_pts).close().extrude(width/2, both=True)
# Hollow out the handle
handle_void_pts = [
    (-wall_th, height_left-wall_th),
    (-38, height_left-wall_th),
    (-56, height_left/2),
    (-38, wall_th),
    (-wall_th, wall_th)
]
handle_void = cq.Workplane("XZ").polyline(handle_void_pts).close().extrude(width/2 - wall_th, both=True)
handle = handle.cut(handle_void)

# Pivot Lug (Top Tab)
lug = (
    cq.Workplane("XZ")
    .moveTo(pivot_x - 8, height_pivot)
    .lineTo(pivot_x, height_pivot + 12)
    .lineTo(pivot_x + 8, height_pivot)
    .close()
    .extrude(4, both=True) # Thinner tab
)
# Add hole to lug
lug = lug.cut(
    cq.Workplane("XZ")
    .moveTo(pivot_x, height_pivot + 5)
    .circle(2.5)
    .extrude(10, both=True)
)

# Right End Hook
hook = (
    cq.Workplane("XZ")
    .moveTo(length, height_right)
    .lineTo(length, height_right + 10)
    .lineTo(length - 8, height_right + 10)
    .lineTo(length - 8, height_right + 6)
    .lineTo(length - 4, height_right + 3)
    .lineTo(length, height_right)
    .close()
    .extrude(width/2, both=True)
)

# --- 5. Combine All Parts ---
result = beam.union(handle).union(lug).union(hook)