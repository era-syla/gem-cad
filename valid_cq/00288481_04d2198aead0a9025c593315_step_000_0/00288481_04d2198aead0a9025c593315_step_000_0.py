import cadquery as cq

# --- Parametric Dimensions ---
length = 130.0        # Total length of the part
width = 32.0          # Max width of the part
height = 25.0         # Height/Thickness
tip_width = 12.0      # Width at the tapered ends
taper_len = 30.0      # Length of the tapered section along X

slot_len = 28.0       # Total length of the oblong slots
slot_dia = 8.0        # Width of the slots
slot_center_dist = 28.0 # Distance from origin to slot center

notch_width = 6.0     # Width of the rectangular cuts
notch_depth = 6.0     # Depth of the cut into the side
notch_pitch = 12.0    # Center-to-center spacing of notches
num_notches = 4       # Number of notches

# --- derived variables ---
hl = length / 2.0
hw = width / 2.0
htw = tip_width / 2.0
straight_hl = hl - taper_len

# --- 1. Base Geometry ---
# Define the profile points clockwise
pts = [
    (straight_hl, hw),    # Top-right taper start
    (hl, htw),            # Right tip top
    (hl, -htw),           # Right tip bottom
    (straight_hl, -hw),   # Bottom-right taper end
    (-straight_hl, -hw),  # Bottom-left taper end
    (-hl, -htw),          # Left tip bottom
    (-hl, htw),           # Left tip top
    (-straight_hl, hw)    # Top-left taper start
]

# Create the main solid block
base = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
)

# --- 2. Slots ---
# Cut the two slots on the top face
with_slots = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(-slot_center_dist, 0), (slot_center_dist, 0)])
    .slot2D(length=slot_len, diameter=slot_dia, angle=0)
    .cutThruAll()
)

# --- 3. Side Notches ---
# Calculate notch positions to center them along the side
notch_group_width = (num_notches - 1) * notch_pitch
start_x = -notch_group_width / 2.0
notch_points = [(start_x + i * notch_pitch, 0) for i in range(num_notches)]

# Create the cutting tool for notches
# We create rectangles on the XY plane and extrude them
# The rects are centered at y=0, then moved to the part edge
notch_cutter = (
    cq.Workplane("XY")
    .pushPoints(notch_points)
    .rect(notch_width, notch_depth * 2) # Double depth to handle centering
    .extrude(height)
    .translate((0, -hw, 0)) # Position at the bottom edge (y = -width/2)
)

# Apply the cut
result = with_slots.cut(notch_cutter)