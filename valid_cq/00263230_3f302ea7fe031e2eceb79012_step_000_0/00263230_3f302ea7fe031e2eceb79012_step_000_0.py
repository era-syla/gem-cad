import cadquery as cq

# --- Parameters ---
height_total = 125.0
thickness = 6.0

# Shaft Dimensions
width_bottom = 10.0
width_neck = 12.0
height_neck = 85.0
width_top_flare = 22.0
height_top_body = 115.0

# Bottom Hub & Pin
radius_hub = 7.0
radius_pin = 4.0
pin_length = 6.0

# Top Plate
plate_width = 24.0
plate_height = 5.0
plate_depth = 8.0

# Slot
slot_width = 3.0
slot_length = 25.0
slot_top_margin = 4.0

# Side Boss
boss_radius = 3.0
boss_y = 102.0
boss_x = 9.0  # Approximate X position on the flare

# Text
text_string = "st.louis-inst.org"
text_size = 5.5

# --- Geometry Construction ---

# 1. Main Arm Profile (Shaft + Flare)
# Define the path on XY plane
def create_arm_profile():
    # Helper for curve control point (concave flare)
    p1 = (width_neck / 2.0, height_neck)
    p2 = (width_top_flare / 2.0, height_top_body)
    mid_x, mid_y = (p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0
    # Control point slightly inward for concave shape
    c_x, c_y = mid_x * 0.7, mid_y 
    
    return (
        cq.Workplane("XY")
        .moveTo(width_bottom / 2.0, 0)
        .lineTo(p1[0], p1[1])
        .threePointArc((c_x, c_y), p2)          # Flare out
        .lineTo(-p2[0], p2[1])                  # Top edge
        .threePointArc((-c_x, c_y), (-p1[0], p1[1])) # Flare in
        .lineTo(-width_bottom / 2.0, 0)
        .close()
    )

arm = create_arm_profile().extrude(thickness)

# 2. Bottom Hub (Rounded End)
hub = (
    cq.Workplane("XY")
    .circle(radius_hub)
    .extrude(thickness)
)

main_body = arm.union(hub)

# 3. Top T-Plate
# Centered on top of the arm body
top_plate = (
    cq.Workplane("XY")
    .moveTo(0, height_top_body + plate_height / 2.0)
    .rect(plate_width, plate_height)
    .extrude(plate_depth)
    # Center the plate relative to the arm thickness
    .translate((0, 0, (thickness - plate_depth) / 2.0))
)

main_body = main_body.union(top_plate)

# 4. Slot Cut
# Cut through the upper section
slot_y_center = height_top_body - slot_top_margin - slot_length / 2.0
main_body = (
    main_body.faces(">Z").workplane()
    .moveTo(0, slot_y_center)
    .rect(slot_width, slot_length)
    .cutThruAll()
)

# 5. Side Boss
# Small cylinder on the side edge
side_boss = (
    cq.Workplane("XY")
    .moveTo(boss_x, boss_y)
    .circle(boss_radius)
    .extrude(thickness)
)
main_body = main_body.union(side_boss)

# 6. Bottom Pin
# Cylinder protruding from the front face
pin = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .moveTo(0, 0)
    .circle(radius_pin)
    .extrude(pin_length)
)
main_body = main_body.union(pin)

# 7. Embossed Text
# Vertical text along the shaft
text_pos_y = 55.0
text_obj = (
    cq.Workplane("XY")
    .text(text_string, text_size, 0.6) # 0.6mm emboss height
    .rotate((0, 0, 0), (0, 0, 1), -90) # Rotate text to run vertically
    .translate((0, text_pos_y, thickness))
)

result = main_body.union(text_obj)