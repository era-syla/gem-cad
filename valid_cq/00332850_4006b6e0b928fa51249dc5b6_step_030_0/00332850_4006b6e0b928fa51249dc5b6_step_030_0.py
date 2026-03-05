import cadquery as cq

# --- Parameters ---
thickness = 3.0
width = 45.0
length_right = 110.0
length_left = 90.0
angle_deg = 135.0  # Obtuse angle between the arms
notch_width = 6.0
notch_depth = 3.0
corner_cut_size = 4.0

# --- Base Geometry Generation ---

# Create the Right Arm (aligned with X-axis)
# Uses centered=False to place corner at (0,0)
arm_right = (
    cq.Workplane("XY")
    .rect(length_right, width, centered=False)
    .extrude(thickness)
)

# Create the Left Arm (rotated by the specified angle)
arm_left = (
    cq.Workplane("XY")
    .rect(length_left, width, centered=False)
    .extrude(thickness)
    .rotate((0, 0, 0), (0, 0, 1), angle_deg)
)

# Union the two arms to form the basic L-shape
base_plate = arm_right.union(arm_left)

# --- Feature Definition ---

cutters = []

def add_cutter(u_pos, v_pos, w, h, rotation):
    """
    Creates a cutting volume.
    u_pos: Distance along the arm length
    v_pos: Distance along the arm width (0 for bottom edge, 'width' for top edge)
    w, h: Width and Height of the cutting rectangle
    rotation: Rotation angle of the arm
    """
    c = (
        cq.Workplane("XY")
        .rect(w, h)
        .extrude(thickness * 2)      # Make cutter thicker than plate
        .translate((0, 0, -thickness)) # Center vertically relative to plate
        .translate((u_pos, v_pos))   # Move to local position on the arm
        .rotate((0, 0, 0), (0, 0, 1), rotation) # Rotate to arm orientation
    )
    cutters.append(c)

# -- Right Arm Features (Angle 0) --
# Edge Notches
# Bottom edge notch (approx mid-length)
add_cutter(length_right * 0.6, 0, notch_width, notch_depth * 2, 0)
# Top edge notch (closer to the bend)
add_cutter(width * 1.4, width, notch_width, notch_depth * 2, 0)

# End Corner Steps/Notches
add_cutter(length_right, 0, corner_cut_size * 2, corner_cut_size * 2, 0)
add_cutter(length_right, width, corner_cut_size * 2, corner_cut_size * 2, 0)


# -- Left Arm Features (Angle 135) --
# Edge Notches
# Bottom edge notch
add_cutter(length_left * 0.6, 0, notch_width, notch_depth * 2, angle_deg)
# Top edge notch
add_cutter(width * 1.4, width, notch_width, notch_depth * 2, angle_deg)

# End Corner Steps/Notches
add_cutter(length_left, 0, corner_cut_size * 2, corner_cut_size * 2, angle_deg)
add_cutter(length_left, width, corner_cut_size * 2, corner_cut_size * 2, angle_deg)


# -- Outer Corner Cut --
# Small notch at the main vertex (origin)
origin_cut = (
    cq.Workplane("XY")
    .rect(corner_cut_size * 2, corner_cut_size * 2)
    .extrude(thickness * 2)
    .translate((0, 0, -thickness))
)
cutters.append(origin_cut)

# --- Final Boolean Operations ---

result = base_plate
for cutter in cutters:
    result = result.cut(cutter)