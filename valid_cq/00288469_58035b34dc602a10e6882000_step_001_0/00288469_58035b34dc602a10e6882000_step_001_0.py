import cadquery as cq

# --- Parametric Dimensions ---
length = 120.0       # Total length of the plate
width = 50.0         # Total width of the plate
thickness = 15.0     # Thickness of the plate

center_hole_dia = 12.0  # Diameter of the central hole

slot_hole_dia = 14.0    # Diameter of the circular part of the end slots
slot_width = 9.0        # Width of the slot opening
slot_offset = 15.0      # Distance from the edge to the center of the slot circle

# --- 3D Modeling ---

# 1. Create the base rectangular block
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Cut the center hole
result = result.faces(">Z").workplane().hole(center_hole_dia)

# 3. Cut the end slots (Keyhole shape)
# Each slot consists of a circular hole and a rectangular channel leading to the edge.

# Coordinates for the circular parts (set inward from the ends)
circle_centers = [
    (length / 2 - slot_offset, 0),
    (-length / 2 + slot_offset, 0)
]

# Coordinates for the channel cuts (centered on the plate edges)
# Positioning the rectangle center on the edge allows a single rect of length (2*offset)
# to span perfectly from the hole center to the outside.
channel_centers = [
    (length / 2, 0),
    (-length / 2, 0)
]

result = (
    result.faces(">Z").workplane()
    # Cut the circular base of the slots
    .pushPoints(circle_centers)
    .hole(slot_hole_dia)
    # Cut the rectangular channels to open the slots
    .pushPoints(channel_centers)
    .rect(slot_offset * 2.0, slot_width)
    .cutThruAll()
)