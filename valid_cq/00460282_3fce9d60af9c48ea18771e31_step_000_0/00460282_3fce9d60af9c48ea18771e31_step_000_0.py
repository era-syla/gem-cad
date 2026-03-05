import cadquery as cq

# --- Parameters ---
width = 100.0          # Total width of the frame
height = 80.0          # Total height of the frame
thickness = 5.0        # Thickness of the material (depth)
frame_border = 4.0     # Width of the frame borders and divider
top_opening_h = 18.0   # Height of the top rectangular opening

# --- Calculations ---
# Calculate the width of the inner openings
inner_width = width - (2 * frame_border)

# Calculate the height of the bottom opening
# Total Height = Top Border + Top Opening + Divider + Bottom Opening + Bottom Border
bottom_opening_h = height - (3 * frame_border) - top_opening_h

# Calculate Center Y positions for the cuts relative to the global origin (0,0)
# Top Opening: Start at top edge, move down by border and half the opening height
y_pos_top = (height / 2) - frame_border - (top_opening_h / 2)

# Bottom Opening: Start at bottom edge, move up by border and half the opening height
y_pos_bottom = -(height / 2) + frame_border + (bottom_opening_h / 2)

# --- Geometry Generation ---

# 1. Create the base rectangular block
result = cq.Workplane("XY").box(width, height, thickness)

# 2. Cut the top rectangular opening
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, y_pos_top)
    .rect(inner_width, top_opening_h)
    .cutThruAll()
)

# 3. Cut the bottom rectangular opening
# We select the face again to reset the workplane center for the next operation
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, y_pos_bottom)
    .rect(inner_width, bottom_opening_h)
    .cutThruAll()
)