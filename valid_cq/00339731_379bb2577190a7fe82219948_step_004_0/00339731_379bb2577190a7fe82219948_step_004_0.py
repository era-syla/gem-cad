import cadquery as cq
import math

# Parameter definitions
thickness = 12.0      # Thickness of the arm (Z direction)
width = 18.0          # Width of the arm (Y direction)
length_straight = 35.0 # Length of the straight section
length_angled = 70.0   # Length of the angled section
bend_angle = 30.0     # Angle of the bend in degrees
slot_width = 6.0      # Width of the fork cutout
slot_depth = 15.0     # Depth of the fork cutout

# Helper to convert degrees to radians
rad = math.radians(bend_angle)

# Calculate vertices for the 2D profile on the XY plane
# We define the shape starting from the origin (0,0) which will be the bottom-left of the fork end
# The profile follows the bottom edge, turns, goes to the end, then the top edge, and back

# 1. Start point (Bottom-left of straight section)
p0 = (0, 0)

# 2. Inner corner of the bend (Bottom-right of straight section)
p1 = (length_straight, 0)

# 3. End point of the angled section (Bottom)
#    x = l1 + l2 * cos(theta)
#    y = l2 * sin(theta)
p2_x = length_straight + length_angled * math.cos(rad)
p2_y = length_angled * math.sin(rad)
p2 = (p2_x, p2_y)

# 4. End point of the angled section (Top)
#    Perpendicular offset by 'width' from p2
#    Vector direction: (cos, sin) -> Normal: (-sin, cos)
p3_x = p2_x - width * math.sin(rad)
p3_y = p2_y + width * math.cos(rad)
p3 = (p3_x, p3_y)

# 5. Outer corner of the bend (Top intersection)
#    Intersection of line y = width (top of straight part)
#    and the line representing the top of the angled part.
#    Slope of angled part = tan(theta)
#    Equation of line through p3: y - p3_y = tan(theta) * (x - p3_x)
#    Solve for x where y = width:
#    width - p3_y = tan(theta) * (x - p3_x)
#    x = (width - p3_y) / tan(theta) + p3_x
p4_y = width
p4_x = (width - p3_y) / math.tan(rad) + p3_x
p4 = (p4_x, p4_y)

# 6. Top-left start point
p5 = (0, width)

# List of points for the polyline
pts = [p0, p1, p2, p3, p4, p5]

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
    # Select the face at the start (X=0) to cut the slot
    .faces("<X")
    .workplane()
    # Draw the slot profile. Since we are on the YZ face (local coords),
    # we center the rectangle to cut the middle of the width.
    # Height is set larger than thickness to ensure a clean through-cut in Z.
    .rect(slot_width, thickness * 2.0)
    # Cut blind into the part (negative direction relative to face normal)
    .cutBlind(-slot_depth)
)