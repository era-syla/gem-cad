import cadquery as cq

# --- Parameters ---
# Main Dimensions
col_size = 40.0
col_height = 160.0
base_thick = 12.0
base_leg_len = 140.0
base_leg_width = 80.0

# --- 1. Vertical Column Assembly ---
# The main vertical square tube
column_tube = (
    cq.Workplane("XY")
    .rect(col_size, col_size)
    .extrude(col_height)
    .faces(">Z").workplane()
    .hole(col_size - 6, depth=col_height) # Hollow core
)

# Slots on the column faces
slot_length = 80.0
slot_width = 8.0
for face in [">X", "<X", ">Y", "<Y"]:
    column_tube = (
        column_tube.faces(face).workplane()
        .slot2D(slot_length, slot_width)
        .cutThruAll()
    )

# Top Cap
cap_size = col_size + 4
cap_thick = 10.0
top_cap = (
    cq.Workplane("XY")
    .box(cap_size, cap_size, cap_thick)
    .translate((0, 0, col_height + cap_thick/2))
)
# Top Cap Features (Central bore and mounting holes)
top_cap = (
    top_cap.faces(">Z").workplane()
    .hole(18.0) # Central hole
    .rect(cap_size - 10, cap_size - 10, centered=True)
    .vertices()
    .hole(4.0) # Corner mounting holes
)

column_assembly = column_tube.union(top_cap)

# --- 2. Base Structure ---
# L-shaped base plate
# We construct it using a sketch to get the corner shape
base_sketch = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_leg_len, 0)
    .lineTo(base_leg_len, base_leg_width)
    .lineTo(base_leg_width, base_leg_width) # Inner corner start
    .lineTo(base_leg_width, base_leg_len)
    .lineTo(0, base_leg_len)
    .close()
    .extrude(-base_thick)
)

# Add some fillets and chamfers to the base for realism
base_structure = base_sketch.edges("|Z").fillet(5.0)

# Add mounting slots to the base legs
base_structure = (
    base_structure.faces(">Z").workplane()
    # Slot on X leg
    .moveTo(base_leg_len * 0.7, base_leg_width / 2)
    .slot2D(40, 10).cutThruAll()
    # Slot on Y leg
    .moveTo(base_leg_width / 2, base_leg_len * 0.7)
    .rect(10, 40).cutThruAll()
)

# Position Column on Base (At the corner)
# The column center should be at (base_leg_width/2, base_leg_width/2) roughly
col_pos_x = base_leg_width / 2
col_pos_y = base_leg_width / 2
column_assembly = column_assembly.translate((col_pos_x, col_pos_y, 0))

# --- 3. Pivot Mechanism (Side Assembly) ---
# Cheek plates holding the lever
cheek_thick = 6.0
cheek_w = 70.0
cheek_h = 70.0

# Define the shape of the side plate
pts = [(0, 0), (cheek_w, 0), (cheek_w * 0.6, cheek_h), (0, cheek_h)]
cheek_plate = (
    cq.Workplane("XZ")
    .polyline(pts).close()
    .extrude(cheek_thick)
    .edges("|Y").fillet(3.0)
)

# Add pivot hole and adjustment slot
cheek_plate = (
    cheek_plate.faces(">Y").workplane(centerOption="CenterOfMass")
    .moveTo(5, 10).hole(12.0) # Main pivot
    .moveTo(-10, -15).slot2D(15, 6, 45).cutThruAll() # Angled slot
)

# Create two plates and a spacer/mount
plate_spacing = 30.0
left_cheek = cheek_plate.translate((0, -cheek_thick, 0))
right_cheek = cheek_plate.translate((0, plate_spacing, 0))

# Lever Arm
arm_len = 120.0
arm_w = 25.0
arm_thk = 10.0
lever_arm = (
    cq.Workplane("XY")
    .box(arm_len, arm_thk, arm_w)
    .edges("|Y").fillet(2.0)
    .rotate((0,0,0), (0,1,0), -35) # Tilt
    .translate((30, plate_spacing/2, 40)) # Position between plates
)
# Add hole to lever arm end
lever_arm = (
    lever_arm.faces(">Y").workplane()
    .moveTo(arm_len/2 - 10, 0).hole(8.0)
)

pivot_assy = left_cheek.union(right_cheek).union(lever_arm)

# Mount the pivot assembly to the X-leg of the base
pivot_assy = pivot_assy.translate((base_leg_len - 60, 5, base_thick)) 
# Adjust Z to sit on top of base (base is extruded -Z, so top is Z=0)
pivot_assy = pivot_assy.translate((0, 0, 0)) 


# --- 4. Detached Rod Assembly (Floating) ---
rod_diam = 10.0
rod_len = 180.0
rod_cyl = cq.Workplane("YZ").circle(rod_diam/2).extrude(rod_len)

# L-Brackets for rod
brkt_w = 30.0
brkt_h = 30.0
brkt_thk = 4.0

l_bracket = (
    cq.Workplane("XY")
    .rect(brkt_w, brkt_thk).extrude(brkt_h) # Vertical wall
    .faces("<Z").workplane().rect(brkt_w, 20).extrude(brkt_thk) # Base flange
)
# Add holes to bracket
l_bracket = (
    l_bracket
    .faces(">Y").workplane(centerOption="CenterOfMass").translate((0, 5)).hole(rod_diam) # Rod hole
    .faces("<Z").workplane(centerOption="CenterOfMass").hole(5.0) # Mounting hole
)

# Assemble Rod
b1 = l_bracket.rotate((0,0,0),(0,0,1), 90).translate((0, brkt_thk/2, 0))
b2 = l_bracket.rotate((0,0,0),(0,0,1), 90).translate((0, rod_len - brkt_thk/2, 0))

rod_assembly = rod_cyl.union(b1).union(b2)

# Position the rod assembly floating to the left
rod_assembly = (
    rod_assembly
    .rotate((0,0,0), (0,0,1), -20)
    .rotate((0,0,0), (1,0,0), 90) # Lay flat? No, image shows it horizontal
    .rotate((0,0,0), (0,1,0), 90) # Align with Y axis roughly
    .translate((-100, 50, 40))
)

# --- Final Assembly ---
result = (
    base_structure
    .union(column_assembly)
    .union(pivot_assy)
    .union(rod_assembly)
)