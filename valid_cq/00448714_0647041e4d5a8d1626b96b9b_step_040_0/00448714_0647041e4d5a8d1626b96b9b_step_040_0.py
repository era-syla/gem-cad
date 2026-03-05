import cadquery as cq

# --- Dimensions & Parameters ---
# Overall dimensions
tube_od = 25.0       # Main body diameter
tube_len = 250.0     # Length of the cylinder tube
bore_dia = 25.0      # Nominal bore (used for sizing hex/caps)

# Rear End Cap (Clevis Mount)
rear_clevis_len = 25.0
rear_clevis_width = 12.0 # Thickness of the flat tang
rear_pin_dia = 10.0
rear_fillet_rad = 5.0
cap_hex_af = 32.0    # Hex across flats
cap_hex_height = 10.0
collar_height = 6.0
collar_od = 27.0     # Collar diameter (slightly larger than tube)

# Front End Cap
nose_dia = 20.0      # Threaded nose diameter
nose_len = 25.0
nose_nut_thk = 8.0
nose_nut_af = 30.0   # Nose mounting nut size

# Piston Rod
rod_dia = 12.0
rod_stickout = 50.0  # Length visible (extension)
rod_thread_dia = 10.0
rod_thread_len = 15.0
rod_nut_thk = 6.0
rod_nut_af = 17.0

# Ports
port_dia = 3.0       # Pneumatic port diameter

# --- Geometry Construction ---

# 1. Rear End Cap Assembly
# Start with the clevis block (cylinder flattened on sides)
# Base cylinder
rear_clevis = (
    cq.Workplane("XY")
    .circle(collar_od / 2)
    .extrude(rear_clevis_len)
)

# Cut the sides to create the flat tang
cut_width = (collar_od * 2) # Large enough to clear
cut_offset = (rear_clevis_width / 2) + (cut_width / 2)

cutter = (
    cq.Workplane("XY")
    .rect(cut_width, cut_width)
    .extrude(rear_clevis_len)
)

rear_clevis = (
    rear_clevis
    .cut(cutter.translate((cut_offset, 0, 0)))
    .cut(cutter.translate((-cut_offset, 0, 0)))
)

# Round the bottom of the tang (fillet edges along Y at Z=0)
# Since selecting edges can be tricky, we'll assume the basic shape is fine or apply fillets carefully.
# We will fillet the vertical edges of the resulting flat block.
rear_clevis = rear_clevis.edges("|Z").fillet(2.0)

# Drill the pivot pin hole
rear_clevis = (
    rear_clevis.faces(">Y").workplane()
    .center(0, -rear_clevis_len/2 + 8) # Position hole 8mm from bottom
    .circle(rear_pin_dia / 2)
    .cutThruAll()
)

# Hexagonal Section
current_z = rear_clevis_len
rear_hex = (
    cq.Workplane("XY")
    .workplane(offset=current_z)
    .polygon(6, cap_hex_af)
    .extrude(cap_hex_height)
)

# Collar (Transition to tube)
current_z += cap_hex_height
rear_collar = (
    cq.Workplane("XY")
    .workplane(offset=current_z)
    .circle(collar_od / 2)
    .extrude(collar_height)
)

# Rear Port Hole on the collar
rear_port = (
    cq.Workplane("XZ")
    .workplane(offset=-collar_od/2) # On the surface
    .center(current_z + collar_height/2, 0)
    .circle(port_dia/2)
    .extrude(-collar_od/2) # Cut inwards
)

rear_assy = rear_clevis.union(rear_hex).union(rear_collar).cut(rear_port)

# 2. Cylinder Tube
current_z += collar_height
tube = (
    cq.Workplane("XY")
    .workplane(offset=current_z)
    .circle(tube_od / 2)
    .extrude(tube_len)
)

# 3. Front End Cap Assembly
current_z += tube_len

# Front Collar
front_collar = (
    cq.Workplane("XY")
    .workplane(offset=current_z)
    .circle(collar_od / 2)
    .extrude(collar_height)
)

# Front Port Hole
front_port = (
    cq.Workplane("XZ")
    .workplane(offset=-collar_od/2)
    .center(current_z + collar_height/2, 0)
    .circle(port_dia/2)
    .extrude(-collar_od/2)
)

# Front Hex
current_z += collar_height
front_hex = (
    cq.Workplane("XY")
    .workplane(offset=current_z)
    .polygon(6, cap_hex_af)
    .extrude(cap_hex_height)
)

# Threaded Nose
current_z += cap_hex_height
front_nose = (
    cq.Workplane("XY")
    .workplane(offset=current_z)
    .circle(nose_dia / 2)
    .extrude(nose_len)
    .faces(">Z").chamfer(1.0)
)

# Mounting Nut on Nose
nose_nut = (
    cq.Workplane("XY")
    .workplane(offset=current_z + 3) # Slightly offset from hex face
    .polygon(6, nose_nut_af)
    .extrude(nose_nut_thk)
    .cut(cq.Workplane("XY").workplane(offset=current_z).circle(nose_dia/2).extrude(nose_len + 10))
)

front_assy = front_collar.union(front_hex).union(front_nose).union(nose_nut).cut(front_port)

# 4. Piston Rod Assembly
# Rod starts from the face of the front hex (inside the nose)
rod_start_z = current_z 
rod_len = nose_len + rod_stickout

rod_main = (
    cq.Workplane("XY")
    .workplane(offset=rod_start_z)
    .circle(rod_dia / 2)
    .extrude(rod_len)
)

# Rod Threaded Tip
tip_z = rod_start_z + rod_len
rod_tip = (
    cq.Workplane("XY")
    .workplane(offset=tip_z)
    .circle(rod_thread_dia / 2)
    .extrude(rod_thread_len)
)

# Rod Nut
rod_nut = (
    cq.Workplane("XY")
    .workplane(offset=tip_z + 4) # Positioned on the thread
    .polygon(6, rod_nut_af)
    .extrude(rod_nut_thk)
    .cut(cq.Workplane("XY").workplane(offset=tip_z).circle(rod_thread_dia/2).extrude(rod_thread_len + 5))
)

rod_assy = rod_main.union(rod_tip).union(rod_nut)

# --- Combine All Parts ---
result = rear_assy.union(tube).union(front_assy).union(rod_assy)