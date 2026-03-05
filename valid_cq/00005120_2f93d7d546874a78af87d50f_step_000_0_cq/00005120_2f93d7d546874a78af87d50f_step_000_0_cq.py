import cadquery as cq

# --- Parameter Definitions ---

# Main body dimensions
base_diameter = 40.0  # Diameter of the bottom flange base
base_thickness = 5.0
hub_diameter = 15.0   # Diameter of the central neck
hub_height = 10.0
upper_body_diameter = 40.0
upper_body_height = 15.0
upper_body_inner_diameter = 30.0

# Flange mounting holes
mount_hole_circle_radius = 16.0
mount_hole_diameter = 3.5
mount_hole_count = 3
mount_lug_radius = 4.0  # Radius of the bumps on the flange

# Sensor/Internal details
internal_boss_size = 5.0
internal_boss_protrusion = 2.0  # From inner wall
internal_boss_hole_dia = 2.0

# Lid dimensions
lid_diameter_outer = 34.0
lid_diameter_lip = 30.0 # Fits into upper_body_inner_diameter
lid_total_height = 8.0
lid_lip_height = 3.0
lid_thickness = 2.0

# Set screw dimensions
screw_dia = 3.0
screw_length = 6.0

# --- Geometry Construction ---

# 1. Base Flange
# We create the central disk first
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_thickness)

# Add the mounting lugs (ears)
lugs = (
    cq.Workplane("XY")
    .polarArray(base_diameter/2, 0, 360, mount_hole_count)
    .circle(mount_lug_radius)
    .extrude(base_thickness)
)

# Combine base and lugs
base = base.union(lugs)

# Add countersunk/counterbored holes
# Note: Image shows simple holes or possibly slight counterbore. Let's do simple holes.
base = (
    base.faces(">Z")
    .workplane()
    .polarArray(mount_hole_circle_radius, 0, 360, mount_hole_count)
    .hole(mount_hole_diameter)
)

# 2. Central Hub (Neck)
hub = (
    base.faces(">Z")
    .workplane()
    .circle(hub_diameter / 2)
    .extrude(hub_height)
)

# 3. Upper Housing Body
upper_body_z_start = base_thickness + hub_height
upper_body = (
    cq.Workplane("XY")
    .workplane(offset=upper_body_z_start)
    .circle(upper_body_diameter / 2)
    .extrude(upper_body_height)
)

# Add lugs to the upper body as well (aligned with bottom lugs)
upper_lugs = (
    cq.Workplane("XY")
    .workplane(offset=upper_body_z_start)
    .polarArray(upper_body_diameter/2, 0, 360, mount_hole_count)
    .circle(mount_lug_radius)
    .extrude(upper_body_height)
)
upper_body = upper_body.union(upper_lugs)

# Hollow out the upper body
upper_body = (
    upper_body.faces(">Z")
    .workplane()
    .hole(upper_body_inner_diameter, depth=upper_body_height) # Blind hole or through? Image implies through to the hub.
)

# Drill through the hub to connect to the bottom? 
# The image shows a hole in the bottom of the upper cup.
# Let's drill a connecting hole through the hub.
hub_hole_dia = hub_diameter - 4.0
combined_body = base.union(hub).union(upper_body)
combined_body = (
    combined_body.faces(">Z")
    .workplane()
    .hole(hub_hole_dia, depth=upper_body_height + hub_height) # Go deep enough to pass through hub
)


# 4. Internal Feature (Square Boss with Hole)
# Located inside the upper cup, on the wall.
# We need to position a workplane on the inner cylindrical face or construct it relative to center.
square_boss = (
    cq.Workplane("XY")
    .workplane(offset=upper_body_z_start + upper_body_height/2) # Middle of upper body
    .center(upper_body_inner_diameter/2 - internal_boss_protrusion/2, 0) # Position near wall
    .box(internal_boss_protrusion, internal_boss_size, internal_boss_size)
)

# Add the small pin/hole on the boss
boss_pin = (
    cq.Workplane("XY")
    .workplane(offset=upper_body_z_start + upper_body_height/2 + internal_boss_size/2)
    .center(upper_body_inner_diameter/2 - internal_boss_protrusion/2, 0)
    .circle(internal_boss_hole_dia/2)
    .extrude(1.0)
)

final_housing = combined_body.union(square_boss).union(boss_pin)

# 5. The Lid (Modeled separately, then positioned for the "exploded" look)
lid = (
    cq.Workplane("XY")
    .circle(lid_diameter_outer / 2)
    .extrude(lid_total_height - lid_lip_height)
)

lid_lip = (
    lid.faces("<Z")
    .workplane()
    .circle(lid_diameter_lip / 2)
    .extrude(lid_lip_height)
)
lid = lid.union(lid_lip)

# Fillet the top edge of the lid for aesthetics
lid = lid.edges(">Z").fillet(1.0)

# Move the lid up for the exploded view
lid_exploded = lid.translate((0, 0, upper_body_z_start + upper_body_height + 15))

# 6. The Screw (Modeled separately)
# Creating a simple threaded-look cylinder
screw = (
    cq.Workplane("XZ")
    .circle(screw_dia / 2)
    .extrude(screw_length)
)
# Move screw to the side for exploded view
screw_exploded = screw.rotate((0,0,0), (0,1,0), 90).translate((-30, 0, upper_body_z_start + upper_body_height/2))


# Combine everything into one object for visualization 'result'
# Note: In a real assembly, these would be separate objects. 
# Here we union them just to return a single 'result' variable as requested.
result = final_housing.union(lid_exploded).union(screw_exploded)