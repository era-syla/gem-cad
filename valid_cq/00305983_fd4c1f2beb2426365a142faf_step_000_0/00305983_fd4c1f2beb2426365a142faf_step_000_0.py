import cadquery as cq

# Dimensions
length_head = 55.0     # Length from shoulder to head
length_foot = 130.0    # Length from shoulder to foot
width_shoulder = 75.0  # Width at the shoulders (widest point)
width_head = 45.0      # Width at the head
width_foot = 35.0      # Width at the foot
height = 45.0          # Height of the coffin
chamfer_size = 6.0     # Size of the top edge chamfer
text_depth = 1.5       # Depth of the text engraving

# Define the points for the 2D profile (Counter-Clockwise)
# Origin (0,0) is at the center of the shoulder line
pts = [
    (width_head / 2.0, length_head),     # Top Right
    (-width_head / 2.0, length_head),    # Top Left
    (-width_shoulder / 2.0, 0.0),        # Shoulder Left
    (-width_foot / 2.0, -length_foot),   # Foot Left
    (width_foot / 2.0, -length_foot),    # Foot Right
    (width_shoulder / 2.0, 0.0)          # Shoulder Right
]

# Create the base solid by extruding the profile
coffin_base = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
)

# Apply chamfer to the top edges
# Select the top face (>Z) and then its edges
result = (
    coffin_base
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

# Cut "R. I. P." text
# Positioned on the top face, shifted towards the head
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, length_head * 0.35)  # Shift center along Y axis towards head
    .text("R. I. P.", fontsize=18, distance=-text_depth, font="Serif", cut=True)
)

# Cut "Jacob Harmon" text
# Positioned just below "R. I. P." near the shoulder line
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, length_head * 0.05)  # Shift center slightly above origin
    .text("Jacob Harmon", fontsize=7, distance=-text_depth, font="Arial", cut=True)
)