import cadquery as cq

# --- Parameters ---
extrusion_height = 450.0
extrusion_width = 20.0
wing_width = 200.0
wing_height = 250.0
wing_thickness = 3.0
disc_radius = 60.0
disc_thickness = 3.0
hub_height = 70.0
arm_length = 250.0
arm_size = 12.0

# --- 1. Vertical Aluminum Extrusion ---
# Create the main body
extrusion_main = cq.Workplane("XY").box(extrusion_width, extrusion_width, extrusion_height, centered=(True, True, False))

# Create T-slots (subtractive cylinders/boxes)
slot_x = cq.Workplane("XY").rect(6.0, extrusion_width).extrude(extrusion_height)
slot_y = cq.Workplane("XY").rect(extrusion_width, 6.0).extrude(extrusion_height)
center_bore = cq.Workplane("XY").circle(2.5).extrude(extrusion_height)

# Apply cuts to create the profile
extrusion = extrusion_main.cut(slot_x).cut(slot_y).cut(center_bore)

# --- 2. Large Wing Plate ---
# Defined on the YZ plane, offset to the side of the extrusion
wing_sketch = (
    cq.Sketch()
    .polygon([
        (0, 50),              # Bottom center (relative to sketch origin)
        (wing_width/2, wing_height),  # Top Right
        (-wing_width/2, wing_height)  # Top Left
    ])
    .vertices().fillet(30.0) # Round the corners
)

wing = (
    cq.Workplane("YZ")
    .workplane(offset=extrusion_width/2 + 2) # Offset to attach to side
    .placeSketch(wing_sketch)
    .extrude(wing_thickness)
)

# --- 3. Circular Base Disc ---
disc = (
    cq.Workplane("XY")
    .workplane(offset=-disc_thickness)
    .circle(disc_radius)
    .extrude(disc_thickness)
)
# Add a cutout to the disc to match the image style (slightly truncated or notched)
disc_cutout = (
    cq.Workplane("XY")
    .workplane(offset=-disc_thickness)
    .rect(disc_radius, disc_radius)
    .extrude(disc_thickness)
    .translate((-disc_radius, -disc_radius, 0))
)
# For the specific image, the disc looks like a full wheel or plate, we'll keep it simple.

# --- 4. Central Hub Assembly ---
# A structural bracket connecting extrusion, arm, and wing.
# Modeled as a hollowed triangular prism block.

hub_outer = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .polygon(3, 80) # Triangle circumradius
    .extrude(hub_height)
    .rotate((0,0,0), (0,0,1), 30) # Orient flat side towards X
)

hub_inner = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .polygon(3, 70)
    .extrude(hub_height)
    .rotate((0,0,0), (0,0,1), 30)
)

# Create the shell
hub = hub_outer.cut(hub_inner)

# Add a central block to clamp the extrusion
hub_core = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .rect(30, 30)
    .extrude(hub_height)
)
hub_core_cut = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .rect(20.5, 20.5)
    .extrude(hub_height)
)
hub_clamp = hub_core.cut(hub_core_cut)
hub = hub.union(hub_clamp)

# Add connecting struts from core to outer triangle
strut = (
    cq.Workplane("XY")
    .workplane(offset=10 + hub_height/2)
    .box(60, 5, hub_height, centered=True)
)
hub = hub.union(strut)
hub = hub.union(strut.rotate((0,0,0), (0,0,1), 120))
hub = hub.union(strut.rotate((0,0,0), (0,0,1), 240))


# --- 5. Horizontal Sensor Arm ---
# A bar extending along the -X axis
arm = (
    cq.Workplane("XY")
    .workplane(offset=35) # Height relative to base
    .box(arm_length, arm_size, arm_size, centered=(False, True, True))
    .translate((-arm_length - 15, 0, 0)) # Move to extend left
)

# Create holes in the arm
hole_spacing = 15.0
holes = cq.Workplane("XY").workplane(offset=35)

for i in range(12):
    # Position holes starting from some offset
    x_pos = -50 - (i * hole_spacing)
    # Cylinder for cutting
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=20)
        .moveTo(x_pos, 0)
        .circle(2.0)
        .extrude(30)
    )
    arm = arm.cut(cutter)

# --- 6. Brackets (Wing to Hub) ---
# Angled plates connecting the wing to the hub structure
bracket_left = (
    cq.Workplane("YZ")
    .workplane(offset=25)
    .moveTo(0, 30)
    .lineTo(30, 80)
    .lineTo(0, 80)
    .close()
    .extrude(5)
)
bracket_right = (
    cq.Workplane("YZ")
    .workplane(offset=-30)
    .moveTo(0, 30)
    .lineTo(30, 80)
    .lineTo(0, 80)
    .close()
    .extrude(5)
)

# --- Final Assembly ---
result = (
    extrusion
    .union(disc)
    .union(wing)
    .union(hub)
    .union(arm)
    .union(bracket_left)
    .union(bracket_right)
)