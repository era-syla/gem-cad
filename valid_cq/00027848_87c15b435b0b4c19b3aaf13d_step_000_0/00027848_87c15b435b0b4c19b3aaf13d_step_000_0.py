import cadquery as cq

# --- Parameters ---
# Main Arm Dimensions
arm_length = 150.0
arm_width_wide = 28.0
arm_width_narrow = 20.0
arm_thickness = 5.0
taper_start = -20.0  # X coordinate where taper begins from pivot area

# Attachment Positions
top_block_pos = -25.0
side_tab_tri_pos = -55.0
side_tab_rect_pos = -95.0

# Bracket Dimensions
bracket_len = 50.0
bracket_width = 45.0
bracket_thickness = 4.0
bracket_wall_height = 40.0

# --- Geometry Construction ---

# 1. Main Lever Arm
# Define the profile of the arm on the XY plane
# Pivot center is at (0,0)
pts = [
    (25, arm_width_wide/2), 
    (25, -arm_width_wide/2),
    (taper_start + 10, -arm_width_wide/2), 
    (taper_start, -arm_width_narrow/2),
    (-arm_length, -arm_width_narrow/2),
    (-arm_length, arm_width_narrow/2),
    (taper_start, arm_width_narrow/2),
    (taper_start + 10, arm_width_wide/2)
]

arm = (cq.Workplane("XY")
       .polyline(pts).close()
       .extrude(arm_thickness)
       .edges("|Z and <X").fillet(arm_width_narrow/2 - 0.1)  # Round off the far end
       )

# Pivot hole in Arm
arm = arm.faces(">Z").workplane().circle(4.1).cutThruAll()

# 2. Top Reinforcement Block
# Sits on top of the arm near the pivot
top_block = (cq.Workplane("XY")
             .workplane(offset=arm_thickness)
             .center(top_block_pos, 0)
             .box(35, 18, 6)
             )
# Holes in top block
top_block = (top_block.faces(">Z").workplane()
             .pushPoints([(-8, 0), (8, 0)])
             .circle(2.6).cutThruAll()
            )
arm = arm.union(top_block)

# 3. Triangular Side Tab
# Sticks out horizontally from the side of the arm
tri_tab = (cq.Workplane("XY")
           .moveTo(side_tab_tri_pos, -arm_width_narrow/2 + 0.1)
           .lineTo(side_tab_tri_pos, -arm_width_narrow/2 - 15)
           .lineTo(side_tab_tri_pos - 15, -arm_width_narrow/2 + 0.1)
           .close()
           .extrude(arm_thickness)
          )
# Hole in triangular tab
tri_tab = (tri_tab.faces(">Z").workplane()
           .moveTo(side_tab_tri_pos - 5, -arm_width_narrow/2 - 5)
           .circle(2.0).cutThruAll()
          )
arm = arm.union(tri_tab)

# 4. Rectangular Side Drop Tab
# Attached to the side and hangs down
rect_tab = (cq.Workplane("XY")
            .workplane(offset=arm_thickness/2)
            .center(side_tab_rect_pos, -arm_width_narrow/2 - 2)
            .box(18, 4, 20)
            .translate((0, 0, -8)) # Shift downwards so it hangs below arm
           )
# Hole in rectangular tab
rect_tab = (rect_tab.faces(">Y").workplane()
            .center(0, -4)
            .circle(2.0).cutThruAll()
           )
arm = arm.union(rect_tab)

# 5. Base Mounting Bracket
# Horizontal Plate (underneath the arm pivot)
bracket_base = (cq.Workplane("XY")
                .workplane(offset=-bracket_thickness)
                .center(5, 5) 
                .box(bracket_len, bracket_width, bracket_thickness)
               )

# Vertical Plate (Side Wall)
# Positioned at the 'back' relative to the arm attachments (positive Y)
bracket_wall = (cq.Workplane("XZ")
                .workplane(offset=5 + bracket_width/2 - bracket_thickness)
                .center(5, -bracket_wall_height/2 - bracket_thickness)
                .box(bracket_len, bracket_thickness, bracket_wall_height)
               )

# Horizontal Ridge/Stiffener on Wall
ridge = (cq.Workplane("XZ")
         .workplane(offset=5 + bracket_width/2 - bracket_thickness/2)
         .center(5, -bracket_wall_height/2 - 5)
         .box(bracket_len - 10, 2, 4)
        )
bracket_wall = bracket_wall.union(ridge)
bracket = bracket_base.union(bracket_wall)

# 6. Pivot Hardware
# Main Pin
pin = (cq.Workplane("XY")
       .workplane(offset=-bracket_thickness)
       .circle(4.0)
       .extrude(bracket_thickness + arm_thickness + 20)
      )

# Pivot Boss/Washer on top of arm
boss = (cq.Workplane("XY")
        .workplane(offset=arm_thickness)
        .circle(8.0)
        .extrude(2.0)
       )

# Hex Bolt Assembly (Secondary attachment point)
hex_pos_x, hex_pos_y = 18, -12
hex_bolt = (cq.Workplane("XY")
            .workplane(offset=arm_thickness)
            .center(hex_pos_x, hex_pos_y)
            .polygon(6, 6.0) # Hex head
            .extrude(5.0)
           )
hex_shaft = (cq.Workplane("XY")
             .workplane(offset=-bracket_thickness - 2)
             .center(hex_pos_x, hex_pos_y)
             .circle(3.0)
             .extrude(bracket_thickness + arm_thickness + 2 + 5)
            )
hex_bolt = hex_bolt.union(hex_shaft)

# 7. Rear Stop Block (Stationary)
# Attached to bracket, behind pivot area
rear_block = (cq.Workplane("XY")
              .workplane(offset=0) # Sits on base plate surface
              .center(20, 15)
              .box(12, 12, 15, centered=(True, True, False))
             )
# Hole through rear block
rear_block = (rear_block.faces(">X").workplane()
              .center(0, 8)
              .circle(2.0).cutThruAll()
             )

# --- Final Assembly ---
# Combine all parts into a single result
result = arm.union(bracket).union(pin).union(boss).union(hex_bolt).union(rear_block)