import cadquery as cq

# --- Parameters ---
# Central Ring Dimensions
ring_od = 90.0          # Outer Diameter
ring_id = 80.0          # Inner Diameter
ring_height = 12.0      # Height of the ring
keyway_width = 4.0
keyway_depth = 2.0      # Depth of cut into the inner wall

# Arm Dimensions
num_arms = 4
arm_length_ext = 55.0   # Length extension from ring center (approx)
# Effective tip position = ring_od/2 + arm_length_ext is not quite right if we want fixed length.
# Let's define distance from center of ring to center of mounting hole:
arm_radius = 95.0       
arm_base_width = 28.0   # Width of arm at the ring interface
arm_tip_radius = 5.0    # Radius of the mounting boss
arm_thickness = 5.0     # Thickness of the arms
mounting_hole_dia = 3.2 # Diameter of hole in boss

# Truss / Lightweighting
wall_thickness = 3.0    # Thickness of outer frame and internal ribs
split_ratio = 0.45      # Percentage of arm length where the vertical rib is placed

# --- Geometry Construction ---

# 1. Create the Central Ring
# Cylinder with hole
ring = (cq.Workplane("XY")
        .circle(ring_od / 2.0)
        .circle(ring_id / 2.0)
        .extrude(ring_height)
        )

# Create Keyway
# We create a shape to subtract. 
# Positioned at an angle (e.g., 135 deg) to match the visual style, or aligned.
key_cutter = (cq.Workplane("XY")
              .moveTo(-keyway_width / 2.0, ring_id / 2.0 - 1.0) # Start slightly inside the void
              .lineTo(keyway_width / 2.0, ring_id / 2.0 - 1.0)
              .lineTo(keyway_width / 2.0, ring_id / 2.0 + keyway_depth)
              .lineTo(-keyway_width / 2.0, ring_id / 2.0 + keyway_depth)
              .close()
              .extrude(ring_height)
              .rotate((0,0,0), (0,0,1), 135) # Arbitrary angle like the image
              )

ring = ring.cut(key_cutter)


# 2. Construct a Single Arm
# We build one arm along the +X axis and then pattern it.

# Define key X coordinates
x_start = ring_od / 2.0 - 0.5  # Slight overlap into ring for robust union
x_end = arm_radius             # Center of the tip boss

# Define outer boundary points for the trapezoidal wedge
p_start_top = (x_start, arm_base_width / 2.0)
p_start_bot = (x_start, -arm_base_width / 2.0)
# The arm tapers to meet the boss tangent-ish. 
# We'll taper to the boss diameter width at the tip center.
p_end_top = (x_end, arm_tip_radius)
p_end_bot = (x_end, -arm_tip_radius)

# Create the solid wedge shape
arm_wedge = (cq.Workplane("XY")
             .moveTo(*p_start_top)
             .lineTo(*p_end_top)
             .lineTo(*p_end_bot)
             .lineTo(*p_start_bot)
             .close()
             .extrude(arm_thickness)
             )

# Create the Tip Boss
boss = (cq.Workplane("XY")
        .moveTo(x_end, 0)
        .circle(arm_tip_radius)
        .extrude(arm_thickness)
        )

# Combine wedge and boss
arm_solid = arm_wedge.union(boss)

# Create Mounting Hole
arm_solid = (arm_solid.faces(">Z").workplane()
             .moveTo(x_end, 0)
             .hole(mounting_hole_dia))


# 3. Create Truss Structure (Pockets and Ribs)
# Strategy: Cut a large pocket following the arm profile, then add ribs back in.

# Calculate pocket boundaries (offset inwards by wall_thickness)
# Linear interpolation helper
def get_y_outer(x):
    # Slope calculation
    m = (arm_tip_radius - arm_base_width/2.0) / (x_end - x_start)
    c = arm_base_width/2.0 - m * x_start
    return m * x + c

# Pocket X range
pk_x_start = x_start + wall_thickness
pk_x_end = x_end - arm_tip_radius - wall_thickness

# Define the points for the large cutout
pk_pts = [
    (pk_x_start, get_y_outer(pk_x_start) - wall_thickness), # Top Left
    (pk_x_end, get_y_outer(pk_x_end) - wall_thickness),     # Top Right
    (pk_x_end, -(get_y_outer(pk_x_end) - wall_thickness)),  # Bot Right
    (pk_x_start, -(get_y_outer(pk_x_start) - wall_thickness)) # Bot Left
]

# Perform the Cut
arm_skeleton = arm_solid.faces(">Z").workplane().polyline(pk_pts).close().cutBlind(-arm_thickness)

# Create Ribs
# Location of the vertical cross-rib
x_rib = x_start + (x_end - x_start) * split_ratio

# Vertical Rib (Rectangular bar)
rib_v = (cq.Workplane("XY")
         .center(x_rib, 0)
         .rect(wall_thickness, arm_base_width) # Height is oversized, will be trimmed
         .extrude(arm_thickness))

# Horizontal Rib (from base to vertical rib)
len_rib_h = x_rib - x_start
rib_h = (cq.Workplane("XY")
         .center(x_start + len_rib_h/2.0, 0)
         .rect(len_rib_h, wall_thickness)
         .extrude(arm_thickness))

# Union ribs and trim them to the arm shape
# We use the original wedge as an intersection mask to ensure ribs don't stick out
ribs_raw = rib_v.union(rib_h)
ribs_trimmed = ribs_raw.intersect(arm_wedge)

# Combine skeleton arm with ribs
arm_final = arm_skeleton.union(ribs_trimmed)


# 4. Pattern and Assembly
# Create the full array of arms
arms_structure = arm_final
for i in range(1, num_arms):
    arms_structure = arms_structure.union(arm_final.rotate((0,0,0), (0,0,1), i * 360 / num_arms))

# Combine with Ring
result = ring.union(arms_structure)

# Export or Render
if __name__ == "__main__":
    # If running in CQ-Editor or similar
    try:
        show_object(result)
    except NameError:
        pass