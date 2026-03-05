import cadquery as cq

# --- Geometric Parameters ---
length = 120.0          # Total length of the component
outer_dia = 25.0        # Outer diameter of the main tube
inner_dia = 18.0        # Inner diameter (hollow section)
slot_length = 70.0      # Total length of the central slot
slot_width = 10.0       # Width of the central slot
hole_dia = 6.0          # Diameter of the holes at the ends

# --- Derived Parameters ---
# Calculate center-to-center distance for the outer stadium profile
# The ends are rounded with a radius of outer_dia/2
body_cc_dist = length - outer_dia

# Calculate center-to-center distance for the internal slot
slot_cc_dist = slot_length - slot_width

# Calculate offset for the holes (centered on the end radii)
hole_offset = body_cc_dist / 2.0

# --- Modeling Steps ---

# 1. Create the Base Tube
# Extrude a hollow circle from the YZ plane along the X axis.
# 'both=True' centers the extrusion on the origin.
tube = (
    cq.Workplane("YZ")
    .circle(outer_dia / 2.0)
    .circle(inner_dia / 2.0)
    .extrude(length, both=True)
)

# 2. Shape the Ends (Plan View Profile)
# Create a stadium shape on the XY plane and extrude it vertically (Z).
# Intersecting this with the horizontal tube trims the ends to be rounded
# and creates the characteristic "forked" or "eared" side profile.
shaper_profile = (
    cq.Workplane("XY")
    .slot2D(body_cc_dist, outer_dia)
    .extrude(outer_dia * 2, both=True)
)

result = tube.intersect(shaper_profile)

# 3. Create the Central Slot
# Cut a slot profile through the Z-axis (top and bottom walls).
result = (
    result.faces("+Z")
    .workplane()
    .slot2D(slot_cc_dist, slot_width)
    .cutThruAll()
)

# 4. Drill End Holes
# Create holes through the Z-axis at both ends.
result = (
    result.faces("+Z")
    .workplane()
    .pushPoints([(-hole_offset, 0), (hole_offset, 0)])
    .circle(hole_dia / 2.0)
    .cutThruAll()
)