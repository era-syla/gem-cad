import cadquery as cq

# Parametric dimensions for the Monitor
# Base dimensions
base_width = 120.0
base_depth = 80.0
base_height = 5.0

# Stand (Neck) dimensions
stand_width = 20.0
stand_depth = 15.0
stand_height = 80.0
stand_offset_from_back = 10.0 # How far forward the stand is from the very back edge of the base

# Screen dimensions
screen_width = 200.0
screen_height = 120.0
screen_thickness = 10.0
screen_elevation = 40.0 # Height of bottom of screen from the ground (approx)

# Connector (Back mount) dimensions
connector_width = 40.0
connector_height = 30.0
connector_thickness = 10.0

# --- Building the Parts ---

# 1. Base
# Centered on XY plane, extruded upwards
base = cq.Workplane("XY").box(base_width, base_depth, base_height)

# 2. Stand (Neck)
# Positioned relative to the base. 
# It sits on top of the base and is centered horizontally, but offset towards the back.
stand = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2) # Start on top of the base (since box centers Z)
    .center(0, (base_depth/2) - stand_depth/2 - stand_offset_from_back)
    .box(stand_width, stand_depth, stand_height, centered=(True, True, False))
)

# 3. Connector Block
# This attaches the stand to the screen. 
# It sits near the top of the stand.
connector_center_z = base_height + stand_height - (connector_height/2) - 5
connector = (
    cq.Workplane("XY")
    .workplane(offset=connector_center_z)
    .center(0, (base_depth/2) - stand_depth - stand_offset_from_back - (connector_thickness/2))
    .box(connector_width, connector_thickness, connector_height)
)

# 4. Screen
# The main display panel.
# Positioned in front of the connector block.
screen_z_center = base_height + screen_elevation + (screen_height/2)
screen_y_center = (base_depth/2) - stand_depth - stand_offset_from_back - connector_thickness - (screen_thickness/2)

screen = (
    cq.Workplane("XY")
    .workplane(offset=screen_z_center)
    .center(0, screen_y_center)
    .box(screen_width, screen_thickness, screen_height)
)

# --- Assembly ---

# Combine all solid parts into one object
result = base.union(stand).union(connector).union(screen)

# Export or display (standard CadQuery practice)
if 'show_object' in globals():
    show_object(result)