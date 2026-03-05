import cadquery as cq

# Parametric dimensions
hex_outer_diameter = 30.0  # Distance across corners
hex_height = 20.0
boss_diameter = 18.0
boss_height = 8.0
hole_diameter = 12.0
hole_offset_x = 2.0  # The hole is visibly off-center relative to the boss
slot_width = 4.0
slot_depth = 1.0

# 1. Create the Hexagonal Base
# Calculate the distance across flats (apothem * 2) if needed, but polygon uses outer radius usually.
# In CadQuery, cq.Workplane().polygon(nSides, diameter) creates a polygon with the specified outer diameter (across corners).
base = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=hex_outer_diameter)
    .extrude(hex_height)
)

# 2. Create the Cylindrical Boss on Top
boss = (
    base.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# 3. Create the Eccentric Hole
# The hole goes through the boss and likely through the base.
# It is offset from the center.
with_hole = (
    boss.faces(">Z")
    .workplane()
    .center(-hole_offset_x, 0)  # Offset the hole to make it eccentric
    .circle(hole_diameter / 2)
    .cutBlind(-(hex_height + boss_height)) # Cut through everything
)

# 4. Create the Vertical Slot on one face
# There is a distinct rectangular groove/slot running vertically on one of the flat faces of the hexagon.
# We need to select one of the side faces.
# Since the hexagon is aligned with polygon(), let's pick a face based on direction (e.g., -Y or -X).
# Let's try to align it with the visible front-left face.
# A standard polygon(6) usually has a point on the X axis or flat on X.
# Let's create a cutter object and subtract it.

# Create a cutter for the slot
# The slot runs along the Z axis on the side of the hex.
# We'll position a rectangle and cut it.
# Calculating the position: Distance to flat is (sqrt(3)/2) * radius.
dist_to_flat = (3**0.5 / 2) * (hex_outer_diameter / 2)

# We select a face to sketch on. Let's sketch on the XY plane and extrude a cutter, then rotate or position it?
# Or sketch directly on the side face.
# Let's sketch on the XY plane and extrude up, positioned to cut the side.
slot_cutter = (
    cq.Workplane("XY")
    .center(0, -dist_to_flat) # Move to the bottom flat face
    .rect(slot_width, slot_depth * 2) # Create rect centered on the edge
    .extrude(hex_height) # Extrude up to the height of the base
)

# Combine the main body with the slot cut
# Note: The image shows the slot on a specific face relative to the eccentric hole.
# The hole is shifted "left" (negative X relative to view), and the slot is on the "front left" face.
# Let's assume standard orientation and just cut the slot on the -Y face for simplicity, 
# as exact orientation dependence isn't fully specified without a drawing.
result = with_hole.cut(slot_cutter)

# 5. Refining the Eccentric Hole orientation relative to the slot
# In the image, looking at the top:
# If the slot is at 6 o'clock (front), the hole is shifted towards 9 o'clock or 10 o'clock.
# My code puts the slot at -Y (6 o'clock) and hole at -X (9 o'clock). This matches visual intuition.

# Export or return result
if __name__ == "__main__":
    # If running in an environment that supports show_object
    try:
        show_object(result)
    except NameError:
        pass