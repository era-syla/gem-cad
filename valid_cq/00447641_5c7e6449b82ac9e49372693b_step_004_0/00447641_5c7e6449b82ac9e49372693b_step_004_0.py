import cadquery as cq

# -- Parametric Dimensions --
length = 140.0
width = 25.0
thickness = 3.0

# Groove dimensions
groove_width = 2.5
groove_depth = 1.0
groove_margin = 15.0  # Distance from ends to start of groove

# Side notch dimensions (on long edges)
side_notch_width = 6.0
side_notch_depth = 2.0

# End notch dimensions (on short edges)
end_notch_width = 8.0
end_notch_depth = 3.0

# -- Model Construction --

# 1. Base Plate
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Side Notches
# We sketch rectangles centered on the midpoints of the long edges
# The rectangle height is 2*depth to ensure it cuts inward by 'depth'
result = result.faces(">Z").workplane().pushPoints([
    (0, width / 2), 
    (0, -width / 2)
]).rect(side_notch_width, side_notch_depth * 2).cutThruAll()

# 3. End Notches
# We sketch rectangles centered on the midpoints of the short edges
# The rectangle width is 2*depth to ensure it cuts inward by 'depth'
result = result.faces(">Z").workplane().pushPoints([
    (length / 2, 0), 
    (-length / 2, 0)
]).rect(end_notch_depth * 2, end_notch_width).cutThruAll()

# 4. Central Groove
# A blind cut along the center of the top face
groove_length = length - (2 * groove_margin)
result = result.faces(">Z").workplane().rect(groove_length, groove_width).cutBlind(-groove_depth)