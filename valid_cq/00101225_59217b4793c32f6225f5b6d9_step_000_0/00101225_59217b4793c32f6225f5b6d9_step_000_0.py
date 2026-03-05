import cadquery as cq

# --- Parameters ---
thickness = 6.0
fillet_radius = 3.0
hole_dia_large = 24.0
hole_dia_small = 3.2
slot_size = (20, 8)

# --- Geometry Definition ---
# Define the outer profile of the plate using (x, y) coordinates
# Coordinates are estimated to match the visual proportions
# Origin is roughly centered on the large hole
points = [
    (40, 35),      # Top Right
    (-15, 35),     # Top Left (Main Body)
    (-85, 12),     # Arm Top Tip
    (-85, -5),     # Arm Bottom Tip
    (-35, -5),     # Arm Bottom Corner (Notch start)
    (-25, -35),    # Main Body Bottom Left (Notch end)
    (40, -35)      # Bottom Right
]

# --- Build Base Plate ---
# Create the solid block from the profile and apply fillets to vertical edges
base = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# --- Create Features ---

# 1. Large Circular Hole
# Centered at (0,0) relative to the conceptual origin used for points
result = base.faces(">Z").workplane().moveTo(0, 0).hole(hole_dia_large)

# 2. Rectangular Slots
# Located to the left of the large hole
slot_centers = [
    (-35, 15),   # Top Slot
    (-35, -15)   # Bottom Slot
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(slot_centers)
    .rect(slot_size[0], slot_size[1])
    .cutThruAll()
)

# 3. Small Mounting Holes
# Distribution based on the image features
small_hole_locations = [
    # Far left arm
    (-78, 3.5),
    (-60, 20),
    
    # Near the bottom notch
    (-40, -20),
    
    # Around the slots (Top and Bottom)
    (-35, 30),  # Above top slot
    (-35, -30), # Below bottom slot
    
    # Around the large hole (Motor mount pattern)
    (-15, 20),
    (-15, -20),
    (15, 20),
    (15, -20),
    
    # Right edge corners
    (32, 28),
    (32, -28)
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(small_hole_locations)
    .hole(hole_dia_small)
)