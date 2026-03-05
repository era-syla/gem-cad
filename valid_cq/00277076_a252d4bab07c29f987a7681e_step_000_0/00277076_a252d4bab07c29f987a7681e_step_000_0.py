import cadquery as cq

# --- Parameters ---
# Overall Dimensions
overall_width = 800.0

# Horizontal Rails
rail_diam = 16.0
rail_length = overall_width
rail_spacing = 35.0  # Vertical center-to-center distance
num_rails = 3

# End Posts
post_diam = 26.0
post_height = 160.0
post_x_offset = (overall_width / 2.0) - 40.0
post_z_base = -30.0 # Base of post relative to bottom rail center

# Central Mount
mount_back_thick = 15.0
mount_base_width = 110.0
mount_top_width = 30.0
mount_plate_z_top = (num_rails - 1) * rail_spacing + 25.0
mount_plate_z_bottom = -25.0

# Central Vertical Pole
pole_diam = 22.0
pole_height = 150.0 # Height extending above the mount body
pole_wall_thick = 4.0

# Front Clamps
clamp_width = 20.0
clamp_thick = 6.0
clamp_spacing = 50.0 # Distance between left and right clamp
clamp_height = (num_rails - 1) * rail_spacing + 40.0

# --- Modeling ---

# 1. Horizontal Rails
# Create a single cylinder and replicate it
def make_rail(z_pos):
    # Main cylinder
    rail = (cq.Workplane("YZ", origin=(0, 0, z_pos))
            .workplane(offset=-rail_length/2.0)
            .circle(rail_diam/2.0)
            .extrude(rail_length))
    
    # Spherical caps for ends
    cap_left = (cq.Workplane("YZ", origin=(0, 0, z_pos))
                .workplane(offset=-rail_length/2.0)
                .sphere(rail_diam/2.0))
    cap_right = (cq.Workplane("YZ", origin=(0, 0, z_pos))
                 .workplane(offset=rail_length/2.0)
                 .sphere(rail_diam/2.0))
                 
    return rail.union(cap_left).union(cap_right)

rails = make_rail(0)
for i in range(1, num_rails):
    rails = rails.union(make_rail(i * rail_spacing))

# 2. End Posts
def make_post(x_pos):
    # Vertical Cylinder
    p = (cq.Workplane("XY", origin=(x_pos, 0, post_z_base))
         .circle(post_diam/2.0)
         .extrude(post_height))
    
    # Hemispherical Top
    dome = (cq.Workplane("XY", origin=(x_pos, 0, post_z_base + post_height))
            .sphere(post_diam/2.0))
            
    return p.union(dome)

left_post = make_post(-post_x_offset)
right_post = make_post(post_x_offset)

# 3. Central Mount Body (Back Plate)
# Trapezoidal extrusion behind the rails
mount_body = (cq.Workplane("XZ", origin=(0, rail_diam/2.0, 0))
              .moveTo(-mount_base_width/2.0, mount_plate_z_bottom)
              .lineTo(mount_base_width/2.0, mount_plate_z_bottom)
              .lineTo(mount_top_width/2.0, mount_plate_z_top)
              .lineTo(-mount_top_width/2.0, mount_plate_z_top)
              .close()
              .extrude(mount_back_thick)) # Extrudes in +Y direction (away from rails)

# 4. Central Vertical Pole
# Cylinder sitting on top of the mount body
pole_y_center = rail_diam/2.0 + mount_back_thick/2.0
pole = (cq.Workplane("XY", origin=(0, pole_y_center, mount_plate_z_top))
        .circle(pole_diam/2.0)
        .extrude(pole_height))

# Create hole in the pole
pole_hole = (cq.Workplane("XY", origin=(0, pole_y_center, mount_plate_z_top + pole_height))
             .circle((pole_diam - 2*pole_wall_thick)/2.0)
             .extrude(-pole_height - 10)) # Cut downwards

pole = pole.cut(pole_hole)

# 5. Front Clamps
def make_clamp_assembly(x_offset):
    # Clamp Plate
    # XZ Plane normal is -Y. Origin at rail surface (-rail_diam/2). 
    # Extruding positive thickness moves further -Y (front).
    clamp_z_center = ((num_rails - 1) * rail_spacing) / 2.0
    
    plate = (cq.Workplane("XZ", origin=(x_offset, -rail_diam/2.0, clamp_z_center))
             .rect(clamp_width, clamp_height)
             .extrude(clamp_thick))
    
    # Bolts
    # Add simple bolt heads on the front face of the clamp
    bolts = None
    front_face_y = -(rail_diam/2.0 + clamp_thick)
    
    for i in range(num_rails):
        z = i * rail_spacing
        bolt = (cq.Workplane("XZ", origin=(x_offset, front_face_y, z))
                .circle(3.5) # Bolt head radius
                .extrude(2.0)) # Extrude out (further -Y)
        
        if bolts is None:
            bolts = bolt
        else:
            bolts = bolts.union(bolt)
            
    return plate.union(bolts)

clamp_left = make_clamp_assembly(-clamp_spacing/2.0)
clamp_right = make_clamp_assembly(clamp_spacing/2.0)

# Combine all components
result = (rails
          .union(left_post)
          .union(right_post)
          .union(mount_body)
          .union(pole)
          .union(clamp_left)
          .union(clamp_right)
          )