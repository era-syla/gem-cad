import cadquery as cq

# -- Parametric Dimensions --
# Plate Geometry
leg_length = 120.0      # Length of the straight sides
thickness = 3.0         # Plate thickness

# Connection Tabs (on the hypotenuse)
tab_width = 15.0
tab_protrusion = 3.0    # Distance tabs stick out

# Internal Features
hole_diameter = 4.2     # Screw holes
slot_width = 3.5        # Rectangular slots short dimension
slot_length = 12.0      # Rectangular slots long dimension
feature_spacing = 20.0  # Lateral spacing between slots/holes

# -- Helper Functions --
def get_diag_point(distance):
    """Returns a point on the symmetry axis (y=x) at given distance from origin."""
    val = distance * 0.70710678  # cos(45)
    return (val, val)

def get_offset_point(base_point, offset):
    """Returns a point offset perpendicular to the diagonal, towards the hypotenuse."""
    # Normal to diagonal (1,1) pointing towards Top-Left is (-1,1)
    vec = 0.70710678
    return (base_point[0] - offset * vec, base_point[1] + offset * vec)

# -- Model Construction --

# 1. Base Plate: Right Isosceles Triangle
# Origin (0,0) corresponds to the 90-degree corner
result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (leg_length, 0), (0, leg_length)])
    .close()
    .extrude(thickness)
)

# 2. Add Locking Tabs to Hypotenuse
# Hypotenuse is the edge from (leg_length, 0) to (0, leg_length)
# We position two tabs at 1/3 and 2/3 along this edge.
# The tabs are rectangles rotated -45 degrees to be perpendicular to the edge.

# Define the tab shape (centered, to be translated later)
# We make it double depth (2*protrusion) so it embeds securely into the plate volume
tab_shape = (
    cq.Workplane("XY")
    .rect(tab_width, tab_protrusion * 2)
    .extrude(thickness)
    .rotate((0, 0, 0), (0, 0, 1), -45)
)

# Calculate positions and union tabs
for ratio in [1/3.0, 2/3.0]:
    # Linear interpolation along hypotenuse
    x_pos = leg_length * (1 - ratio)
    y_pos = leg_length * ratio
    
    # Translate tab to position and unite
    result = result.union(tab_shape.translate((x_pos, y_pos, 0)))

# 3. Create Cutouts (Holes and Slots)
# The pattern consists of rows at specific distances from the origin (corner)

# Define feature locations
# Row 1 (Near corner): Single Hole
p1_center = get_diag_point(leg_length * 0.25)

# Row 2 (Middle): Hole on axis, Slot offset to left
p2_center = get_diag_point(leg_length * 0.55)
p2_slot = get_offset_point(p2_center, feature_spacing)

# Row 3 (Far): Slot on axis, Slot offset to left
p3_center = get_diag_point(leg_length * 0.82)
p3_slot = get_offset_point(p3_center, feature_spacing)

# Cut Circular Holes
result = (
    result.faces(">Z").workplane()
    .pushPoints([p1_center, p2_center])
    .hole(hole_diameter)
)

# Cut Rectangular Slots
# Slots are oriented radially (pointing towards hypotenuse), requiring 45 deg rotation
slot_locations = [p2_slot, p3_center, p3_slot]

for loc in slot_locations:
    # We use a loop to handle local rotation for each slot correctly
    result = (
        result.faces(">Z").workplane()
        .center(loc[0], loc[1])       # Move workplane origin to slot center
        .rect(slot_width, slot_length)
        .rotate((0, 0, 0), (0, 0, 1), 45) # Rotate rectangle 45 deg relative to local origin
        .cutBlind(-thickness)         # Cut through
    )