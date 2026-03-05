import cadquery as cq

# Define parameters for the shape
# The shape looks like a stylized, angular 'y' or rune.
# We will define it using a series of 2D points to create a wire, 
# then extrude and chamfer.

thickness = 5.0
chamfer_amount = 0.5

# Define the coordinates for the outline of the shape
# Let's imagine the shape on the XY plane.
# Based on visual estimation of proportions:

# Let's start from the bottom left corner of the "stem"
# Point 1: (0, 0)
pts = [
    (0, 0),         # Bottom left outer
    (10, 5),        # Bottom right of left leg
    (20, 20),       # Inner corner of left leg
    (25, 15),       # Inner corner of right leg
    (35, 25),       # Inner corner under right arm
    (55, 20),       # Bottom right of right arm
    (60, 25),       # Tip of right arm
    (30, 45),       # Top tip of middle peak
    (20, 30),       # Left side of middle peak
    (15, 35),       # Top tip of left arm
    (5, 25),        # Left side of left arm
    (0, 0)          # Closing the loop
]

# Refined coordinates to better match the sharp angular look
# The image shows parallel-ish legs. Let's try to construct it more geometrically.

# Let's try a different set of points to match the specific "rune" look more closely.
# It has a left diagonal leg, a right diagonal leg that branches off.
# Actually, looking at it, it seems like three main segments meeting.
# Left leg going up-left. Right leg going up-right. A bottom leg going down-left?
# No, let's trace the perimeter counter-clockwise starting from the bottom-left-most point.

# Let's assume the bottom-left corner of the main diagonal bar is (0,0).
# The main bar goes up and right.
# There is a vertical-ish branch on the left.
# There is a horizontal-ish branch on the right.

# Let's try sketching relative coordinates.
# Start at bottom left of the left leg.
p0 = (0, 10) 
p1 = (10, 0)   # Bottom tip
p2 = (40, 15)  # Bottom of the main rightward sweep
p3 = (60, 20)  # Far right tip bottom
p4 = (62, 25)  # Far right tip top (slanted)
p5 = (35, 40)  # Top point
p6 = (28, 38)  # Inner corner under the top point
p7 = (32, 28)  # Inner corner
p8 = (20, 20)  # The "crotch" of the Y
p9 = (12, 35)  # Tip of left leg top
p10 = (5, 32)  # Tip of left leg left side
# This is getting complicated to guess. Let's simplify the geometry perception.

# It looks like a shape made of thick lines.
# Let's define the centerlines and thicken them, or just trace the outline directly.
# Let's try direct outline tracing again, creating a "Y" shape with a bent right arm.

outline_pts = [
    (0, 10),    # Leftmost bottom point
    (10, 0),    # Bottom-most point
    (60, 20),   # Rightmost point bottom edge
    (60, 26),   # Rightmost point top edge (flat bit)
    (30, 45),   # Topmost point
    (25, 45),   # Topmost point width
    (22, 25),   # Inner valley right side
    (15, 20),   # Inner valley bottom
    (12, 35),   # Top of left arm
    (5, 35),    # Width of left arm
    (0, 10)     # Back to start
]

# Let's try a cleaner, more parametric approach based on visual segments.
# Segment 1: Bottom-left to Top-right diagonal base
# Segment 2: A vertical-ish prong on the left
# Segment 3: The right end is pointy.

# Re-evaluating coordinates based on image grid estimation if it were there.
# Let's assume bounding box is roughly 60x50.
# The shape is roughly a "U" or "y" rotated.

# Let's define points explicitly.
# 1. Bottom Left Corner of the whole shape: (5, 5)
# 2. Bottom Right Corner (long arm): (55, 25)
# 3. Top Peak: (25, 45)
# 4. Left Arm Top: (10, 35)

points = [
    (5, 15),    # Left arm, bottom-left corner
    (15, 5),    # Bottom point
    (55, 20),   # Right arm, bottom-right corner
    (58, 24),   # Right arm, tip thickness
    (30, 42),   # Top peak, right side
    (26, 42),   # Top peak, left side
    (25, 28),   # Inner crotch, right side
    (18, 22),   # Inner crotch, bottom
    (12, 35),   # Left arm, top-right inner corner
    (8, 35),    # Left arm, top-left outer corner
]
# Closing point is implied by polyline(True)

# Adjusting for a better look:
# The bottom edge is long and straight-ish. From (15,5) to (55,20).
# The right tip is sharp.
# The top peak is sharp.
# The left arm is blunt.

points_final = [
    (10, 20),   # 1. Leftmost bottom
    (20, 10),   # 2. Bottom 'corner'
    (60, 25),   # 3. Far right bottom tip
    (60, 28),   # 4. Far right top tip (short vertical segment)
    (35, 45),   # 5. Top peak tip
    (32, 45),   # 6. Top peak width (very sharp) -> Let's make it a single point? No, has width.
    (30, 28),   # 7. Inner V right side
    (22, 22),   # 8. Inner V bottom
    (18, 35),   # 9. Left arm top inner
    (12, 35),   # 10. Left arm top outer
    # Close to 1
]

# Let's make the right tip sharper
points_final = [
    (8, 20),    # 1. Bottom-left of left leg
    (20, 8),    # 2. Bottom corner (lowest point)
    (65, 25),   # 3. Far right tip
    (40, 42),   # 4. Top peak
    (30, 25),   # 5. Inner corner (crotch)
    (18, 18),   # 6. Inner corner (crotch bottom)
    (15, 32),   # 7. Left leg top inner
    (8, 32)     # 8. Left leg top outer
] 
# This looks like 8 points. 
# Let's trace visually again. 
# 1. Left leg outer face (vertical-ish)
# 2. Bottom face (diagonal up-right)
# 3. Right leg tip (sharp or small flat)
# 4. Top face (diagonal up-left)
# 5. Inner face (diagonal down-left)
# 6. Inner crotch (horizontal-ish)
# 7. Inner left leg face (vertical-ish)
# 8. Top of left leg (horizontal-ish)

# Revised Coordinates strategy:
pts = [
    (5, 15),    # Bottom-left of left leg
    (15, 5),    # Bottom corner
    (55, 20),   # Right tip bottom
    (55, 22),   # Right tip vertical (small flat end)
    (30, 40),   # Top peak
    (28, 25),   # Inner corner right
    (20, 20),   # Inner corner bottom
    (15, 35),   # Left leg inner top
    (5, 35)     # Left leg outer top
]

# Create the sketch and extrude
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Apply chamfer to the top face
# We select the top face, then its edges.
result = (
    result
    .faces(">Z")
    .edges()
    .chamfer(chamfer_amount)
)

# Export or visualization would happen here normally, 
# but "result" is the requested variable.