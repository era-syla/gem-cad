import cadquery as cq

# --- Parametric Dimensions ---
plate_width = 220.0     # Main square width
plate_length = 220.0    # Main square length
plate_thickness = 4.0   # Thickness of the plate

# Tab dimensions
tab_width = 30.0        # How far the tab sticks out
tab_length = 50.0       # Length of the tab along the plate edge
tab_fillet = 5.0        # Fillet radius at tab corners

# Hole dimensions
hole_diameter = 3.5     # Diameter of mounting holes
hole_offset = 5.0       # Distance from tab edge to hole center

# --- Geometry Construction ---

# 1. Create the main central plate
main_plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Define the tab locations and geometry
# We will create one tab and then mirror/union it to the other positions
# Position: centered on Y, offset on X to sticking out

# Calculate tab center position relative to center of plate
# The tab is attached to the "length" sides (left and right in typical orientation)
# Let's attach tabs to the left and right sides first.
# Wait, looking at the image, there are 4 tabs. 
# They are not at the corners, but offset slightly or centered on the sides?
# Looking closely at the image:
# It's a large square. There are 4 tabs extending from the two opposite sides (let's say Left and Right).
# On the Left side, there are two tabs near the corners.
# On the Right side, there are two tabs near the corners.
# Actually, looking at the perspective, it looks like a heated bed support plate or similar.
# It seems to have a "butterfly" shape or "H" shape variant.
# Let's re-evaluate: It looks like a square plate with rectangular cutouts at the corners, leaving tabs.
# Or, a square plate with tabs added.
# Let's assume it's a central square with 4 tabs attached near the corners.

# Revised Strategy:
# Create a sketch.
# Rectangle (Main Body).
# Add 4 small rectangles for tabs.
# Extrude.
# Fillet.
# Drill holes.

# Let's determine positions.
# Let's assume the tabs are symmetric.
# Let's assume the tabs are flush with the top/bottom edges (Y-axis) and extend outwards on X-axis?
# No, looking at the image, the tabs are recessed slightly from the corners. 
# Let's look at the bottom-left corner of the top plate. The tab is extending from the side edge, but its top edge is flush with the main plate's corner? 
# Actually, it looks like the tab is centered on the corner? No, that would be diagonal.
# It looks like the tabs are extensions of the side edges.
# Let's try this: A base rectangle (width x length). 
# Then 4 tabs protruding from the sides.
# Let's place the tabs at specific offsets from the Y-center.

tab_y_offset = (plate_width / 2) - (tab_length / 2) - 15.0 # Distance from center Y to center of tab. 15mm indent from corner.
tab_x_pos = plate_length / 2

def create_tab(loc_x, loc_y):
    return (
        cq.Workplane("XY")
        .center(loc_x, loc_y)
        .box(tab_width * 2, tab_length, plate_thickness) # Width*2 to ensure overlap for union
    )

# Create the 4 tabs using the logic
# Top Right
tab1 = create_tab(tab_x_pos, tab_y_offset)
# Bottom Right
tab2 = create_tab(tab_x_pos, -tab_y_offset)
# Top Left
tab3 = create_tab(-tab_x_pos, tab_y_offset)
# Bottom Left
tab4 = create_tab(-tab_x_pos, -tab_y_offset)

# Union everything
result = main_plate.union(tab1).union(tab2).union(tab3).union(tab4)

# 3. Apply Fillets
# We want to fillet the outer corners of the tabs and the inner corners where tabs meet plate
# Select edges parallel to Z
result = result.edges("|Z").fillet(2.0)

# 4. Drill Holes
# Holes are located in the center of the protruding part of the tab usually, or offset from the edge.
# Let's put them relative to the tab extremities.

# Calculate hole coordinates
h_x = (plate_length / 2) + (tab_width / 2) 
h_y = tab_y_offset

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (h_x, h_y),
        (h_x, -h_y),
        (-h_x, h_y),
        (-h_x, -h_y)
    ])
    .hole(hole_diameter)
)

# Optional: Add the slight insulation pad look (the top layer in the image)
# The image shows two distinct objects or a bi-material object.
# The request asks for "this 3D CAD model". Usually implies the geometry.
# The image shows a metal plate (bottom) and a possibly heated bed or surface (top).
# I will model the main metal carriage plate (the complex shape) as a single solid, 
# as that is the primary engineering component shown. The top grey square looks like a separate component (glass/build surface).
# However, to be thorough, let's look if it's a single part with a recess.
# It looks like two plates stacked. I will generate the complex bottom plate as 'result'
# since that contains the distinct geometric features (tabs, holes).
# If it were an assembly, the prompt usually specifies. I will stick to the detailed support plate.

# Refined Logic for the specific shape in image:
# The tabs in the image actually look like they are flush with the main edges in one dimension.
# Let's look at the bottom-left tab. It extends out to the left. Its bottom edge aligns with the bottom edge of the main plate?
# No, there is a clear notch. The tab is narrower than the side.
# Let's assume the `tab_y_offset` logic used above is correct (indented from corners).

# Final adjustment to ensure clean geometry
result = result.combine()