import cadquery as cq

# --- Parametric Dimensions ---
base_width = 80.0
base_length = 80.0
base_height = 15.0

wall_thickness = 5.0
pocket_depth = 10.0  # Depth of the inner pocket

center_hole_diameter = 30.0

tab_width = 20.0
tab_length = 15.0
tab_height = 8.0  # Height of the mounting tabs relative to bottom
tab_hole_diameter = 6.0

# --- Geometry Construction ---

# 1. Create the main base block
main_body = cq.Workplane("XY").box(base_length, base_width, base_height)

# 2. Create the inner pocket (hollow out the top)
# We subtract a smaller box from the top face
pocket = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2)  # Move to top face
    .rect(base_length - 2*wall_thickness, base_width - 2*wall_thickness)
    .extrude(-pocket_depth)
)

result = main_body.cut(pocket)

# 3. Create the central hole
result = (
    result.faces(">Z")
    .workplane()
    .hole(center_hole_diameter)
)

# 4. Create the mounting tabs
# There are 4 tabs, positioned on the sides.
# Looking at the image, there are two tabs on the "front" face and two on the "back" face (or left/right depending on orientation).
# Let's assume they are on the sides along the X-axis (front and back in Y).

# Define a function or loop to add tabs, or union them all at once.
# Let's create one tab shape first.
tab_x_offset = (base_length / 2) - (tab_width / 2)
tab_y_offset = (base_width / 2) + (tab_length / 2)
tab_z_pos = -base_height/2 + tab_height/2

# Helper to create a single tab with a hole
def create_tab(x_pos, y_pos):
    t = (
        cq.Workplane("XY")
        .workplane(offset=tab_z_pos)
        .center(x_pos, y_pos)
        .box(tab_width, tab_length, tab_height)
    )
    # Add hole to tab
    t = (
        t.faces(">Z")
        .workplane()
        .hole(tab_hole_diameter)
    )
    return t

# Coordinates for the 4 tabs
# The image shows tabs aligned with the corners but slightly inset or flush with corners?
# Looking closely, the tabs seem flush with the outer corners of the main box along the width.
# The tabs protrude OUT from the main body.

# Tab 1: Front-Left
tab1 = create_tab(-tab_x_offset, -tab_y_offset)
# Tab 2: Front-Right
tab2 = create_tab(tab_x_offset, -tab_y_offset)
# Tab 3: Back-Left
tab3 = create_tab(-tab_x_offset, tab_y_offset)
# Tab 4: Back-Right
tab4 = create_tab(tab_x_offset, tab_y_offset)

# Union the tabs to the main body
result = result.union(tab1).union(tab2).union(tab3).union(tab4)

# 5. Add holes inside the pocket (corners)
# The image shows 4 small holes in the bottom of the pocket, near the corners.
# These match the tab locations roughly but are inside the wall.
inner_hole_spacing = base_width - 2*wall_thickness - 15 # Inset somewhat
inner_hole_diameter = 4.0

result = (
    result.faces(">Z[1]") # Select the bottom face of the pocket (it's the second highest Z face usually)
    .workplane()
    .rect(inner_hole_spacing, inner_hole_spacing, forConstruction=True)
    .vertices()
    .hole(inner_hole_diameter)
)

# Ensure the 'result' variable exists for export/visualization
if 'show_object' in globals():
    show_object(result)