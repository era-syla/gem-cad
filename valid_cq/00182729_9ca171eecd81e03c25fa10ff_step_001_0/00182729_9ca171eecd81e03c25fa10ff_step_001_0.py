import cadquery as cq

# --- Parameters ---
# Grip dimensions
grip_height = 60.0
grip_base_rx = 18.0
grip_base_ry = 14.0
grip_neck_rx = 12.0
grip_neck_ry = 9.0
grip_rake_x = 12.0  # Offset to slant the grip back

# Platform dimensions
plat_length = 90.0
plat_width = 26.0
plat_thick = 4.0
plat_z = grip_height

# Nose/Front dimensions
nose_len = 35.0
nose_height = 18.0
nose_width = 30.0

# --- 1. Grip Construction ---
# Base profile at Z=0
s_base = cq.Sketch().ellipse(grip_base_rx, grip_base_ry)

# Neck profile at Z=grip_height
# Move neck slightly back (+X) to create ergonomic rake
s_neck = cq.Sketch().rect(grip_neck_rx*2, grip_neck_ry*2).vertices().fillet(4)

grip = (
    cq.Workplane("XY")
    .placeSketch(s_base, s_neck.moved(cq.Location(cq.Vector(grip_rake_x, 0, grip_height))))
    .loft()
)

# Add a fillet to the base of the grip for the flare effect
grip = grip.edges("<Z").fillet(3)

# --- 2. Main Platform Construction ---
# Sits on top of the grip, extends backwards (+X)
# Center the platform roughly over the grip neck
plat_center_x = grip_rake_x + (plat_length / 2.0) - 10.0

platform = (
    cq.Workplane("XY")
    .workplane(offset=plat_z)
    .center(plat_center_x, 0)
    .box(plat_length, plat_width, plat_thick)
)

# --- 3. Front Nose / Housing ---
# Block sticking out the front (-X direction from grip top)
nose_center_x = grip_rake_x - (nose_len / 2.0)
nose_z_base = grip_height

nose = (
    cq.Workplane("XY")
    .workplane(offset=nose_z_base)
    .center(nose_center_x, 0)
    .box(nose_len, nose_width, nose_height, centered=(True, True, False))
)

# Sculpting the nose: Angled cut on the front face
# Create a cutting tool (wedge)
cut_plane = (
    cq.Workplane("XY")
    .workplane(offset=nose_z_base)
    .center(nose_center_x - nose_len/2, 0)
    .transformed(rotate=cq.Vector(0, -30, 0)) # Angle down
    .box(20, 40, 40, centered=(True, True, True))
)
nose = nose.cut(cut_plane)

# Add side chamfers to nose
nose = nose.edges("|X").edges(">Z").chamfer(4)

# --- 4. Top Mechanism (Loop & Boss) ---
# Located on the platform behind the grip
mech_start_x = grip_rake_x + 20.0

# The Loop/Guide
loop_sketch = (
    cq.Sketch()
    .rect(22, 8)
    .rect(18, 4, mode='s') # Subtract inner rect
)

loop = (
    cq.Workplane("XY")
    .workplane(offset=plat_z + plat_thick)
    .center(mech_start_x, 0)
    .placeSketch(loop_sketch)
    .extrude(12)
)

# The Side Boss with Hole
boss_x = mech_start_x + 5.0
boss_y = (plat_width / 2.0) - 1.0 # Align with edge
boss = (
    cq.Workplane("XY")
    .workplane(offset=plat_z + plat_thick)
    .center(boss_x, boss_y)
    .box(12, 6, 10, centered=(True, True, False))
)
# Hole through boss
boss = boss.faces(">Y").workplane().center(0, 5).hole(3.5)

# --- 5. Rear Detail ---
# Fork/Catch at the end of the platform
rear_x = plat_center_x + plat_length/2.0 - 5.0
rear_structure = (
    cq.Workplane("XY")
    .workplane(offset=plat_z + plat_thick)
    .center(rear_x, 0)
    .box(10, plat_width, 6, centered=(True, True, False))
)
# Cut a U-slot in the rear structure
rear_structure = rear_structure.faces(">Z").workplane().rect(12, 12).cutBlind(-10)

# --- 6. Assembly & Refinement ---
# Combine all main bodies
result = grip.union(platform).union(nose).union(loop).union(boss).union(rear_structure)

# Fillet the transition between grip and platform (Neck)
# We select edges near the junction point
try:
    result = result.edges(cq.selectors.BoxSelector(
        (grip_rake_x - 10, -20, grip_height - 5),
        (grip_rake_x + 30, 20, grip_height + 5)
    )).fillet(4)
except Exception:
    pass # Fillet might fail if geometry is complex, skip if so

# Create the pass-through hole visible in the image (top of grip into platform)
result = (
    result.faces(">Z").workplane()
    .center(grip_rake_x, 0)
    .rect(14, 10)
    .cutBlind(-25) # Cut down into the grip
)

# Trigger/Finger groove cutout on the front of the grip
trigger_cut = (
    cq.Workplane("XY")
    .workplane(offset=grip_height - 15)
    .center(grip_rake_x - 10, 0) # Front side
    .box(15, 12, 20) # Box to remove material
)
result = result.cut(trigger_cut)