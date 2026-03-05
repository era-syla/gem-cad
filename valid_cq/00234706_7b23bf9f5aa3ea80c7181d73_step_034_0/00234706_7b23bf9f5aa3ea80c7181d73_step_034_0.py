import cadquery as cq

# --- Parameters ---
plate_thickness = 4.0
total_height = 60.0
right_leg_width = 10.0
gap_width = 8.0
left_leg_width = 10.0
ear_width = 14.0
ear_drop_height = 24.0  # Distance from top to bottom of the ear
crotch_height = 25.0    # Length of the cut between legs
leg_length = 35.0       # Approximate length of legs

# Derived Coordinates
# Origin (0,0) is Top-Right corner
x0 = 0
x1 = -right_leg_width
x2 = -(right_leg_width + gap_width)
x3 = -(right_leg_width + gap_width + left_leg_width)
x4 = -(right_leg_width + gap_width + left_leg_width + ear_width)

y_top = 0
y_bottom = -total_height
y_crotch = y_bottom + crotch_height
y_ear_bottom = -ear_drop_height

# --- Main Plate Profile ---
# Define points counter-clockwise starting from top-right
pts = [
    (x0, y_top),
    (x4, y_top),
    (x4, y_ear_bottom),
    (x3, y_ear_bottom),
    (x3, y_bottom),
    (x2, y_bottom),
    (x2, y_crotch),
    (x1, y_crotch),
    (x1, y_bottom),
    (x0, y_bottom)
]

# Create base solid
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(plate_thickness)
)

# --- Fillets ---
# Helper selector for vertical edges at specific XY coordinates
def select_edge(x, y):
    return cq.selectors.NearestToPointSelector((x, y, plate_thickness/2))

# Top Corners
result = result.edges("|Z").edges(select_edge(x0, y_top)).fillet(4.0)
result = result.edges("|Z").edges(select_edge(x4, y_top)).fillet(4.0)

# Ear Bottom Corner
result = result.edges("|Z").edges(select_edge(x4, y_ear_bottom)).fillet(3.0)

# Inner Corners (Crotch and Ear-Leg junction)
result = result.edges("|Z").edges(select_edge(x1, y_crotch)).fillet(2.0)
result = result.edges("|Z").edges(select_edge(x2, y_crotch)).fillet(2.0)
result = result.edges("|Z").edges(select_edge(x3, y_ear_bottom)).fillet(2.0)

# Leg Bottoms (Full Round)
# Use a radius slightly less than half width to avoid geometry errors
leg_radius = right_leg_width / 2.0 - 0.05
result = result.edges("|Z").edges(select_edge(x0, y_bottom)).fillet(leg_radius)
result = result.edges("|Z").edges(select_edge(x1, y_bottom)).fillet(leg_radius)
result = result.edges("|Z").edges(select_edge(x2, y_bottom)).fillet(leg_radius)
result = result.edges("|Z").edges(select_edge(x3, y_bottom)).fillet(leg_radius)

# --- Holes and Slots ---
# 1. Vertical Slot on Right Leg
slot_x = (x0 + x1) / 2
slot_y = (y_crotch + y_bottom) / 2 - 2.0
result = result.faces(">Z").workplane().center(slot_x, slot_y).slot2D(16, 5, 90).cutThruAll()

# 2. Hole above Slot
hole1_y = -10.0
result = result.faces(">Z").workplane().center(slot_x, hole1_y).circle(4.2/2).cutThruAll()

# 3. Hole in middle (Left Leg axis)
hole2_x = (x2 + x3) / 2
hole2_y = -18.0
result = result.faces(">Z").workplane().center(hole2_x, hole2_y).circle(3.5/2).cutThruAll()

# 4. Small hole on Ear
hole3_x = x4 + 3.0
hole3_y = y_ear_bottom + 3.0
result = result.faces(">Z").workplane().center(hole3_x, hole3_y).circle(2.5/2).cutThruAll()

# --- Sensor Block Component ---
# Block located on the back of the ear
sensor_width = 12.0
sensor_height = 16.0
sensor_depth = 14.0
sensor_x = (x3 + x4) / 2
sensor_y = y_top - 10.0

sensor_body = (
    cq.Workplane("XY")
    .workplane(offset=0) # Back face of plate (Z=0)
    .center(sensor_x, sensor_y)
    .rect(sensor_width, sensor_height)
    .extrude(-sensor_depth) # Extrude backwards
)

# Sensor Button (small cylinder on top face)
sensor_button = (
    cq.Workplane("XZ")
    .workplane(offset=sensor_y + sensor_height/2) # Move to top face of sensor
    .center(sensor_x, -sensor_depth/2)
    .circle(1.2)
    .extrude(2.0)
)

# Sensor Side Detail (Connector/Latch)
sensor_detail = (
    cq.Workplane("YZ")
    .workplane(offset=sensor_x - sensor_width/2) # Left face of sensor
    .center(sensor_y, -sensor_depth/2)
    .rect(4, 8)
    .extrude(-1.5) # Extrude outwards to left
)

# Combine all parts
result = result.union(sensor_body).union(sensor_button).union(sensor_detail)