import cadquery as cq

# --- Parameters ---
length = 200.0         # Total length of the part
height = 35.0          # Height of the main strip
thickness = 3.0        # Material thickness
tab_height = 15.0      # Extra height for the end tabs
tab_width = 15.0       # Width of the end tabs
fillet_radius = 12.0   # Radius of the internal fillet on the left
corner_radius = 35.0   # Radius of the bottom-right curve (matches height for full curve)
slot_width = 2.5       # Width of the notches
slot_depth = 10.0      # Depth of the notches
num_main_slots = 7     # Number of slots along the main edge

# --- Geometry Construction ---

# Define the points for the base profile polygon (counter-clockwise)
pts = [
    (0, 0),                                      # Bottom Left
    (length, 0),                                 # Bottom Right (sharp corner, to be filleted)
    (length, height + tab_height),               # Top Right (Top of right tab)
    (length - tab_width, height + tab_height),   # Inner Top Right
    (length - tab_width, height),                # Inner Bottom Right (Transition to strip)
    (tab_width, height),                         # Inner Bottom Left (Transition to tab)
    (tab_width, height + tab_height),            # Inner Top Left
    (0, height + tab_height)                     # Top Left (Top of left tab)
]

# Create the base solid by extruding the profile
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# --- Apply Fillets ---

# 1. Bottom Right Large Curve
# Select the vertical edge at the bottom right corner
# This rounds the sharp corner at (length, 0) in the XY plane
result = result.edges(cq.NearestToPointSelector((length, 0))).fillet(corner_radius)

# 2. Left Internal Fillet
# Select the vertical edge at the inner left corner where the tab meets the strip
result = result.edges(cq.NearestToPointSelector((tab_width, height))).fillet(fillet_radius)

# --- Create Slots ---

# Calculate slot positions (x coordinates and y reference)
slot_configs = []

# Slot on the Left Tab (Centered on tab)
slot_configs.append({
    'x': tab_width / 2.0,
    'y_top': height + tab_height
})

# Slot on the Right Tab (Centered on tab)
slot_configs.append({
    'x': length - tab_width / 2.0,
    'y_top': height + tab_height
})

# Slots along the main strip
# Distribute them evenly between the left fillet end and the right tab
start_x = tab_width + fillet_radius + slot_width
end_x = length - tab_width - slot_width * 2
step = (end_x - start_x) / (num_main_slots - 1)

for i in range(num_main_slots):
    x_pos = start_x + i * step
    slot_configs.append({
        'x': x_pos,
        'y_top': height
    })

# Execute Cuts for each slot
for slot in slot_configs:
    # Create a cutter object (Box)
    # The box is positioned to cut downwards from the top edge 'y_top'
    # Height is set to 2*depth to ensure clean intersection
    cutter = (
        cq.Workplane("XY")
        .box(slot_width, slot_depth * 2, thickness * 2)
        .translate((slot['x'], slot['y_top'], thickness / 2.0))
    )
    
    # Boolean subtraction
    result = result.cut(cutter)

# Result is stored in the 'result' variable