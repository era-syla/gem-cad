import cadquery as cq

# --- Parameters ---
thickness = 2.0  # Sheet metal thickness
height = 150.0   # Total height of the panel
width_main = 120.0 # Width of the larger flat face
width_side = 40.0  # Width of the side face with vents

# Vent parameters
vent_slot_width = 3.0
vent_slot_height = 12.0
vent_spacing_y = 18.0 # Vertical pitch between rows
vent_spacing_x = 6.0  # Horizontal pitch between columns in a pair
num_vent_rows = 7
num_vent_cols = 2

# Tab parameters (locking tabs on edges)
tab_width = 4.0
tab_height = 3.0
tab_positions_top = [width_side * 0.3, width_main * 0.2, width_main * 0.8] # Relative positions roughly
tab_positions_side = [height * 0.5, height * 0.2] # Roughly middle and bottom

# --- Geometry Construction ---

# 1. Base L-Shape Profile
# We will create an L-shaped profile and extrude it, or create a shell. 
# Given it's a sheet metal part, creating a solid block and shelling or 
# creating the profile path is best. Let's do a profile path extrusion.

# Create the L-shape wire
path = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(width_side, 0)        # Side leg
    .lineTo(width_side, width_main) # Main leg (making a corner)
)

# Thicken the wire to create the sheet metal base
# We offset the wire to create the thickness
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, width_main)
    .lineTo(-width_side, width_main) # Note direction change for L-shape coordinate logic
    .offset2D(thickness/2, kind='intersection') # Create the thickness
    .extrude(height)
)

# Re-approach: It's simpler to make two plates and union them to ensure sharp corners and easy sketching.
# Let's make the Side Plate (with vents) and the Main Plate.

# -- Side Plate (XZ plane mostly) --
side_plate = (
    cq.Workplane("YZ")
    .box(width_side, height, thickness, centered=(False, True, True))
    .translate((-width_side, 0, 0)) # Position it
)

# -- Main Plate (YZ plane mostly) --
main_plate = (
    cq.Workplane("XZ")
    .box(width_main, height, thickness, centered=(False, True, True))
)

# Combine them into the L-bracket
L_bracket = side_plate.union(main_plate)

# 2. Add Vents to the Side Plate
# The vents are pairs of slots running vertically.

# Calculate start position for vents
vent_start_y = height/2 - ((num_vent_rows - 1) * vent_spacing_y) / 2
vent_x_offset = -width_side / 2 # Center of the side plate roughly

def create_vent_slot(loc):
    return cq.Solid.makeBox(vent_slot_width, vent_slot_height, thickness * 3)

# Create a sketch for the cutouts
vent_cutout = (
    cq.Workplane("YZ")
    .workplane(offset=0) # Surface of the side plate
    .pushPoints([
        (-width_side + 12.0, (i * vent_spacing_y) - height/2 + 20) 
        for i in range(num_vent_rows)
    ])
    .rect(vent_slot_width, vent_slot_height)
    .pushPoints([
        (-width_side + 12.0 + vent_spacing_x, (i * vent_spacing_y) - height/2 + 20) 
        for i in range(num_vent_rows)
    ])
    .rect(vent_slot_width, vent_slot_height)
    .extrude(thickness * 2) # Cut through
)

# Apply cuts
result = L_bracket.cut(vent_cutout)


# 3. Add Tabs (Protrusions)
# There are tabs on the top edge of both panels and the side edge of the side panel.

# Tabs on Top Edge (Main Panel)
top_tabs_main = (
    cq.Workplane("XY")
    .workplane(offset=height/2)
    .moveTo(width_main * 0.25, 0)
    .rect(tab_width, thickness)
    .moveTo(width_main * 0.85, 0)
    .rect(tab_width, thickness)
    .extrude(tab_height)
)

# Tabs on Top Edge (Side Panel)
top_tabs_side = (
    cq.Workplane("XY")
    .workplane(offset=height/2)
    .moveTo(0, -width_side + 5) # Coordinate system relative to the union might be tricky, adjusting
    .rect(thickness, tab_width)
    .extrude(tab_height)
)

# Correcting coordinates based on visual estimation of the union
# The union origin is at the corner.
# Main plate extends +X. Side plate extends -Y (based on previous logic).

# Let's refine the specific coordinates for clarity
# Main Plate: X from 0 to 120, Z from -75 to 75, Y from -1 to 1 (thickness)
# Side Plate: Y from -40 to 0, Z from -75 to 75, X from -1 to 1 (thickness)

# Re-doing the main structure for absolute clarity on coordinates
final_L = (
    cq.Workplane("XY")
    # Draw L profile
    .moveTo(0,0)
    .lineTo(width_main, 0)
    .lineTo(width_main, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, width_side)
    .lineTo(0, width_side)
    .close()
    .extrude(height)
)

# Vents on the side face (which is now in YZ plane roughly)
# Side face is at X=0..thickness, Y=thickness..width_side
vent_centers = []
start_z = 20.0
for r in range(num_vent_rows):
    z_pos = start_z + (r * vent_spacing_y)
    # Column 1
    vent_centers.append((thickness + 10, z_pos)) 
    # Column 2
    vent_centers.append((thickness + 10 + vent_spacing_x, z_pos))

# Create the cutter
cutter_sketch = (
    cq.Workplane("YZ")
    .workplane(offset=-5) # Start outside
    .pushPoints(vent_centers)
    .rect(vent_slot_width, vent_slot_height)
    .extrude(20) # Cut through X
)

result = final_L.cut(cutter_sketch)

# Add Top Tabs
# Tabs on the top face (Z = height)
top_tabs_sketch = (
    cq.Workplane("XY")
    .workplane(offset=height)
    # Tab on side leg
    .moveTo(thickness/2, width_side - 5)
    .rect(thickness, tab_width)
    # Tab on corner area
    .moveTo(thickness/2, width_side - 30) # A second tab on the side leg based on image
    .rect(thickness, tab_width)
    # Tab on main leg far end
    .moveTo(width_main - 10, thickness/2)
    .rect(tab_width, thickness)
    # Tab on main leg near corner
    .moveTo(40, thickness/2)
    .rect(tab_width, thickness)
    .extrude(tab_height)
)

# Add fillet to tabs for the rounded look
top_tabs = top_tabs_sketch.edges("|Z").fillet(0.5)

result = result.union(top_tabs)


# Add Side/Front Tabs (on the edge of the side panel)
# These stick out in the -Y direction from the face at X=0
side_tabs_sketch = (
    cq.Workplane("XZ")
    .workplane(offset=-width_side) # At the far edge of the side panel?
    # Actually, looking at the image, there is a tab sticking out of the THICKNESS of the main plate on the right
    # And a tab sticking out of the front edge of the side plate.
)

# Right edge tab (Main plate, right side)
right_tab = (
    cq.Workplane("YZ")
    .workplane(offset=width_main)
    .moveTo(thickness/2, height * 0.6)
    .rect(thickness, tab_width)
    .extrude(tab_height) # Extrudes in +X
    .edges("|X").fillet(0.4)
)

# Front edge tabs (Side plate, front edge)
# These protrude from the face at Y=width_side
front_tabs = (
    cq.Workplane("XZ")
    .workplane(offset=width_side)
    .moveTo(thickness/2, height * 0.25)
    .rect(thickness, tab_width)
    .moveTo(thickness/2, height * 0.15) # A lower one
    .rect(thickness, tab_width)
    .extrude(tab_height) # Extrudes in +Y
    .edges("|Y").fillet(0.4)
)

result = result.union(right_tab).union(front_tabs)

# Fillet the inner corner for strength and realism
result = result.edges(cq.selectors.NearestToPointSelector((thickness, thickness, height/2))).fillet(thickness/2)
