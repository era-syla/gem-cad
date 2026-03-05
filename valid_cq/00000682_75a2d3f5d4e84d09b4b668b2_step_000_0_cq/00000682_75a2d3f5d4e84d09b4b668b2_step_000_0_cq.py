import cadquery as cq
import math

# --- Parameters ---
plate_diameter = 100.0
plate_thickness = 15.0
slot_width = 8.0   # Diameter of the slot ends
slot_length = 15.0 # Center-to-center distance of slot ends (approximate from visual)
pattern_radius = 35.0
num_slots = 6

# --- Logic ---

# 1. Create the base disk
base = cq.Workplane("XY").circle(plate_diameter / 2).extrude(plate_thickness)

# 2. Define the slot shape
# We create a slot sketch on the face of the disk.
# The `slot2D` method takes length and diameter. 
# In CadQuery, length is usually the total length, so we need to calculate:
# total_length = center_to_center + diameter
total_slot_len = slot_length + slot_width

# 3. Create the pattern of slots
# We select the top face, work on it, and create a polar array of points
result = (
    base.faces(">Z")
    .workplane()
    .polarArray(pattern_radius, 0, 360, num_slots)
    .slot2D(total_slot_len, slot_width, angle=90) # Angle=90 orients slots radially/tangentially as needed. Looking at image, they are circumferential.
    .cutThruAll()
)

# Note on Slot Orientation:
# The image shows the slots following the circumference (tangential).
# .slot2D(length, diameter, angle) usually creates a slot along the X axis if angle=0.
# The polarArray context rotates the local coordinate system for each point.
# If angle=0 inside polarArray, slots radiate outwards (spokes).
# If angle=90 inside polarArray, slots follow the circle (tangential).
# The image shows tangential slots.

# Refine orientation calculation just to be sure:
# The `slot2D` inside a `polarArray` context places the slot at the array point.
# By default, without rotation, the slot aligns with the local X. 
# The polar array rotates the local X.
# If we want them tangential, we need them perpendicular to the radius (local X).
# So, `angle=90` makes the slot perpendicular to the radius.

# Let's rebuild carefully to match the specific look.
# The slots in the image are curved? No, usually machined slots are straight slots arranged in a circle.
# Looking closely at the image, they look like straight stadium shapes ("oblongs"), not curved arc slots.
# So `slot2D` is the correct primitive.

# Final check of the generated geometry code construction.
result = (
    cq.Workplane("XY")
    .circle(plate_diameter / 2)
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    .polarArray(pattern_radius, 0, 360, num_slots)
    .slot2D(total_slot_len, slot_width, angle=90) 
    .cutThruAll()
)