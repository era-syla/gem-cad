import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
part_length = 60.0    # Total length from end to end
part_width = 30.0     # Width of the rectangular ends
part_height = 20.0    # Thickness of the part

# Central cylindrical feature
center_radius = 20.0  # Radius of the outer central bulge

# Cutout dimensions
slot_length = 40.0    # Length of the rectangular part of the slot
slot_width = 10.0     # Width of the rectangular part of the slot
hole_radius = 10.0    # Radius of the central circular hole

# --- Modeling Process ---

# 1. Create the base shape
# We start with a sketch on the XY plane.
# The shape consists of a central circle and a rectangle centered on it.
# We will construct the outer profile first.

# Create the main body
# - A central cylinder
# - Two rectangular blocks on sides
# - Combine them (union)

# Step 1: Create the central cylinder
cylinder = cq.Workplane("XY").circle(center_radius).extrude(part_height)

# Step 2: Create the rectangular box
# The box length corresponds to the total part length.
# The box width corresponds to the width of the wings.
box = cq.Workplane("XY").rect(part_length, part_width).extrude(part_height)

# Step 3: Combine cylinder and box to get the outer profile
base_body = cylinder.union(box)

# 2. Create the cutouts
# The cutout consists of a central hole and a rectangular slot.

# Step 4: Create the central hole
center_hole = cq.Workplane("XY").circle(hole_radius).extrude(part_height)

# Step 5: Create the rectangular slot
# The slot goes through the center along the long axis
slot_rect = cq.Workplane("XY").rect(slot_length, slot_width).extrude(part_height)

# Step 6: Combine the hole and slot geometries into a single "tool" for cutting
cutout_tool = center_hole.union(slot_rect)

# 3. Final Operation
# Subtract the cutout tool from the base body
result = base_body.cut(cutout_tool)

# Alternatively, this can be done more concisely using sketch operations or sequential boolean operations on a single Workplane stack.
# Let's try a more robust, single-chain approach which is often cleaner in CadQuery.

result = (
    cq.Workplane("XY")
    # Draw the outer profile
    .rect(part_length, part_width)        # The rectangular base
    .circle(center_radius)                # The central bulge
    .extrude(part_height)                 # Create solid
    # Now create the cutouts
    .faces(">Z")                          # Select top face
    .workplane()
    .rect(slot_length, slot_width)        # Rectangular slot profile
    .cutBlind(-part_height)               # Cut through
    .faces(">Z")
    .workplane()
    .circle(hole_radius)                  # Central circular hole
    .cutBlind(-part_height)               # Cut through
)

# Refined approach to ensure perfect boolean union of the slot/hole geometry before cutting
# to match the image exactly (where the slot and hole merge cleanly).

# Create the main solid block first
main_body = (
    cq.Workplane("XY")
    .rect(part_length, part_width)
    .union(cq.Workplane("XY").circle(center_radius).extrude(part_height))
    .extrude(part_height)  # Note: logic above was mixed. Let's restart logic for clarity.
)

# Correct Logic:
# 1. Base rectangle
base = cq.Workplane("XY").rect(part_length, part_width).extrude(part_height)

# 2. Central cylinder
center = cq.Workplane("XY").circle(center_radius).extrude(part_height)

# 3. Fuse them
solid = base.union(center)

# 4. Create the cut profile
# We want to cut a shape that is the union of a circle and a rectangle
cut_shape = (
    cq.Workplane("XY")
    .rect(slot_length, slot_width)
    .union(cq.Workplane("XY").circle(hole_radius).extrude(part_height)) # Create 2D union? No, union works on solids or 2D wires separately.
    .extrude(part_height)
)
# Actually, creating the cutter as a solid is easier.
cutter_rect = cq.Workplane("XY").rect(slot_length, slot_width).extrude(part_height)
cutter_circ = cq.Workplane("XY").circle(hole_radius).extrude(part_height)
cutter = cutter_rect.union(cutter_circ)

# 5. Apply cut
result = solid.cut(cutter)