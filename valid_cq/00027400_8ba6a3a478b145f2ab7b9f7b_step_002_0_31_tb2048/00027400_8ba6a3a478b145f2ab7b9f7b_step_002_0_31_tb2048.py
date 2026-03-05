import cadquery as cq
import math

# Parametric dimensions for the interlocking hexagonal tile
circumradius = 50.0
thickness = 6.0
notch_length = 4.0
notch_depth = 2.0
notch_offset = 12.0

# 1. Create the base hexagonal prism
result = cq.Workplane("XY").polygon(6, circumradius * 2).extrude(thickness)

# 2. Add structural chamfers to all main edges for a finished look
result = result.faces(">Z").edges().chamfer(0.5)
result = result.faces("<Z").edges().chamfer(0.5)
result = result.edges("|Z").chamfer(0.5)

# 3. Create the edge notches/interlocking tabs visible on the left-facing edges
# The image shows two small notches on each of the three left-side edges
notch_tool = cq.Workplane("XY").box(notch_depth * 2, notch_length, thickness)

# Calculate the apothem (inradius) to position the notches exactly on the edges
apothem = circumradius * math.cos(math.pi / 6)

# Define angles for the 3 left-facing edges (150, 210, 270 degrees in standard polar)
angles = [150, 210, 270]

for angle in angles:
    rad = math.radians(angle)
    # Midpoint of the edge
    cx = apothem * math.cos(rad)
    cy = apothem * math.sin(rad)
    
    # Calculate offset positions for the two notches along the edge
    dx = notch_offset * math.sin(rad)
    dy = -notch_offset * math.cos(rad)
    
    # Notch 1
    result = result.cut(
        notch_tool.translate((cx + dx, cy + dy, thickness / 2))
                  .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    
    # Notch 2
    result = result.cut(
        notch_tool.translate((cx - dx, cy - dy, thickness / 2))
                  .rotate((0, 0, 0), (0, 0, 1), angle)
    )
