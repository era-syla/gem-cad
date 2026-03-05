import cadquery as cq

# --- Parameters ---

# Central wheel/housing parameters
wheel_outer_radius = 20.0
wheel_thickness = 10.0
central_hole_radius = 3.0
groove_depth = 2.0
groove_width = 2.0

# Side cylinder (axle/mount) parameters
mount_radius_large = 6.0
mount_height_large = 15.0
mount_radius_small = 3.0
mount_height_small = 10.0  # Height of the pin extending from the mount
mount_offset_x = 25.0  # Distance from center
mount_offset_y = 10.0  # Vertical offset based on visual perspective

# Rear cylinder (small post) parameters
post_radius = 4.0
post_height = 15.0
post_offset_x = 20.0
post_offset_y = -5.0 # Visual offset

# Separate bearing/ring component parameters
bearing_outer_radius = 8.0
bearing_inner_radius = 4.0
bearing_thickness = 5.0
bearing_rim_thickness = 1.0
bearing_offset_x = 40.0 # Distance to the separate part
bearing_offset_z = 15.0 # Height offset

# --- Modeling ---

# 1. Main Central Wheel
# Create the base cylinder
wheel = cq.Workplane("XY").circle(wheel_outer_radius).extrude(wheel_thickness)

# Create a central hole
wheel = wheel.faces(">Z").workplane().hole(central_hole_radius * 2)

# Create a groove in the middle (simulating a split or pulley groove)
# We'll subtract a torus or a cylinder from the side
groove_cutter = (
    cq.Workplane("XY")
    .workplane(offset=wheel_thickness / 2 - groove_width / 2)
    .circle(wheel_outer_radius + 1) # Make it larger than outer
    .extrude(groove_width)
)

# In the image, it looks more like a slot cut into the cylinder, or two halves.
# Let's model it as a simple aesthetic groove around the circumference.
# Since simple subtraction is tricky on the cylindrical face without plugins, 
# let's just make two cylinders with a gap or a smaller cylinder in between.
# Alternative approach: Revolve a profile.

# Let's stick to the visual: A cylinder with a line in the middle.
# We'll actually construct it as two cylinders joined by a slightly smaller inner cylinder.
wheel_half_thickness = (wheel_thickness - groove_width) / 2
left_half = cq.Workplane("XY").circle(wheel_outer_radius).extrude(wheel_half_thickness)
right_half = cq.Workplane("XY").workplane(offset=wheel_half_thickness + groove_width).circle(wheel_outer_radius).extrude(wheel_half_thickness)
inner_connector = cq.Workplane("XY").workplane(offset=wheel_half_thickness).circle(wheel_outer_radius - groove_depth).extrude(groove_width)

main_assembly = left_half.union(inner_connector).union(right_half)
main_assembly = main_assembly.faces(">Z").workplane().hole(central_hole_radius * 2)

# Rotate main wheel to stand upright like in the image (Y-up approx)
main_assembly = main_assembly.rotate((0,0,0), (1,0,0), 90)


# 2. Side Mount (The stepped cylinder on the left)
# It consists of a larger base and a smaller pin.
mount_base = cq.Workplane("XY").circle(mount_radius_large).extrude(mount_height_large)
mount_pin = (
    cq.Workplane("XY")
    .workplane(offset=mount_height_large)
    .circle(mount_radius_small)
    .extrude(mount_height_small)
)
side_mount = mount_base.union(mount_pin)

# Position the side mount relative to the wheel
# In the image, it's to the "left" and slightly "down" relative to the wheel center
side_mount = side_mount.translate((-mount_offset_x, -mount_offset_y, -mount_height_large/2))


# 3. Rear/Right Post (The cylinder behind/to the right)
right_post = cq.Workplane("XY").circle(post_radius).extrude(post_height)
# Position it
right_post = right_post.translate((post_offset_x, post_offset_y, -post_height/2))


# 4. Separate Bearing/Ring (Floating to the right)
# Create a rimmed shape
bearing_body = cq.Workplane("YZ").circle(bearing_outer_radius).extrude(bearing_thickness)
bearing_hole = (
    cq.Workplane("YZ")
    .workplane(offset=-1) # Start slightly before
    .circle(bearing_inner_radius)
    .extrude(bearing_thickness + 2)
)
# Create the recess for the bearing look (rims on both sides)
recess_front = (
    cq.Workplane("YZ")
    .workplane(offset=bearing_rim_thickness)
    .circle(bearing_outer_radius - bearing_rim_thickness)
    .extrude(bearing_thickness - 2 * bearing_rim_thickness)
)
# Re-add the inner hub
hub = (
    cq.Workplane("YZ")
    .workplane(offset=bearing_rim_thickness)
    .circle(bearing_inner_radius + bearing_rim_thickness)
    .extrude(bearing_thickness - 2 * bearing_rim_thickness)
)

floating_bearing = bearing_body.cut(bearing_hole).cut(recess_front).union(hub)
floating_bearing = floating_bearing.translate((bearing_offset_x, bearing_offset_z, 10))


# Combine all parts
result = main_assembly.union(side_mount).union(right_post).union(floating_bearing)
