import cadquery as cq

# --- Parameter Definitions ---
# Side Cheek parameters
cheek_length = 100.0
cheek_height_front = 30.0
cheek_height_rear = 15.0  # Tapering down
cheek_thickness = 5.0
cheek_spacing = 30.0  # Distance between the two side cheeks

# Axle/Support parameters
front_axle_diam = 6.0
front_axle_length = cheek_spacing + 30.0  # Stick out past cheeks
rear_support_diam = 6.0
rear_support_length = cheek_spacing + 30.0

# Wheel parameters
wheel_diam = 25.0
wheel_thickness = 5.0
wheel_hole_diam = front_axle_diam + 0.5  # Clearance

# Central Cylinder (Barrel) parameters
barrel_length = 80.0
barrel_diam = 20.0
barrel_trunnion_diam = 5.0  # The pivot pins for the barrel
barrel_trunnion_length = cheek_spacing + 10.0 # Must span the cheeks

# --- Geometry Construction ---

# 1. Create the Side Cheek
# We'll draw the profile of one cheek on the XZ plane and extrude it.
# The shape is roughly trapezoidal, taller at the front.
pts = [
    (0, 0),
    (cheek_length, 0),
    (cheek_length, cheek_height_rear),
    (0, cheek_height_front)
]

cheek = (cq.Workplane("XZ")
         .polyline(pts)
         .close()
         .extrude(cheek_thickness)
         )

# Add holes for axles/trunnions to the cheek
# Front axle hole
front_axle_pos_x = 20.0
front_axle_pos_z = 10.0

# Barrel trunnion hole (pivot point)
trunnion_pos_x = 45.0
trunnion_pos_z = 20.0

# Rear support/handle hole
rear_support_pos_x = cheek_length - 10.0
rear_support_pos_z = cheek_height_rear / 2.0 + 3.0

cheek_with_holes = (cheek
                    .faces(">Y")
                    .workplane()
                    .pushPoints([(front_axle_pos_x, front_axle_pos_z), 
                                 (trunnion_pos_x, trunnion_pos_z),
                                 (rear_support_pos_x, rear_support_pos_z)])
                    .hole(front_axle_diam) # Simplified: using same diameter for all holes for now, can be adjusted
                   )

# Position the two cheeks
left_cheek = cheek_with_holes.translate((0, -cheek_spacing/2 - cheek_thickness, 0))
right_cheek = cheek_with_holes.translate((0, cheek_spacing/2, 0))

# 2. Create Axles and Supports
# Front Axle
front_axle = (cq.Workplane("YZ")
              .circle(front_axle_diam/2)
              .extrude(front_axle_length)
              .translate((front_axle_pos_x, -front_axle_length/2, front_axle_pos_z))
              )

# Rear Support bar
rear_support = (cq.Workplane("YZ")
                .circle(rear_support_diam/2)
                .extrude(rear_support_length)
                .translate((rear_support_pos_x, -rear_support_length/2, rear_support_pos_z))
                )

# 3. Create the Barrel
# The barrel is a cylinder in the middle
barrel_main = (cq.Workplane("YZ")
               .circle(barrel_diam/2)
               .extrude(barrel_length)
               .translate((trunnion_pos_x - barrel_length/2, -barrel_length/2, trunnion_pos_z)) # Initial orientation wrong
               # Rotate to align with X axis
               .rotate((0,0,0), (0,0,1), 90) # Rotate 90 deg around Z
               # Re-position after rotation: Center of barrel at trunnion X
               .translate((trunnion_pos_x - barrel_length/2 + barrel_length/2, 0, trunnion_pos_z)) 
               )
# The rotation logic above is a bit tricky with translation. Let's do it simpler:
# Create barrel along X axis directly.
barrel = (cq.Workplane("YZ")
          .circle(barrel_diam/2)
          .extrude(barrel_length)
          .rotate((0,0,0), (0,1,0), 90) # Orient along X
          .translate((trunnion_pos_x - barrel_length/2, 0, trunnion_pos_z))
         )

# Create Barrel Trunnions (pins sticking out sideways)
trunnion_pin = (cq.Workplane("YZ")
                .circle(barrel_trunnion_diam/2)
                .extrude(barrel_trunnion_length)
                .translate((trunnion_pos_x, -barrel_trunnion_length/2, trunnion_pos_z))
               )

# Combine barrel parts
full_barrel = barrel.union(trunnion_pin)

# 4. Create Wheels
# Simple disc wheel
wheel_single = (cq.Workplane("YZ")
                .circle(wheel_diam/2)
                .extrude(wheel_thickness)
                .faces(">X").workplane().hole(wheel_hole_diam)
                )

# Position wheels on the front axle
# Based on the image, there is one clearly visible wheel in front
wheel_left = wheel_single.translate((front_axle_pos_x, -cheek_spacing/2 - cheek_thickness - wheel_thickness - 2, front_axle_pos_z))
wheel_right = wheel_single.translate((front_axle_pos_x, cheek_spacing/2 + cheek_thickness + 2, front_axle_pos_z))

# --- Assembly / Final Union ---

result = (left_cheek
          .union(right_cheek)
          .union(front_axle)
          .union(rear_support)
          .union(full_barrel)
          .union(wheel_left)
          # .union(wheel_right) # Uncomment to add the second wheel (hidden in perspective)
          )