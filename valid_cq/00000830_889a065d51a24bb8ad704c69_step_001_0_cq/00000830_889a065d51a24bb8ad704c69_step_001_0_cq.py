import cadquery as cq

# Parametric dimensions
plate_length = 80.0
plate_width = 50.0
plate_thickness = 2.0

hole_diameter = 20.0
hole_spacing = 40.0  # Center-to-center distance

tab_width = 5.0
tab_length = 8.0
tab_spacing = 10.0 # Center-to-center distance between tabs
notch_width = 4.0
notch_depth = 2.0
notch_position_from_edge = 2.0 # Offset from the main plate edge into the tab

# Create the main rectangular plate
# We center it on XY plane for easier symmetry operations
main_plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Create the two large holes
# Positioned symmetrically along the X-axis
holes = (
    cq.Workplane("XY")
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .circle(hole_diameter / 2)
    .extrude(plate_thickness)
)

# Define the tab geometry
# We'll create one tab profile and then position/mirror it or create both explicitly
# Looking at the image, the tabs stick out from one of the long edges (let's say -Y side)

# Calculate positions for the tabs
# They are centered around X=0 on the -Y face
tab_y_pos = -plate_width / 2
left_tab_x = -tab_spacing / 2
right_tab_x = tab_spacing / 2

# Create the tabs
# Strategy: Sketch on the XY plane, extrude, and union
tabs = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness/2) # Start at bottom face
    .center(0, tab_y_pos) # Move origin to the edge
    # Create points for the two tabs
    .pushPoints([(left_tab_x, -tab_length/2), (right_tab_x, -tab_length/2)]) 
    .rect(tab_width, tab_length)
    .extrude(plate_thickness)
)

# Define the small notch cutout between/on the tabs
# It looks like a small rectangular cutout bridging the space between the tabs 
# or cutting into the plate edge between them.
# Looking closely at the image: There is a small rectangular cutout centered 
# between the tabs, effectively making a 'T' shape negative space or a keying slot.
# It cuts into the main plate slightly and into the space between tabs.

# Let's interpret the notch feature:
# It seems to be a cutout centered at X=0 on the edge where the tabs are.
center_notch = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness/2)
    .center(0, tab_y_pos)
    .rect(notch_width, notch_depth * 2) # *2 to ensure it cuts through the edge
    .extrude(plate_thickness)
)

# Combine operations
result = (
    main_plate
    .cut(holes)          # Remove main holes
    .union(tabs)         # Add the protruding tabs
    .cut(center_notch)   # Cut the small notch between tabs
)

# Export or visualize would happen here, but the prompt asks for the variable 'result'