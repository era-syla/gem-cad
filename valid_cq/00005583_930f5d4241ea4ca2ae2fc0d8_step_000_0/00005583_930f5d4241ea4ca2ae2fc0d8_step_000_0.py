import cadquery as cq
import math

# --- Parameters ---
length = 120.0          # Overall length of the tube
outer_diam = 40.0       # Outer diameter
wall_thickness = 3.0    # Wall thickness
inner_diam = outer_diam - (2 * wall_thickness)

# Notch parameters (Near end feature)
notch_len = 10.0        # Length of the rectangular cutout along the tube axis
notch_height = 5.0      # Depth of the cutout from the split edge (circumferential direction)

# Bayonet/Hole parameters (Far end feature)
hole_dist_from_end = 15.0  # Distance from the far face to the hole center
hole_diameter = 5.0        # Diameter of the locking hole
slot_width = 2.5           # Width of the slot leading to the hole
hole_angle = 20.0          # Angular position of the hole center from the split edge (degrees)

# --- Derived Values ---
outer_radius = outer_diam / 2.0
inner_radius = inner_diam / 2.0
mean_radius = (outer_radius + inner_radius) / 2.0

# --- Geometry Construction ---

# 1. Create the base tube
# We start with a full cylinder tube centered on the Z-axis
tube = cq.Workplane("XY").circle(outer_radius).circle(inner_radius).extrude(length)

# 2. Cut the tube in half to create a semi-cylindrical shell
# We want to keep the top half (Y > 0), so we remove the bottom half (Y < 0).
# We create a large box shifted in -Y to perform the cut.
cut_box = (
    cq.Workplane("XY")
    .center(0, -outer_radius) # Shift center so box covers negative Y
    .box(outer_diam * 2.5, outer_diam, length * 2.0)
)
shell = tube.cut(cut_box)

# 3. Create the Notch at the near end (Z=0)
# Located on the split edge (Y=0), on the positive X side.
# The cutter box is positioned to remove material from the corner.
notch_cutter = (
    cq.Workplane("XY")
    .workplane(offset=notch_len / 2.0)      # Move workplane up to center of notch length
    .center(outer_radius, notch_height / 2.0) # Position X on rim, Y centered for the cut depth
    .box(wall_thickness * 4.0, notch_height, notch_len) # X width is large to ensure wall cut
)

result = shell.cut(notch_cutter)

# 4. Create the Bayonet Hole and Slot at the far end (Z = length)
# 4a. The Hole
# Calculate position based on angle
hole_z = length - hole_dist_from_end
rad_angle = math.radians(hole_angle)
# Determine (x, y) for hole center on the mean radius
hole_x = mean_radius * math.cos(rad_angle)
hole_y = mean_radius * math.sin(rad_angle)

# Create a cylinder cutter oriented radially at the hole position
hole_cutter = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, hole_z), rotate=cq.Vector(0, 0, hole_angle)) # Position and align with angle
    .transformed(rotate=cq.Vector(0, 90, 0)) # Rotate local Z to point radially outward
    .circle(hole_diameter / 2.0)
    .extrude(outer_diam, both=True) # Cut through the wall
)
result = result.cut(hole_cutter)

# 4b. The Slot
# The slot connects the split edge (Y=0) to the hole (Y=hole_y).
# We use a box cutter.
slot_cutter = (
    cq.Workplane("XY")
    .workplane(offset=hole_z)               # Position at hole Z level
    .center(mean_radius, hole_y / 2.0)      # Center X approx at wall, Center Y halfway to hole
    .box(wall_thickness * 4.0, hole_y, slot_width) # Box height spans 0 to hole_y
)
result = result.cut(slot_cutter)