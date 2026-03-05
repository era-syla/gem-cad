import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_length = 80.0
body_width = 40.0
thickness = 2.0

# Tab dimensions
tab_length = 25.0
tab_width = 20.0

# Slot specifications
slot_length = 40.0
slot_width = 7.0
slot_gap = 4.0         # Wall thickness between slots
left_margin = 5.0      # Distance from left edge to start of slot

# Hole specifications
hole_diameter = 4.0

# --- Derived Calculations ---
# Calculate center positions to assemble geometry relative to origin (0,0,0)
# Main body extends from X = -40 to 40
main_body_center_x = 0
main_body_center_y = 0

# Tab is attached to the right side (X = 40)
# Tab center X = (Body Right Edge) + (Half Tab Length)
tab_center_x = (body_length / 2) + (tab_length / 2)

# Slot positioning
# Left edge of body is at X = -body_length/2
# Slot center X = (Left Edge) + (Margin) + (Half Slot Length)
slot_center_x = (-body_length / 2) + left_margin + (slot_length / 2)

# Slot Y pitch (center-to-center distance)
slot_pitch = slot_width + slot_gap

# --- Modeling ---

# 1. Create the Main Rectangular Body
main_body = cq.Workplane("XY").box(body_length, body_width, thickness)

# 2. Create the Tab
tab = cq.Workplane("XY").moveTo(tab_center_x, 0).box(tab_length, tab_width, thickness)

# 3. Combine Main Body and Tab
result = main_body.union(tab)

# 4. Create Slots
# We determine points for the centers of the three slots
# Assuming 3 slots centered vertically: at Y=0, Y=+pitch, Y=-pitch
slot_points = [
    (slot_center_x, 0),
    (slot_center_x, slot_pitch),
    (slot_center_x, -slot_pitch)
]

result = (
    result.faces(">Z")            # Select the top face
    .workplane()                  # Create a workplane on it
    .pushPoints(slot_points)      # Push the 3 center points
    .rect(slot_length, slot_width)# Draw rectangles at points
    .cutThruAll()                 # Cut through the part
)

# 5. Create Hole in Tab
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(tab_center_x, 0)      # Move to center of the tab
    .circle(hole_diameter / 2)    # Draw circle
    .cutThruAll()                 # Cut hole
)