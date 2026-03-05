import cadquery as cq
import math

# --- Parameters ---
length = 100.0          # Total length of the nameplate
width = 36.0            # Total width of the nameplate
thickness = 5.0         # Thickness of the plate
straight_len = 50.0     # Length of the central rectangular section
fillet_radius = 2.0     # Radius of the edge fillet
text_string = "Tobias"  # Text to display
text_size = 16          # Font size
text_depth = 1.0        # Depth of the text engraving

# --- Geometry Calculation ---
# Coordinates for key points
x_straight = straight_len / 2.0
y_top = width / 2.0
x_tip = length / 2.0

# We calculate a 'tangent' arc that smoothly transitions from the straight top edge
# to the pointed tip. 
# Circle center (xc, yc) is assumed to be at x = x_straight for tangency.
# Passes through (x_straight, y_top) and (x_tip, 0).
dx = x_tip - x_straight
# Solving for yc: (y_top - yc)^2 = dx^2 + yc^2  -> yc = (y_top^2 - dx^2) / (2*y_top)
yc = (y_top**2 - dx**2) / (2 * y_top)
R = y_top - yc

# Calculate a midpoint on this arc for the threePointArc command
x_mid = (x_straight + x_tip) / 2.0
# Circle eq: (x - x_straight)^2 + (y - yc)^2 = R^2
y_mid = yc + math.sqrt(R**2 - (x_mid - x_straight)**2)

# Define symmetric points
pt_arc_TR = (x_mid, y_mid)
pt_arc_BR = (x_mid, -y_mid)
pt_arc_BL = (-x_mid, -y_mid)
pt_arc_TL = (-x_mid, y_mid)

# --- Model Construction ---

# 1. Base Shape
result = (
    cq.Workplane("XY")
    .moveTo(-x_straight, y_top)
    .lineTo(x_straight, y_top)
    .threePointArc(pt_arc_TR, (x_tip, 0))
    .threePointArc(pt_arc_BR, (x_straight, -y_top))
    .lineTo(-x_straight, -y_top)
    .threePointArc(pt_arc_BL, (-x_tip, 0))
    .threePointArc(pt_arc_TL, (-x_straight, y_top))
    .close()
    .extrude(thickness)
)

# 2. Edge Fillet
# Select edges on the top face to create the rounded look
result = result.faces(">Z").edges().fillet(fillet_radius)

# 3. Engraved Text
# Create text on the top face and cut it
result = (
    result.faces(">Z")
    .workplane()
    .text(text_string, text_size, -text_depth, font="Arial", kind="bold")
)