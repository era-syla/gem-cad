import cadquery as cq
import math

# --- Dimensions (Parametric) ---
# Base Bracket
bracket_base_width = 40.0
bracket_base_length = 80.0
bracket_base_thickness = 8.0
bracket_tube_od = 30.0
bracket_tube_id = 24.0
bracket_tube_height = 80.0
bracket_hole_spacing = 60.0
bracket_hole_dia = 6.5

# Lever Arm with Spring
lever_arm_length = 80.0
lever_arm_width = 10.0
lever_arm_thickness = 5.0
lever_end_dia = 12.0
lever_end_hole = 6.0
spring_coil_od = 32.0  # Slightly larger than bracket tube to fit over
spring_coil_id = 26.0  # Clearance for bracket tube
spring_length = 35.0
spring_wire_dia = 4.0 # Conceptual wire diameter for the spiral look

# Clevis Pin
clevis_dia = 12.0
clevis_len = 25.0
clevis_slot_width = 5.0
clevis_slot_depth = 12.0
clevis_pin_hole_dia = 3.0

# Small Pin
small_pin_dia = 2.8
small_pin_len = 15.0

# --- Geometry Generation ---

# 1. Base Bracket
def make_bracket():
    # Base plate
    base = (
        cq.Workplane("XY")
        .rect(bracket_base_width, bracket_base_length)
        .extrude(bracket_base_thickness)
        .edges("|Z")
        .fillet(bracket_base_width / 2.0 - 0.1) # Full round ends
    )
    
    # Mounting holes
    base = (
        base.faces(">Z")
        .workplane()
        .pushPoints([(0, bracket_hole_spacing/2), (0, -bracket_hole_spacing/2)])
        .hole(bracket_hole_dia)
    )
    
    # Vertical tube
    tube = (
        cq.Workplane("XY")
        .workplane(offset=bracket_base_thickness)
        .circle(bracket_tube_od / 2)
        .circle(bracket_tube_id / 2)
        .extrude(bracket_tube_height)
    )
    
    # Combine
    return base.union(tube)

# 2. Lever Arm (Spring-like Hub)
def make_lever_arm():
    # Main Hub (Spring coil representation)
    # Instead of a complex helix, we'll model it as a cylinder with grooves
    # to represent the spring coils as seen in the image style.
    hub_outer = (
        cq.Workplane("XY")
        .circle(spring_coil_od / 2)
        .circle(spring_coil_id / 2)
        .extrude(spring_length)
    )
    
    # Add grooves to simulate coils
    groove_depth = 1.5
    num_grooves = 3
    groove_pitch = spring_length / (num_grooves + 1)
    
    for i in range(1, num_grooves + 1):
        z_pos = i * groove_pitch
        groove = (
            cq.Workplane("XY")
            .workplane(offset=z_pos)
            .circle(spring_coil_od / 2 + 0.1) # Cut from outside
            .circle(spring_coil_od / 2 - groove_depth)
            .extrude(1.0) # Groove width
        )
        hub_outer = hub_outer.cut(groove)
        
    # The Arm
    # Tangent to the hub
    arm = (
        cq.Workplane("XY")
        .workplane(offset=spring_length - lever_arm_thickness) # Position at one end
        .moveTo(0, spring_coil_od/2 - 2) # Start slightly embedded
        .rect(lever_arm_thickness, lever_arm_width, centered=False) # Vertical orientation relative to arm direction
        .extrude(lever_arm_length)
        # Rotate to align roughly with image
        .rotate((0,0,0), (0,1,0), -90)
        .translate((lever_arm_thickness, spring_coil_od/2 - 2, spring_length - lever_arm_thickness))
    )
    
    # Re-orienting the arm creation for better control:
    # Let's create the arm shape on the XZ plane and extrude Y
    arm_shape = (
        cq.Workplane("XZ")
        .workplane(offset=spring_coil_od/2 - 1) # Tangent to hub
        .moveTo(0, spring_length - lever_arm_thickness/2)
        .lineTo(-lever_arm_length, spring_length - lever_arm_thickness/2)
        # Add the rounded end
        .lineTo(-lever_arm_length - lever_end_dia/2, spring_length - lever_arm_thickness/2)
        .move(-lever_end_dia/2, 0) # Placeholder logic, better to draw profile
    )

    # Simplified Arm Construction
    arm_geo = (
        cq.Workplane("XY")
        .workplane(offset=spring_length - lever_arm_thickness)
        .center(-spring_coil_od/2, 0) # Start near edge
        .rect(lever_arm_length + spring_coil_od/2, lever_arm_width, centered=False)
        .extrude(lever_arm_thickness)
        .translate((-lever_arm_length, -lever_arm_width/2, 0))
    )
    
    # Clean up hub intersection
    arm_geo = arm_geo.cut(
        cq.Workplane("XY").circle(spring_coil_od/2).extrude(100)
    )
    
    # Add the round eyelet at the end of the arm
    eyelet = (
        cq.Workplane("XY")
        .workplane(offset=spring_length - lever_arm_thickness)
        .center(-lever_arm_length, 0)
        .circle(lever_end_dia / 2)
        .extrude(lever_arm_thickness)
    )
    
    eyelet = eyelet.faces(">Z").workplane().hole(lever_end_hole)
    
    # Small tab on the hub (top right of spring in image)
    tab = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .center(spring_coil_od/2 + 2, 0)
        .rect(6, 6)
        .extrude(lever_arm_thickness)
        .faces(">Z").workplane().hole(3)
    )
    
    final_arm = hub_outer.union(arm_geo).union(eyelet).union(tab)
    return final_arm

# 3. Clevis Pin
def make_clevis():
    pin = (
        cq.Workplane("XY")
        .circle(clevis_dia / 2)
        .extrude(clevis_len)
    )
    
    # Slot
    slot = (
        cq.Workplane("XZ")
        .workplane(offset=-clevis_slot_width/2)
        .moveTo(0, clevis_len)
        .rect(clevis_dia * 2, clevis_slot_depth, centered=False) # Cut downwards
        .extrude(clevis_slot_width)
        .translate((0, -clevis_slot_depth, 0)) # Adjust pos
    )
    
    # Through hole for locking pin
    pin = pin.cut(
        cq.Workplane("YZ")
        .workplane(offset=0)
        .moveTo(0, clevis_len - clevis_slot_depth/2)
        .circle(clevis_pin_hole_dia/2)
        .extrude(clevis_dia + 5, both=True)
    )
    
    # Apply slot cut
    pin = pin.cut(
        cq.Workplane("XZ")
        .workplane(offset=-clevis_slot_width/2)
        .center(0, clevis_len)
        .rect(clevis_dia*1.5, clevis_slot_depth*2) # Oversized rect to ensure cut
        .extrude(clevis_slot_width)
    )
    
    return pin

# 4. Small Locking Pin
def make_small_pin():
    return cq.Workplane("XY").circle(small_pin_dia/2).extrude(small_pin_len)

# --- Assembly / Positioning ---

part_bracket = make_bracket()
part_lever = make_lever_arm()
part_clevis = make_clevis()
part_pin = make_small_pin()

# Move parts to match the exploded view in the image

# Bracket stays at origin
# Lever moves forward and down, rotated
lever_pos = part_lever.rotate((0,0,0), (1,0,0), 90).rotate((0,0,0), (0,0,1), 30).translate((40, -60, 20))

# Clevis moves to the right
clevis_pos = part_clevis.translate((50, 20, 0))

# Pin moves next to clevis
pin_pos = part_pin.translate((40, 20, 5))

# Combine into one result variable for visualization
result = (
    part_bracket
    .union(lever_pos)
    .union(clevis_pos)
    .union(pin_pos)
)