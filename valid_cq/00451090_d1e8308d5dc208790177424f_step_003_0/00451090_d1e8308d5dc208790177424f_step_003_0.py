import cadquery as cq

# --- Parameters ---
# Main body dimensions
width_front = 240.0      # Width of the front edge (wide end)
width_back = 180.0       # Width of the back edge (bend line)
main_depth = 120.0       # Depth of the main plate
thickness = 2.0          # Sheet metal thickness

# Flange dimensions
flange_length = 35.0     # Length of the bent flange
flange_angle = 30.0      # Angle of the flange (degrees up from horizontal)

# Slot dimensions
slot_len = 12.0
slot_width = 4.0
slot_margin = 15.0       # Distance from the right edge to slot center

# --- Geometry Construction ---

# 1. Create Main Base Plate
# Modeled as a trapezoid extruded vertically
# Coordinates: Centered on X-axis. Y goes from 0 (back) to depth (front).
p1 = (-width_back/2, 0)
p2 = (width_back/2, 0)
p3 = (width_front/2, main_depth)
p4 = (-width_front/2, main_depth)

base = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3, p4])
    .close()
    .extrude(thickness)
)

# 2. Create Angled Flange
# Calculate taper to determine the width at the tip of the flange
# assuming the taper angle continues from the main body
taper_per_side = (width_front - width_back) / (2 * main_depth)
flange_tip_width = width_back - 2 * (taper_per_side * flange_length)

# Flange profile points in local 2D coordinates
pf1 = (-width_back/2, 0)
pf2 = (width_back/2, 0)
pf3 = (flange_tip_width/2, flange_length)
pf4 = (-flange_tip_width/2, flange_length)

# Rotation calculation: 
# Rotate around X-axis. 180 degrees flips Y to -Y (backwards).
# Subtracting the flange angle tilts it upwards into +Z.
rotation_angle = 180.0 - flange_angle

flange = (
    cq.Workplane("XY")
    .transformed(rotate=(rotation_angle, 0, 0))
    .polyline([pf1, pf2, pf3, pf4])
    .close()
    .extrude(thickness)
)

# 3. Cut Slot in Flange
# Calculate slot position
# Centered along the length of the flange
slot_y_local = flange_length / 2
# Determine width of flange at the slot's Y position to apply margin
current_half_width = (width_back / 2) - (taper_per_side * slot_y_local)
slot_x_local = current_half_width - slot_margin

flange_with_slot = (
    flange
    .faces(">Z") # Select the top face of the flange (local Z)
    .workplane()
    .center(slot_x_local, slot_y_local)
    .slot2D(slot_len, slot_width, angle=90) # Oriented along the flange length
    .cutBlind(-2 * thickness)
)

# 4. Final Boolean Operation
result = base.union(flange_with_slot)

# Optional: Export if running as a script
# cq.exporters.export(result, "tray_model.step")