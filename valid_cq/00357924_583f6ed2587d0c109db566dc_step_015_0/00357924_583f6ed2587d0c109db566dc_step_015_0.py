import cadquery as cq

# --- Dimensions ---
# Main body (middle section)
body_length = 40.0
body_height = 10.0
body_width = 8.0

# Head (front/left section)
head_length = 20.0
head_ext_up = 3.0      # Extension above body height
head_ext_down = 8.0    # Extension below body bottom

# Tail (rear/right section)
tail_length = 35.0
tail_tip_height = 2.0

# --- Profile Construction ---
# Create the 2D profile in the XZ plane.
# Origin (0,0) is at the intersection of the body bottom and the head-body vertical interface.
# X-axis: Positive towards tail, Negative towards head.
# Z-axis: Positive Up.

pts = [
    # Top-Front of Head
    (-head_length, body_height + head_ext_up),
    # Top-Rear of Head (Step)
    (0, body_height + head_ext_up),
    # Step Down
    (0, body_height),
    # Top-Rear of Body (Start of Tail slope)
    (body_length, body_height),
    # Top of Tail Tip
    (body_length + tail_length, tail_tip_height),
    # Bottom of Tail Tip
    (body_length + tail_length, 0),
    # Bottom of Body (Start of Head extension)
    (0, 0),
    # Step Down for Head
    (0, -head_ext_down),
    # Bottom-Front of Head
    (-head_length, -head_ext_down),
    # Close loop at Top-Front
    (-head_length, body_height + head_ext_up)
]

# Create the base solid by extruding the profile
# Centered on Y to facilitate symmetrical features if needed
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(body_width)
    .translate((0, -body_width / 2.0, 0))
)

# --- Features & Cuts ---

# 1. Front Vertical Slot
# A U-shaped channel cut into the front face of the head
slot_width = 3.5
slot_depth = 12.0
# Position a cutter on the front face plane
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=-head_length)  # Move to front face X
    .move(0, (body_height - head_ext_down)/2) # Approximate center vertically
    .rect(slot_width, body_height + head_ext_up + head_ext_down + 5) # Tall rectangle
    .extrude(slot_depth) # Cut inwards (positive extrude from this plane goes +X)
)

# 2. Side Recess on Head
# Detail on the side of the downward extension
recess_depth = 1.0
recess_h = head_ext_down * 0.6
recess_l = head_length * 0.6

result = (
    result.faces(">Y").workplane()
    .moveTo(-head_length / 2.0, -head_ext_down / 2.0)
    .rect(recess_l, recess_h)
    .cutBlind(-recess_depth)
)

# 3. Top Notch at Step
# A small cut where the head steps down to the body
result = (
    result.faces(">Z").workplane(centerOption="ProjectedOrigin")
    .moveTo(0, 0) # At the origin X, which is the step location
    .rect(4.0, body_width + 2.0) # Width+2 ensures clean cut across
    .cutBlind(-2.0)
)