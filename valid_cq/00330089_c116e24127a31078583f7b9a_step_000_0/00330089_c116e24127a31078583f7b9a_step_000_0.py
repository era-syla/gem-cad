import cadquery as cq

# --- Parametric Dimensions ---
# Handle
handle_len = 90.0
handle_max_dia = 32.0
handle_neck_dia = 16.0
collar_dia = 26.0
collar_height = 6.0
fillet_radius = 2.0

# Shaft
shaft_dia = 6.0
shaft_len = 90.0  # Length extending from the handle

# Tip
tip_len = 12.0
tip_thk = 0.8
tip_width = 6.0

# Derived parameters
r_max = handle_max_dia / 2.0
r_neck = handle_neck_dia / 2.0
r_collar = collar_dia / 2.0
r_shaft = shaft_dia / 2.0

# --- 1. Create the Handle ---
# Define the profile points for the ergonomic grip (XZ plane)
# Starting from the bottom center (0,0) up to the neck
p0 = (0, 0)
p1 = (r_max * 0.4, handle_len * 0.1)
p2 = (r_max, handle_len * 0.45)           # Widest point of the handle
p3 = (r_neck, handle_len - collar_height - 2.0) # Neck constriction

# Create the solid of revolution for the handle
handle = (
    cq.Workplane("XZ")
    .moveTo(*p0)
    .spline([p1, p2, p3], includeCurrent=True)
    .lineTo(r_collar, handle_len - collar_height)  # Flare out to the collar
    .lineTo(r_collar, handle_len)                  # Vertical side of collar
    .lineTo(0, handle_len)                         # Flat top
    .close()
    .revolve(360)
)

# Apply a fillet to the sharp transition at the neck (under the collar)
# We select edges based on Z height range and radius
try:
    neck_edges = handle.edges(
        f"(>Z[{handle_len * 0.5}]) and (<Z[{handle_len - 1.0}]) and (>Y[{r_neck - 2.0}])"
    )
    handle = neck_edges.fillet(fillet_radius)
except Exception:
    pass # Fallback if fillet fails due to geometric constraints

# --- 2. Create the Shaft ---
# Extrude a cylinder from the top center of the handle
shaft_main_len = shaft_len - tip_len
shaft = (
    cq.Workplane("XY")
    .workplane(offset=handle_len)
    .circle(r_shaft)
    .extrude(shaft_main_len)
)

# --- 3. Create the Tip ---
# Loft from the circular shaft profile to a rectangular flat-head profile
# This creates the tapered wedge shape of the screwdriver tip
tip = (
    shaft.faces(">Z").workplane()
    .circle(r_shaft)                    # Start profile (matches shaft)
    .workplane(offset=tip_len)
    .rect(tip_width, tip_thk)           # End profile (flat blade)
    .loft(combine=True)
)

# --- 4. Assembly ---
# Union all components into the final result
result = handle.union(shaft).union(tip)