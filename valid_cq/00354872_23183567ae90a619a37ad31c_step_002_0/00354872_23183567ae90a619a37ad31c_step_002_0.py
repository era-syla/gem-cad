import cadquery as cq
import math

# --- Parameters ---
# Overall Dimensions
base_length = 60.0
head_length = 45.0
width = 40.0
thickness = 10.0
bend_angle = 45.0  # Degrees downward

# Mounting Holes (Base)
hole_spacing_x = 35.0
hole_spacing_y = 24.0
hole_diameter = 5.0
csk_diameter = 10.0
csk_angle = 90.0

# Head Features
slot_width = 14.0
curve_radius = 40.0  # Radius of the implied mounting cylinder at the tip
curve_cut_depth = 3.0 # How deep the curve cuts into the tip

# --- derived variables ---
angle_rad = math.radians(bend_angle)
# Tip coordinates calculation relative to the hinge point
dx = head_length * math.cos(angle_rad)
dz = -head_length * math.sin(angle_rad)

# --- Geometry Construction ---

# 1. Create the Main Body using a Side Profile Sketch
# We draw the top line of the profile (base + angled head)
# Then offset it to create thickness, then extrude.
path_pts = [
    (0, 0),                 # Start of base
    (base_length, 0),       # Hinge point
    (base_length + dx, dz)  # Tip of head
]

# Create the solid body
main_body = (
    cq.Workplane("XZ")
    .polyline(path_pts)
    .offset2D(-thickness, kind="intersection") # Offset downwards
    .extrude(width / 2.0, both=True)          # Extrude symmetrically
)

# 2. Add Countersunk Holes to the Base
# We select the top face (Z=0 plane)
result = (
    main_body
    .faces(">Z").workplane()
    .center(base_length / 2.0, 0) # Center workplane on the base section
    .rect(hole_spacing_x, hole_spacing_y)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)

# 3. Cut the Slot in the Head
# Create a cutter object aligned with the angled head
# We create a box, align it, and then subtract it.
slot_cutter_length = head_length * 2.0 # Make it long enough to cut through
slot_cutter = (
    cq.Workplane("XY")
    .box(slot_cutter_length, slot_width, thickness * 3.0)
    # Move box so its local origin is near the start of the cut, allowing for some overlap
    .translate((slot_cutter_length / 2.0 - 5.0, 0, 0)) 
    # Rotate to match the head angle
    .rotate((0, 0, 0), (0, 1, 0), -bend_angle)
    # Move to the hinge point
    .translate((base_length, 0, 0))
)

result = result.cut(slot_cutter)

# 4. Cut the Curved Profile at the Tip
# We simulate a cylindrical mount by creating a cylinder transverse to the head
# and subtracting it from the tip.
# Calculate center of the cutting cylinder
# We want the surface of the cylinder to intersect the tip with a specific depth
# Cylinder Axis is Y.
tip_x = base_length + dx
tip_z = dz

# Vector direction of the head
head_dir_x = math.cos(angle_rad)
head_dir_z = -math.sin(angle_rad)

# Position cylinder center along the extension of the head vector
# Distance = Radius - Desired Depth
dist_to_center = curve_radius - curve_cut_depth
cyl_center_x = tip_x + dist_to_center * head_dir_x
cyl_center_z = tip_z + dist_to_center * head_dir_z

curve_cutter = (
    cq.Workplane("XY")
    .cylinder(curve_radius, width * 2.0) # Create cylinder Z-aligned
    .rotate((0,0,0), (1,0,0), 90)        # Rotate to Y-aligned
    .translate((cyl_center_x, 0, cyl_center_z))
)

result = result.cut(curve_cutter)

# Export or display
# show_object(result)