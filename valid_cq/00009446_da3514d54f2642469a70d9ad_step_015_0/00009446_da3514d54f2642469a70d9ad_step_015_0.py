import cadquery as cq
import math

# --- Parameters ---
# Dimensions for the robotic limb and components
hip_size = (40, 35, 20)
thigh_length = 50
shin_length = 60
joint_radius = 8
limb_taper_start = 9
limb_taper_mid = 6
limb_taper_end = 3

# --- 1. Modeling the Floating Components (Left side of image) ---
def create_cover_shell():
    """Creates the small shell-like components visible on the left."""
    # Create a base capsule-like shape
    part = (
        cq.Workplane("XY")
        .box(15, 8, 6)
        .edges("|Z").fillet(3.9)  # Round the ends
        .edges(">Z").fillet(2.9)  # Round the top
    )
    
    # Add a small mounting detail
    mount = (
        cq.Workplane("XY")
        .circle(1.5)
        .extrude(7)
        .translate((4, 0, 0))
    )
    
    return part.union(mount)

# Create two stacked instances
cover_top = create_cover_shell().translate((-50, 0, 10))
cover_bottom = create_cover_shell().translate((-50, 0, -2))


# --- 2. Modeling the Main Body / Hip Joint ---
# Central hub structure
hip_main = (
    cq.Workplane("XY")
    .rect(hip_size[0], hip_size[1])
    .extrude(hip_size[2])
    .edges("|Z").fillet(5)
    .edges(">Z").fillet(3)
    .edges("<Z").fillet(3)
)

# Cutout detail to make it look mechanical
cutout = (
    cq.Workplane("XY")
    .rect(hip_size[0] * 0.6, hip_size[1] * 0.6)
    .extrude(5)
    .translate((0, 0, hip_size[2]/2))
)
hip_main = hip_main.cut(cutout)

# Side joint block where the leg attaches
joint_block = (
    cq.Workplane("YZ")
    .workplane(offset=hip_size[0]/2 - 5)
    .circle(joint_radius * 1.2)
    .extrude(15)
)

# Combine hip parts
hip_assembly = hip_main.union(joint_block)


# --- 3. Modeling the Limb Segments ---

# Starting position for the thigh (end of the hip joint)
start_x = hip_size[0]/2 + 10

# Thigh (Upper Limb)
# Loft from a larger circle to a smaller one to create organic taper
thigh = (
    cq.Workplane("YZ")
    .workplane(offset=start_x)
    .circle(limb_taper_start)
    .workplane(offset=thigh_length)
    .circle(limb_taper_mid)
    .loft()
)

# Knee Joint (Sphere)
knee_center_x = start_x + thigh_length
knee = (
    cq.Workplane("XY")
    .sphere(limb_taper_mid * 1.1)
    .translate((knee_center_x, 0, 0))
)

# Shin (Lower Limb)
# Constructed along X first, then rotated to simulate a slight bend
shin_angle = -15  # Degrees downwards
shin_raw = (
    cq.Workplane("YZ")
    .circle(limb_taper_mid)
    .workplane(offset=shin_length)
    .circle(limb_taper_end)
    .loft()
)

# Rotate shin and move to knee position
shin = shin_raw.rotate((0,0,0), (0,1,0), shin_angle).translate((knee_center_x, 0, 0))

# Foot / End Effector
# Calculate position of the tip based on rotation
tip_x = knee_center_x + shin_length * math.cos(math.radians(shin_angle))
tip_z = shin_length * math.sin(math.radians(shin_angle))

foot = (
    cq.Workplane("XY")
    .sphere(limb_taper_end * 1.2)
    .translate((tip_x, 0, tip_z))
)


# --- 4. Final Assembly ---
# Union all connected parts into the main limb
robotic_limb = hip_assembly.union(thigh).union(knee).union(shin).union(foot)

# Combine with the floating parts
result = robotic_limb.union(cover_top).union(cover_bottom)