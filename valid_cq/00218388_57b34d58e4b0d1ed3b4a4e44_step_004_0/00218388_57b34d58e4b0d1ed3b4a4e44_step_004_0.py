import cadquery as cq

# --- Geometric Parameters ---
length_cs = 435.0         # Chainstay length (Pivot to Axle)
width_axle = 148.0        # Rear axle width (Boost standard)
width_pivot = 72.0        # Main pivot width
rad_pivot = 22.0          # Main pivot radius
length_yoke = 60.0        # Length of the front yoke section

# Seatstay Upper Pivot Location (relative to main pivot origin)
ss_piv_x = 110.0
ss_piv_z = 170.0
ss_piv_w = 55.0

# Tube profiles
tube_cs_start = (20, 32)  # Width, Height
tube_cs_end = (16, 24)
tube_ss_start = (14, 14)
tube_ss_end = (16, 20)

# --- Helper Logic ---
# Function to create one side of the swingarm, then mirror it.

# 1. Main Pivot Housing (Front)
# Create a central cylinder housing for bearings
pivot_housing = (
    cq.Workplane("XZ")
    .circle(rad_pivot)
    .extrude(width_pivot / 2 + 5, both=True)
)
pivot_cutout = (
    cq.Workplane("XZ")
    .circle(15)
    .extrude(100, both=True)
)
main_pivot = pivot_housing.cut(pivot_cutout)

# 2. Left Chainstay Assembly
# A. Yoke / Connector Arm
# Loft from the pivot housing side to the start of the tube
yoke_arm = (
    cq.Workplane("YZ")
    .workplane(offset=15) # Start slightly offset from center X
    .moveTo(width_pivot/2, -5)
    .rect(25, 45)         # Beefy connection at pivot
    .workplane(offset=length_yoke - 15)
    .moveTo(width_pivot/2 + 5, -5)
    .rect(*tube_cs_start) # Tube profile start
    .loft()
)

# B. Chainstay Tube
# Loft from Yoke end to Dropout start
chainstay_tube = (
    cq.Workplane("YZ")
    .workplane(offset=length_yoke)
    .moveTo(width_pivot/2 + 5, -5)
    .rect(*tube_cs_start)
    .workplane(offset=length_cs - length_yoke - 40) # Distance to traverse
    .moveTo(width_axle/2 - 10, 0)
    .rect(*tube_cs_end)
    .loft()
)

# 3. Left Dropout
# Create a sketch on the side plane near the rear axle
do_offset = width_axle/2 - 12
dropout_plane = cq.Workplane("XY").workplane(offset=do_offset)

# Define the outer shape of the dropout
pts_dropout = [
    (length_cs, 0),             # Axle center
    (length_cs - 20, -25),      # Bottom hook
    (length_cs - 50, -10),      # CS interface bottom
    (length_cs - 50, 15),       # CS interface top
    (length_cs - 60, 100),      # SS interface bottom
    (length_cs - 45, 120),      # SS interface top
    (length_cs + 15, 20),       # Rear spine top
]

dropout_solid = (
    dropout_plane
    .polyline(pts_dropout).close()
    .extrude(12) # Thickness inwards
)

# Cut axle hole
dropout_solid = (
    dropout_solid
    .faces(">Y").workplane()
    .moveTo(length_cs, 0)
    .circle(6) # 12mm axle hole
    .cutThruAll()
)

# Cut relief pockets (Truss look)
dropout_solid = (
    dropout_solid
    .faces(">Y").workplane()
    .moveTo(length_cs - 30, 45)
    .polygon(3, 20) # Triangle cutout
    .cutThruAll()
)

# 4. Left Seatstay
# Loft from Dropout top to Upper Pivot
ss_tube = (
    cq.Workplane("YZ")
    .workplane(offset=length_cs - 45)
    .moveTo(width_axle/2 - 10, 110) # Approx match dropout top
    .rect(*tube_ss_start)
    .workplane(offset=ss_piv_x - (length_cs - 45)) # Relative offset backwards
    .moveTo(ss_piv_w/2, ss_piv_z)
    .rect(*tube_ss_end)
    .loft()
)

# 5. Upper Pivot Mount
# Eyelet at the top of the seatstay
ss_mount = (
    cq.Workplane("XZ")
    .workplane(offset=-ss_piv_w/2)
    .moveTo(ss_piv_x, ss_piv_z)
    .circle(18)
    .extrude(-15) # Extrude inwards
)
ss_mount_hole = (
    cq.Workplane("XZ")
    .moveTo(ss_piv_x, ss_piv_z)
    .circle(8)
    .extrude(100, both=True)
)
ss_mount = ss_mount.cut(ss_mount_hole)

# --- Assembly ---

# Combine Left Side components
left_assembly = (
    yoke_arm
    .union(chainstay_tube)
    .union(dropout_solid)
    .union(ss_tube)
    .union(ss_mount)
)

# Mirror to create Right Side
right_assembly = left_assembly.mirror("XZ")

# Combine everything
result = (
    left_assembly
    .union(right_assembly)
    .union(main_pivot)
)

# Optional: Add simple fillets to the main junctions for better visual
# Note: Filleting generated lofts can be unstable, so we apply only to the pivot union
try:
    result = result.edges(cq.selectors.NearestToPointSelector((0, width_pivot/2, 0))).fillet(2)
except:
    pass