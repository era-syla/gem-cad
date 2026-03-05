import cadquery as cq

# --- Parametric Dimensions ---
tube_od = 36.0           # Outer diameter of the main tube
tube_id = 26.0           # Inner diameter of the main tube
tube_length = 45.0       # Total length of the tube

tab_width = 30.0         # Width of the tab (perpendicular to extension)
tab_thickness = 12.0     # Thickness of the tab
tab_extension = 38.0     # Distance from tube center to tab hole center

hole_diameter = 8.5      # Pivot hole diameter
cb_diameter = 20.0       # Counterbore diameter
cb_depth = 3.5           # Counterbore depth

hex_width = 11.0         # Hexagon width (across corners approx)
hex_depth = 4.0          # Depth of hex recess
hex_offset = 19.0        # Distance from tube center to hex center

# --- Modeling ---

# 1. Create the Main Tube
# Aligned along the X-axis (Extruded from YZ plane)
tube = (
    cq.Workplane("YZ")
    .circle(tube_od / 2.0)
    .extrude(tube_length / 2.0, both=True)
)

# 2. Create the Tab Body
# The tab is created on the XY plane.
# It consists of a rectangular section connecting to the tube
# and a rounded end (cylinder) where the hole is.

# Rectangular block
# Positioned to connect tube center to the rounded end center
# Center Y is halfway between 0 and -tab_extension
tab_rect = (
    cq.Workplane("XY")
    .center(0, -tab_extension / 2.0)
    .box(tab_width, tab_extension, tab_thickness)
)

# Rounded End
# A cylinder centered at the hole location
tab_end = (
    cq.Workplane("XY")
    .center(0, -tab_extension)
    .cylinder(tab_thickness, tab_width / 2.0)
)

# Union the base geometries
# Note: The tab rect penetrates the tube; we will clear the bore later.
solid = tube.union(tab_rect).union(tab_end)

# 3. Features and Cuts

# Tube Bore
# Create a cutter for the ID and remove material
bore_cutter = (
    cq.Workplane("YZ")
    .circle(tube_id / 2.0)
    .extrude(tube_length, both=True)
)

# Perform the cuts on the solid
result = (
    solid
    .cut(bore_cutter)  # clear the tube interior
    
    # Pivot Hole (Through)
    .faces(">Z").workplane()
    .center(0, -tab_extension)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
    
    # Counterbore (Blind)
    .faces(">Z").workplane()
    .center(0, -tab_extension)
    .circle(cb_diameter / 2.0)
    .cutBlind(-cb_depth)
    
    # Hexagonal Recess (Blind)
    .faces(">Z").workplane()
    .center(0, -hex_offset)
    .polygon(6, hex_width)
    .cutBlind(-hex_depth)
)