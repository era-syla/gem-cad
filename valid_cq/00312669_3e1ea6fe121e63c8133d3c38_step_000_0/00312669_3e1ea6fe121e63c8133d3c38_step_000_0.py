import cadquery as cq

# Geometric Parameters
num_spikes = 8
radius_tip = 60.0
radius_shoulder = 40.0
radius_neck = 18.0
radius_base = 0.5  # Start slightly away from 0 to ensure valid overlap geometry

width_shoulder = 14.0
width_neck = 5.0
width_base = 1.5   # Width at the base overlap

thickness_center = 8.0
thickness_shoulder = 5.0
thickness_tip = 0.1 # Non-zero to avoid degenerate tip

def make_rhombus_profile(x_offset, width, thickness):
    """
    Creates a rhombus wire in the YZ plane at a specified X offset.
    This defines the cross-section of the spike.
    """
    return (
        cq.Workplane("YZ")
        .workplane(offset=x_offset)
        .polyline([
            (0, thickness / 2.0),
            (width / 2.0, 0),
            (0, -thickness / 2.0),
            (-width / 2.0, 0),
            (0, thickness / 2.0)
        ])
        .close()
    )

# --- Construct a single Arm ---

# Define the profiles for the inner segment (Curved part: Base -> Neck -> Shoulder)
wires_inner = [
    make_rhombus_profile(radius_base, width_base, thickness_center),
    make_rhombus_profile(radius_neck, width_neck, thickness_center * 0.9),
    make_rhombus_profile(radius_shoulder, width_shoulder, thickness_shoulder)
]

# Define the profiles for the outer segment (Straight part: Shoulder -> Tip)
wires_outer = [
    make_rhombus_profile(radius_shoulder, width_shoulder, thickness_shoulder),
    make_rhombus_profile(radius_tip, 0.1, thickness_tip)
]

# Create the solid segments
# Inner segment uses a smooth spline loft for the organic curve
solid_inner = cq.Solid.makeLoft([w.val() for w in wires_inner], ruled=False)

# Outer segment uses a ruled loft for sharp, straight lines to the tip
solid_outer = cq.Solid.makeLoft([w.val() for w in wires_outer], ruled=True)

# Combine segments into a single arm
arm = cq.Workplane(obj=solid_inner).union(cq.Workplane(obj=solid_outer))

# --- Pattern Generation ---

# Create the full star by rotating and unioning the arm
result = arm
for i in range(1, num_spikes):
    angle = i * (360.0 / num_spikes)
    rotated_arm = arm.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_arm)

# Optional: execution hook for CQ-Editor
if 'show_object' in globals():
    show_object(result)