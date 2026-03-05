import cadquery as cq

# --- Parameters ---
# Case dimensions
case_length = 90.0
case_width = 60.0
case_height = 25.0
wall_thickness = 2.0
corner_radius = 5.0
mount_ear_radius = 4.0

# IO Port dimensions (Side)
eth_width = 15.0
eth_height = 12.0
usb_width = 13.0
usb_height = 13.0
usb_spacing = 8.0  # spacing between USBs
side_ports_y_offset = -5.0 # adjust vertical position on the side face

# Other Side Port (HDMI/Power/Audio side usually, but purely geometric here)
# Let's approximate the square cutout on the left side
side_cutout_width = 12.0
side_cutout_height = 10.0
side_cutout_offset = 15.0 # from the corner

# Top Slot (GPIO/Camera ribbon cable)
top_slot_length = 40.0
top_slot_width = 4.0
top_slot_x_offset = 10.0 # offset from center

# Mounting holes
corner_hole_diam = 2.5
top_screw_hole_diam = 2.0
mount_hole_inset = 3.5

# --- Geometry Construction ---

# 1. Base Body Profile
# Create the rounded rectangle base
base_shape = (
    cq.Workplane("XY")
    .rect(case_length, case_width)
    .extrude(case_height)
    .edges("|Z").fillet(corner_radius)
)

# 2. Add Mounting "Ears" (Cylinders at corners)
# We need to find the centers of the corners.
# Based on case dimensions, corners are roughly at (+-L/2, +-W/2).
# But since we filleted, the original corners are gone, so we position relative to center.
cx = case_length / 2.0
cy = case_width / 2.0

# Create a sketch for the ears
ears = (
    cq.Workplane("XY")
    .rect(case_length, case_width, forConstruction=True)
    .vertices()
    .circle(mount_ear_radius)
    .extrude(case_height)
)

# 3. Combine Main Body and Ears
body = base_shape.union(ears)

# 4. Create the Lip/Overhang at Top and Bottom
# The image shows the top and bottom plates being slightly wider/having lips like thin plates.
# Let's add thin cylinders at top and bottom to simulate the "sandwich" look of the plates.
plate_thickness = 1.0
plate_overhang = 1.0 # Extra radius on the ears

top_plate = (
    cq.Workplane("XY")
    .workplane(offset=case_height)
    .rect(case_length, case_width, forConstruction=True)
    .vertices()
    .circle(mount_ear_radius + plate_overhang)
    .extrude(plate_thickness)
)
# We also need the main rect for the top plate to cover the body
top_plate_main = (
    cq.Workplane("XY")
    .workplane(offset=case_height)
    .rect(case_length, case_width)
    .extrude(plate_thickness)
    .edges("|Z").fillet(corner_radius) # Match corner radius but slightly larger perhaps? No, same looks fine.
)
top_plate = top_plate.union(top_plate_main)

bottom_plate = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness)
    .rect(case_length, case_width, forConstruction=True)
    .vertices()
    .circle(mount_ear_radius + plate_overhang)
    .extrude(plate_thickness)
)
bottom_plate_main = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness)
    .rect(case_length, case_width)
    .extrude(plate_thickness)
    .edges("|Z").fillet(corner_radius)
)
bottom_plate = bottom_plate.union(bottom_plate_main)

# Combine plates into body
result = body.union(top_plate).union(bottom_plate)

# 5. Shelling (Hollowing out the inside)
# For a visual model, we can just subtract a smaller version, but since we are cutting ports,
# a solid block is easier to work with. If we needed a true shell, we'd do:
# result = result.faces("-Z").shell(wall_thickness)
# For this exercise, we keep it solid to ensure robust boolean cuts, 
# assuming it's a "dummy" model or the cuts represent the interior voids.

# 6. Cuts: Side Ports (Ethernet/USB style) on the Right (+X face)
# We need to position relative to the +X face.
# The face center is at X = case_length/2.
right_face_center = cq.Location(cq.Vector(case_length/2, 0, case_height/2))

# We'll cut directly through the body.
# USB/Ethernet area usually has 2-4 ports. Image shows 2 distinct square-ish holes.
port_z = case_height / 2.0 
port_depth = 10.0 # How deep to cut in

# Cut 1 (Rightmost)
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=case_length/2.0 + plate_overhang + 1) # Start slightly outside
    .center(-case_width/4.0 + 3, port_z - case_height/2) # approximate Y position on face, Z relative to workplane center
    .rect(usb_width, usb_height)
    .extrude(-port_depth * 2) # Cut inwards
)

# Cut 2 (Next to it)
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=case_length/2.0 + plate_overhang + 1)
    .center(-case_width/4.0 + 3 + usb_width + 5, port_z - case_height/2)
    .rect(eth_width, eth_height)
    .extrude(-port_depth * 2)
)

# 7. Cuts: Side Cutout on the Front/Left (-Y face or -X face?)
# Looking at the image, the long side facing us has a cut. Let's assume the long side is aligned with X.
# So this is the -Y face.
front_face_y = -case_width/2.0
result = result.cut(
    cq.Workplane("XZ")
    .workplane(offset=front_face_y - plate_overhang - 1)
    .center(-case_length/4.0, port_z - case_height/2)
    .rect(side_cutout_width, side_cutout_height)
    .extrude(port_depth * 2) # Cut inwards (positive normal of XZ is -Y direction, so we extrude + to go into object? No, XZ normal is -Y. wait. XZ normal is +Y. So we need to offset to -Y and extrude +Y)
    # Let's simplify: just center it globally.
)


# 8. Cuts: Top Slot
# Long rectangular slot on the top face
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=case_height + plate_thickness + 1)
    .center(top_slot_x_offset, case_width/4.0)
    .rect(top_slot_length, top_slot_width)
    .extrude(-(plate_thickness * 2 + case_height)) # Cut down through top
)

# 9. Holes in the Corners (Mounting holes)
# These go through the "ears"
result = result.cut(
    cq.Workplane("XY")
    .rect(case_length, case_width, forConstruction=True)
    .vertices()
    .circle(corner_hole_diam / 2.0)
    .extrude(case_height + 2*plate_thickness + 5, both=True)
)

# 10. Small Screw Holes on Top Plate
# There are 4 small holes near the corners of the main rectangular body
screw_dx = case_length - 2*mount_hole_inset - 15 # Inset from edges
screw_dy = case_width - 2*mount_hole_inset - 5

result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=case_height + plate_thickness + 1)
    .rect(screw_dx, screw_dy, forConstruction=True)
    .vertices()
    .circle(top_screw_hole_diam / 2.0)
    .extrude(-5.0) # Shallow blind holes or through top plate
)

# 11. Split Line (Cosmetic Groove)
# The image shows a horizontal line running around the middle, indicating where the case splits.
# We can simulate this with a small cut or just leave it as the union of two parts.
# To make it look like the image, let's cut a tiny groove.
groove_path = (
    cq.Workplane("XY")
    .workplane(offset=case_height/2.0)
    .rect(case_length + 20, case_width + 20) # Bigger than case
    .rect(case_length - 10, case_width - 10) # Smaller than case
    .extrude(0.2) # Very thin cut
)
# Actually, easier to just create a small chamfer on the edges where they meet, 
# but a parametric groove is harder on a complex perimeter.
# We will skip the complex groove boolean for performance and reliability, 
# as the geometry is clearly a top and bottom assembly.

# Final cleanup: apply a small fillet to vertical edges of the ears to smooth them
# (Optional, as the cylinder creation already makes them smooth)

# Ensure the object is centered
# result = result.translate((0, 0, 0)) # Already centered on XY, Z is from -1 to 26