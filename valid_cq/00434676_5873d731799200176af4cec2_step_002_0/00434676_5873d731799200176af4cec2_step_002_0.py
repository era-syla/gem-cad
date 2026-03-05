import cadquery as cq
import math

# --- Parameters ---
# Extrusion Dimensions (2020 Profile)
ex_size = 20.0
ex_slot_w = 6.0
ex_slot_d = 2.0     # Depth of slot opening
ex_cavity_w = 10.0  # Width of inner cavity
ex_cavity_d = 4.0   # Depth of inner cavity (approx)
ex_center_d = 5.0   # Center hole diameter
ex_fillet = 0.5     # Exterior corner fillet

# Assembly Dimensions
vert_len = 280.0
horiz_len = 150.0
mount_height = 40.0 # Height of horizontal beam from motor top
motor_size = 42.3
motor_len = 40.0

# --- Helper Functions ---

def create_profile_sketch():
    """Generates a parametric sketch for a 2020 T-slot aluminum profile."""
    # Base Square with rounded corners
    s = (
        cq.Sketch()
        .rect(ex_size, ex_size)
        .vertices()
        .fillet(ex_fillet)
    )
    
    # Subtract Center Hole
    s = s.circle(ex_center_d / 2, mode='s')
    
    # Subtract T-Slots on all 4 sides
    for i in range(4):
        angle = i * 90.0
        rad = math.radians(angle)
        
        # 1. Slot Opening (at the edge)
        # Distance to edge center
        edge_dist = ex_size / 2
        # Center of the opening rectangle (to ensure it cuts the edge)
        # We place it at (0, edge_dist) then rotate
        # The rect height is 2*slot_d centered at edge_dist to cut cleanly inwards
        
        s = s.push([(edge_dist * math.sin(rad), edge_dist * math.cos(rad))])
        s = s.rect(ex_slot_w, ex_slot_d * 2, mode='s', angle=angle)
        s = s.clean() # Reset stack
        
        # 2. Inner Cavity
        # Calculate center position of the inner cavity
        # It is located inwards from the edge
        # Distance from center = edge_dist - slot_d - (cavity_d / 2)
        cavity_dist = edge_dist - ex_slot_d - (ex_cavity_d / 2)
        
        cx = cavity_dist * math.sin(rad)
        cy = cavity_dist * math.cos(rad)
        
        s = s.push([(cx, cy)])
        s = s.rect(ex_cavity_w, ex_cavity_d, mode='s', angle=angle)
        s = s.clean()
        
    return s

# --- Part Generation ---

# 1. Motor (NEMA 17 Style Base)
motor_body = (
    cq.Workplane("XY")
    .box(motor_size, motor_size, motor_len, centered=(True, True, False))
    .edges("|Z")
    .chamfer(3.0) # Chamfered corners characteristic of stepper motors
)

# Motor Boss (Raised cylinder on top)
motor_boss = (
    motor_body.faces(">Z")
    .workplane()
    .circle(11.0) # 22mm diameter
    .extrude(2.0)
)

# Motor Shaft
motor_shaft = (
    motor_boss.faces(">Z")
    .workplane()
    .circle(2.5) # 5mm diameter
    .extrude(20.0)
)

motor_assy = motor_body.union(motor_boss).union(motor_shaft)


# 2. Vertical Extrusion
# Placed on top of the motor
profile_sketch = create_profile_sketch()

vert_beam = (
    cq.Workplane("XY")
    .placeSketch(profile_sketch)
    .extrude(vert_len)
    .translate((0, 0, motor_len))
)

# 3. Horizontal Extrusion
# Extends to the 'left' (-X direction) from the side of the vertical beam
horiz_beam = (
    cq.Workplane("YZ") # YZ plane orientation puts the profile facing the X axis
    .placeSketch(profile_sketch)
    .extrude(horiz_len)
)

# Orientation and Position adjustment
# Rotate to point in -X direction (currently extrudes +X)
horiz_beam = horiz_beam.rotate((0,0,0), (0,1,0), 180)

# Translate to correct position
# X: Butt against the side of vertical beam (X = -ex_size/2)
# Z: Mounted slightly above the motor base
horiz_beam_x = -(ex_size / 2)
horiz_beam_z = motor_len + mount_height + (ex_size / 2)
horiz_beam = horiz_beam.translate((horiz_beam_x, 0, horiz_beam_z))


# 4. Corner Bracket (Gusset)
# Triangular bracket connecting the horizontal and vertical beams
bracket_size = 20.0
bracket_thick = 18.0 # Fits inside the 20mm profile width

bracket = (
    cq.Workplane("XY")
    .polyline([(0,0), (bracket_size, 0), (0, bracket_size), (0,0)])
    .close()
    .extrude(bracket_thick)
)

# Orient bracket: Triangle in XZ plane, Thickness in Y
# Initial: Triangle in XY, Thickness Z
# Rotate to align with the corner between beams (Legs along -X and +Z)
# Rotate 90 deg around X (stands it up)
bracket = bracket.rotate((0,0,0), (1,0,0), 90)
# Rotate 180 deg around Z (mirrors X and Y)
bracket = bracket.rotate((0,0,0), (0,0,1), 180)

# Position bracket
# Corner at intersection of beams
bracket_x = -(ex_size / 2)
bracket_y = bracket_thick / 2 # Center on Y axis
bracket_z = horiz_beam_z + (ex_size / 2) # Top of horizontal beam

bracket = bracket.translate((bracket_x, bracket_y, bracket_z))


# --- Final Assembly ---

result = motor_assy.union(vert_beam).union(horiz_beam).union(bracket)