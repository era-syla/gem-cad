import cadquery as cq

# --- Geometric Parameters ---
shaft_radius = 6.0
shaft_length = 30.0

head_radius = 14.0
head_total_height = 18.0
head_base_height = 6.0  # Height of the solid disk portion

slot_width = 10.0
# Depth of the cuts (lugs height)
lug_height = head_total_height - head_base_height

# Parameter to define the flat face position
# Distance from center to the flat face
flat_offset = 10.0  

hole_diameter = 3.5
hole_countersink_dia = 6.5
hole_spacing = 10.0

# --- Modeling ---

# 1. Create the cylindrical shaft
result = cq.Workplane("XY").circle(shaft_radius).extrude(shaft_length)

# 2. Create the cylindrical head on top of the shaft
# We extrude the full cylinder first, then machine away the features
result = (
    result.faces(">Z").workplane()
    .circle(head_radius)
    .extrude(head_total_height)
)

# 3. Cut the central slot
# We orient the slot along the Y-axis
result = (
    result.faces(">Z").workplane()
    .rect(slot_width, head_radius * 3.0)  # Length > diameter to ensure full cut
    .cutBlind(-lug_height)
)

# 4. Cut the flat face on one side
# We remove the material on the -X side beyond the flat_offset
cut_width = (head_radius - flat_offset) + 5.0  # Width to ensure we clear the edge
cut_center_x = -flat_offset - (cut_width / 2.0)

result = (
    result.faces(">Z").workplane()
    .center(cut_center_x, 0)
    .rect(cut_width, head_radius * 3.0)
    .cutBlind(-lug_height)
)

# 5. Add Countersunk Holes
# Select the flat face (which has normal roughly pointing to -X)
# We center the workplane on the face's center of mass
# We limit the depth to puncture the wall but not hit the opposite lug
wall_thickness = flat_offset - (slot_width / 2.0)
drill_depth = wall_thickness + 2.0 

result = (
    result.faces("<X").workplane(centerOption="CenterOfMass")
    # Local X aligns with Global Y for this face selection
    .pushPoints([(hole_spacing / 2.0, 0), (-hole_spacing / 2.0, 0)])
    .cskHole(hole_diameter, hole_countersink_dia, 82, depth=drill_depth)
)

# 6. Add a small fillet to the bottom of the shaft
result = result.edges("<Z").fillet(0.5)