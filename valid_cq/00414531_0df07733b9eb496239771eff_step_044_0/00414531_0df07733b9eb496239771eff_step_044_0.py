import cadquery as cq

# --- Dimensions ---
# Header (Top wide section)
header_width = 60.0
header_length = 24.0
header_height = 16.0
header_fillet = 3.0

# Body (Main section)
body_width = 44.0
body_length = 88.0
body_height = 16.0
body_chamfer = 0.5

# Connector details
conn_trans_w = 28.0 # Transition width
conn_trans_l = 4.0
conn_main_w = 24.0
conn_main_l = 8.0
conn_rib_w = 26.0   # Width of the rib section
conn_rib_l = 4.0

# --- Geometry Construction ---

# 1. Header Section
# Centered at X=0, Y aligned such that interface is at Y=0
header = (
    cq.Workplane("XY")
    .workplane(offset=header_height / 2.0)
    .center(0, header_length / 2.0)
    .box(header_width, header_length, header_height)
    .edges("|Z").fillet(header_fillet)
)

# 2. Main Body Section
# Extends from Y=0 downwards
body = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2.0)
    .center(0, -body_length / 2.0)
    .box(body_width, body_length, body_height)
)

# Union Header and Body
main_shape = header.union(body)

# 3. Refine Edges
# Fillet top edges of the header
main_shape = main_shape.edges(">Z and >Y").fillet(1.5)
# Chamfer body edges for style
main_shape = main_shape.edges(">Z and <Y").chamfer(body_chamfer)
main_shape = main_shape.edges("<Z").chamfer(body_chamfer)

# 4. Features: Holes and Text

# Side mounting holes on the Header
main_shape = (
    main_shape.faces(">X").workplane()
    .center(0, header_length / 2.0)
    .hole(3.2, depth=10)
)
main_shape = (
    main_shape.faces("<X").workplane()
    .center(0, header_length / 2.0)
    .hole(3.2, depth=10)
)

# LED Indicator Hole (Top Face, offset from text)
main_shape = (
    main_shape.faces(">Z").workplane()
    .center(0, 0) # At interface
    .pushPoints([(0, 4.0)]) # Slightly into the header
    .circle(1.0)
    .cutThruAll()
)

# Engraved Text on Header
# Note: Text generation depends on system fonts. Using a generic fallback if needed.
try:
    main_shape = (
        main_shape.faces(">Z").workplane()
        .center(0, header_length / 2.0 + 1.0) # Center on header face
        .text("MC SHOUT HO", fontsize=5.0, distance=-0.6, font="Arial", halign="center", valign="center")
    )
except Exception:
    # Fallback if font issues occur, typically in some CI environments
    pass

# 5. Connector Interface (Bottom/Rear)
# Constructed in parts and unioned to the main body

# Transition block
c_trans = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2.0)
    .center(0, -body_length - conn_trans_l / 2.0)
    .box(conn_trans_w, conn_trans_l, 12.0)
)

# Main connector housing
c_housing = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2.0)
    .center(0, -body_length - conn_trans_l - conn_main_l / 2.0)
    .box(conn_main_w, conn_main_l, 12.0)
)

# Side Ribs on connector
c_ribs = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2.0)
    .center(0, -body_length - conn_trans_l - conn_rib_l / 2.0)
    .box(conn_rib_w, conn_rib_l, 10.0)
)

# PCB Tongue (Protruding element)
c_pcb = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2.0)
    .center(0, -body_length - conn_trans_l - conn_main_l - 2.5)
    .box(18.0, 5.0, 1.6)
)

# Combine connector parts
connector_assembly = c_trans.union(c_housing).union(c_ribs).union(c_pcb)

# Final Union
result = main_shape.union(connector_assembly)

# Export or display
if 'show_object' in globals():
    show_object(result)