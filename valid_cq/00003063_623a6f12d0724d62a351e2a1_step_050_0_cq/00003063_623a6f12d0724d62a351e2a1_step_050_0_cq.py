import cadquery as cq

# --- Parametric Variables ---

# Base Plate Dimensions
base_plate_length = 60.0
base_plate_width = 80.0
base_plate_thickness = 4.0

# Vertical Mount Plate Dimensions
vert_plate_height = 50.0
vert_plate_thickness = 5.0
vert_plate_width = base_plate_width

# Gearbox/Housing Dimensions
housing_length = 50.0
housing_width = 60.0
housing_height = 20.0
housing_fillet = 3.0
housing_screw_inset = 4.0
housing_screw_radius = 1.5

# Motor Dimensions (Approximated 370 or similar DC motor)
motor_diameter = 24.4
motor_body_height = 30.8
motor_shaft_boss_dia = 8.0
motor_shaft_boss_height = 2.0
motor_terminal_dia = 1.0
motor_terminal_height = 3.0
motor_terminal_spacing = 7.0  # approximate
motor_back_nub_dia = 4.0
motor_back_nub_height = 1.5

# Offset Motor Position
motor_offset_x = -10.0
motor_offset_y = 10.0

# Output Shaft/Bearing Dimensions
output_boss_dia = 12.0
output_boss_height = 3.0
output_shaft_dia = 6.0
output_shaft_protrusion = 2.0  # Above boss

output_offset_x = 10.0
output_offset_y = -5.0

# Mounting Holes on Vertical Plate
vert_hole_dia = 4.0
vert_hole_spacing = 50.0
vert_hole_height_offset = 20.0  # From bottom

# --- Geometry Construction ---

# 1. Base Structure (L-bracket shape)
# Horizontal Plate
base_plate = (
    cq.Workplane("XY")
    .box(base_plate_length, base_plate_width, base_plate_thickness, centered=(True, True, False))
)

# Vertical Plate attached to the side
vert_plate = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .transformed(offset=(-base_plate_length/2 - vert_plate_thickness/2, 0, vert_plate_height/2))
    .box(vert_plate_thickness, vert_plate_width, vert_plate_height, centered=(True, True, True))
)

# Combine Base
structure = base_plate.union(vert_plate)

# Add mounting holes to vertical plate
structure = (
    structure.faces("<X").workplane()
    .pushPoints([
        (0, vert_hole_height_offset - vert_plate_height/2 + vert_plate_width/2), # Adjusting for coord system
        (0, vert_hole_height_offset - vert_plate_height/2 - vert_plate_width/2)  # This logic depends on exact centering
    ])
    # Let's simplify coordinates relative to the face center
    .center(0, -vert_plate_height/2 + vert_hole_height_offset) # Move to hole height
    .pushPoints([(vert_hole_spacing/2, 0), (-vert_hole_spacing/2, 0)])
    .cboreHole(vert_hole_dia, vert_hole_dia * 1.8, vert_hole_dia) # Countersink/bore look
)

# 2. Main Gearbox Housing
# Created as a stack of rounded rectangles on top of the base plate
housing = (
    cq.Workplane("XY")
    .workplane(offset=base_plate_thickness)
    .box(housing_length, housing_width, housing_height, centered=(True, True, False))
    .edges("|Z").fillet(housing_fillet)
)

# Add split line detail (visual groove)
split_line = (
    cq.Workplane("XY")
    .workplane(offset=base_plate_thickness + housing_height/2)
    .rect(housing_length + 2, housing_width + 2) # Slightly larger to cut through
    .extrude(0.5)
)
# Subtract a tiny sliver or just union for the look? The image shows a seam.
# We will model it as two stacked blocks for a better seam look.
housing_bottom = (
    cq.Workplane("XY")
    .workplane(offset=base_plate_thickness)
    .box(housing_length, housing_width, housing_height/2 - 0.2, centered=(True, True, False))
    .edges("|Z").fillet(housing_fillet)
)
housing_top = (
    cq.Workplane("XY")
    .workplane(offset=base_plate_thickness + housing_height/2)
    .box(housing_length, housing_width, housing_height/2, centered=(True, True, False))
    .edges("|Z").fillet(housing_fillet)
)
housing_assembly = housing_bottom.union(housing_top)

# Housing Screw Holes (Countersunk)
housing_assembly = (
    housing_assembly.faces(">Z").workplane()
    .rect(housing_length - 2*housing_screw_inset, housing_width - 2*housing_screw_inset, forConstruction=True)
    .vertices()
    .cboreHole(2.5, 4.5, 1.5) # Screw dimensions
)

# 3. Motor Model
def create_motor():
    # Main Body
    m_body = cq.Workplane("XY").circle(motor_diameter/2).extrude(motor_body_height)
    m_body = m_body.edges(">Z").fillet(1.0) # Round top edge
    
    # Front Boss (connects to gearbox)
    m_boss = (
        cq.Workplane("XY")
        .workplane(offset=-motor_shaft_boss_height)
        .circle(motor_shaft_boss_dia/2)
        .extrude(motor_shaft_boss_height)
    )
    
    # Back Nub
    m_nub = (
        m_body.faces(">Z").workplane()
        .circle(motor_back_nub_dia/2)
        .extrude(motor_back_nub_height)
    )
    
    # Terminals
    m_terminals = (
        m_body.faces(">Z").workplane()
        .pushPoints([(motor_terminal_spacing/2, 0), (-motor_terminal_spacing/2, 0)])
        .circle(motor_terminal_dia/2)
        .extrude(motor_terminal_height)
    )
    
    return m_body.union(m_boss).union(m_nub).union(m_terminals)

motor = create_motor()

# Position Motor
# Rotate so terminals align roughly as seen
motor = motor.rotate((0,0,0), (0,0,1), 90)
# Move to top of housing
motor_z_pos = base_plate_thickness + housing_height
motor = motor.translate((motor_offset_x, motor_offset_y, motor_z_pos))


# 4. Output Shaft Assembly
output_assy = (
    cq.Workplane("XY")
    .workplane(offset=base_plate_thickness + housing_height)
    .center(output_offset_x, output_offset_y)
    # Bearing Boss
    .circle(output_boss_dia/2)
    .extrude(output_boss_height)
    .faces(">Z").workplane()
    # Shaft
    .circle(output_shaft_dia/2)
    .extrude(output_shaft_protrusion)
    .faces(">Z").workplane()
    # Small depression in center of shaft
    .circle(output_shaft_dia/2 * 0.6)
    .cutBlind(-0.5)
)
# Add a ring/circlip detail on the boss
output_ring = (
     cq.Workplane("XY")
    .workplane(offset=base_plate_thickness + housing_height + output_boss_height)
    .center(output_offset_x, output_offset_y)
    .circle(output_shaft_dia/2 + 1.5)
    .circle(output_shaft_dia/2)
    .extrude(0.5)
)


# --- Combine Final Assembly ---

result = structure.union(housing_assembly).union(motor).union(output_assy).union(output_ring)

# Optional: Add fillets to the base bracket connection for strength/realism
result = result.edges(cq.selectors.BoxSelector(
    (-base_plate_length/2 - vert_plate_thickness, -base_plate_width/2, 0),
    (-base_plate_length/2 + 1, base_plate_width/2, base_plate_thickness+1)
)).fillet(1.0)