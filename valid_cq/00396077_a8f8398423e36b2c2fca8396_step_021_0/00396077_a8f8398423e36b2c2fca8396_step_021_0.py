import cadquery as cq

# --- Parameters ---
height = 120.0          # Total vertical height of the bracket
width = 45.0            # Base width of the bracket
thickness = 6.0         # Thickness of the material
fillet_radius = 20.0    # Radius for the rounded bottom corner

# Tab (mounting lug) configuration
tab_protrusion = 5.0    # How far the tabs extend backwards
tab_height = 10.0       # Vertical length of the tabs
tab_bottom_y = 30.0     # Y position of the bottom tab
tab_top_y = 90.0        # Y position of the top tab

# --- Geometry Construction ---

# Define the vertices of the profile loop
# Starting from the origin (0,0) which corresponds to the bottom-inner corner
points = []

# 1. Start at origin
points.append((0, 0))

# 2. Draw bottom edge to the outer corner
points.append((width, 0))

# 3. Draw hypotenuse to the top tip
points.append((0, height))

# 4. Draw the back edge including the tabs, moving from top down to bottom
# Top Tab
points.append((0, tab_top_y + tab_height))          # Top of upper tab on wall
points.append((-tab_protrusion, tab_top_y + tab_height)) # Outer top corner
points.append((-tab_protrusion, tab_top_y))              # Outer bottom corner
points.append((0, tab_top_y))                       # Bottom of upper tab on wall

# Bottom Tab
points.append((0, tab_bottom_y + tab_height))       # Top of lower tab on wall
points.append((-tab_protrusion, tab_bottom_y + tab_height)) # Outer top corner
points.append((-tab_protrusion, tab_bottom_y))           # Outer bottom corner
points.append((0, tab_bottom_y))                    # Bottom of lower tab on wall

# Note: The .close() method will automatically connect the last point back to (0,0)

# --- Generate Solid ---

result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# Apply the fillet to the bottom-outer corner
# We select the vertical edge located at (width, 0)
result = result.edges(cq.NearestToPointSelector((width, 0, 0))).fillet(fillet_radius)