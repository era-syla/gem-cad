import cadquery as cq

# --- Parametric Dimensions ---
# Main Body
cylinder_dia = 50.0
cylinder_len = 120.0

# End Caps
cap_dia = 56.0
rear_cap_thick = 12.0
front_cap_thick = 12.0

# Piston Rod
rod_dia = 25.0
rod_len = 85.0

# Rear Mount (Base)
base_mount_len = 45.0  # Length from cap face to hole center
base_eye_od = 30.0
base_eye_id = 12.5
base_mount_width = 24.0
base_mount_height = 36.0 # Height at the connection to the cap

# Front Mount (Rod End)
rod_eye_od = 26.0
rod_eye_id = 12.5
rod_eye_width = 24.0

# Port/Valve (Bottom of rear mount)
port_dia = 8.0
port_len = 12.0
port_lip_dia = 10.0
port_lip_thick = 3.0

# --- Construction ---

# 1. Main Cylinder Body (Aligned along X axis)
# Origin (0,0,0) is at the interface between Rear Cap and Main Cylinder
main_body = cq.Workplane("YZ").circle(cylinder_dia / 2.0).extrude(cylinder_len)

# 2. Rear Cap (Extrudes backwards from origin)
rear_cap = cq.Workplane("YZ").circle(cap_dia / 2.0).extrude(-rear_cap_thick)

# 3. Front Cap (Rod Guide)
front_cap = (
    main_body.faces(">X").workplane()
    .circle(cap_dia / 2.0)
    .extrude(front_cap_thick)
    .edges(">X").chamfer(1.0) # Chamfer the front edge
)

# 4. Piston Rod
rod = (
    front_cap.faces(">X").workplane()
    .circle(rod_dia / 2.0)
    .extrude(rod_len)
)

# 5. Rear Mount Assembly
# Center X coordinate of the rear eyelet
rear_eye_x = -rear_cap_thick - base_mount_len

# Rear Eyelet Cylinder (Axis along Y)
rear_eye = (
    cq.Workplane("XZ", origin=(rear_eye_x, 0, 0))
    .circle(base_eye_od / 2.0)
    .extrude(base_mount_width / 2.0, both=True)
)

# Rear Connector (Block connecting Cap to Eyelet)
# Using a polyline profile on XZ plane extruded in Y
connector_pts = [
    (-rear_cap_thick, base_mount_height / 2.0),  # Top at cap
    (-rear_cap_thick, -base_mount_height / 2.0), # Bottom at cap
    (rear_eye_x, -base_eye_od / 2.0),            # Bottom at eye
    (rear_eye_x, base_eye_od / 2.0)              # Top at eye
]

rear_connector = (
    cq.Workplane("XZ")
    .polyline(connector_pts).close()
    .extrude(base_mount_width / 2.0, both=True)
)

# Port on the bottom of the connector
port_x = -rear_cap_thick - (base_mount_len / 2.0)
port_z_start = -10.0 # Approximate start height inside the block
port = (
    cq.Workplane("XY", origin=(port_x, 0, port_z_start))
    .circle(port_dia / 2.0)
    .extrude(-port_len)
)
# Lip/Cap on the port
port_lip = (
    port.faces("<Z").workplane()
    .circle(port_lip_dia / 2.0)
    .extrude(port_lip_thick)
)

# 6. Front Rod End Mount
# Center X coordinate
rod_end_x = cylinder_len + front_cap_thick + rod_len + (rod_eye_od / 2.0) - 2.0

# Rod Eyelet Cylinder (Axis along Y)
rod_eye = (
    cq.Workplane("XZ", origin=(rod_end_x, 0, 0))
    .circle(rod_eye_od / 2.0)
    .extrude(rod_eye_width / 2.0, both=True)
)

# Connector to smooth transition from Rod to Eyelet
rod_connector = (
    cq.Workplane("XZ")
    .moveTo(cylinder_len + front_cap_thick + rod_len - 5.0, rod_dia / 2.0)
    .lineTo(cylinder_len + front_cap_thick + rod_len - 5.0, -rod_dia / 2.0)
    .lineTo(rod_end_x, -rod_eye_od / 2.0)
    .lineTo(rod_end_x, rod_eye_od / 2.0)
    .close()
    .extrude(rod_dia / 1.5, both=True) # Slightly thinner than rod diameter
)

# --- Combine Geometry ---
parts = [
    main_body, rear_cap, front_cap, rod,
    rear_eye, rear_connector, port, port_lip,
    rod_eye, rod_connector
]

result = parts[0]
for part in parts[1:]:
    result = result.union(part)

# --- Cuts (Holes) ---

# Cut Rear Mounting Hole
result = (
    result.cut(
        cq.Workplane("XZ", origin=(rear_eye_x, 0, 0))
        .circle(base_eye_id / 2.0)
        .extrude(base_mount_width, both=True)
    )
)

# Cut Front Mounting Hole
result = (
    result.cut(
        cq.Workplane("XZ", origin=(rod_end_x, 0, 0))
        .circle(rod_eye_id / 2.0)
        .extrude(rod_eye_width, both=True)
    )
)

# --- Finishing Touches ---
# Add fillets to main body junctions for realism
try:
    # Fillet Main Body <-> Rear Cap
    result = result.edges(cq.selectors.NearestToPointSelector((0, cylinder_dia/2.0, 0))).fillet(2.0)
    # Fillet Main Body <-> Front Cap
    result = result.edges(cq.selectors.NearestToPointSelector((cylinder_len, cylinder_dia/2.0, 0))).fillet(2.0)
except Exception:
    pass # Skip fillets if topology makes them fail