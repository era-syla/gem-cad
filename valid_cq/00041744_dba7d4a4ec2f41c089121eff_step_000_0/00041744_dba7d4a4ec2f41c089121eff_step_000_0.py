import cadquery as cq

# --- Parameters ---
# Main Body Dimensions
body_length = 55.0
body_width = 32.0
body_height = 16.0
fillet_radius = 4.0

# Joint & Shaft Dimensions
sphere_radius = 13.0
shaft_radius = 6.5
shaft_length = 32.0

# Lever Dimensions
lever_pos_x = -6.0
lever_pos_y = -8.0
lever_radius = 4.0

# --- Geometry Construction ---

# 1. Main Housing Body
# Rectangular block with rounded vertical corners, aligned so front face is at X=0
body = (cq.Workplane("XY")
        .box(body_length, body_width, body_height)
        .edges("|Z").fillet(fillet_radius)
        .translate((-body_length/2, 0, 0))
        )

# 2. Transition Neck
# Loft from a rectangle on the body face to a circle near the sphere center
# Starts slightly inside the body and ends inside the sphere for solid union
neck = (cq.Workplane("YZ")
        .workplane(offset=-2)
        .rect(body_width - 2, body_height - 2)
        .workplane(offset=12) # Distance to sphere center
        .circle(sphere_radius - 0.5)
        .loft(combine=False)
        )

# 3. Spherical Joint
# The bulbous connection point
ball_center_x = 10.0
ball = (cq.Workplane("XY")
        .center(ball_center_x, 0)
        .sphere(sphere_radius)
        )

# 4. Shaft
# Cylindrical extension from the sphere
shaft = (cq.Workplane("YZ")
         .workplane(offset=ball_center_x)
         .circle(shaft_radius)
         .extrude(shaft_length)
         )

# 5. Shaft Tip
# Rounded end with a slotted screw-like detail
tip_pos_x = ball_center_x + shaft_length
tip = (cq.Workplane("YZ")
       .workplane(offset=tip_pos_x)
       .sphere(shaft_radius)
       )

# Create the slot cut
slot = (cq.Workplane("YZ")
        .workplane(offset=tip_pos_x + shaft_radius/2)
        .rect(2.0, shaft_radius * 2.5)
        .extrude(-6)
        )
tip = tip.cut(slot)

# 6. Lever Mechanism
# Cylindrical pivot base on top of the body
lever_base_z = body_height / 2
pivot = (cq.Workplane("XY")
         .workplane(offset=lever_base_z)
         .center(lever_pos_x, lever_pos_y)
         .circle(lever_radius)
         .extrude(3.0)
         )

# Lever Handle
# Modeled by extruding a custom 2D profile
handle_profile = (cq.Workplane("XY")
                  .workplane(offset=lever_base_z + 1.0)
                  .center(lever_pos_x, lever_pos_y)
                  .transformed(rotate=(0, 0, 35)) # Angle the handle for visual interest
                  .move(0, -lever_radius/2)
                  .lineTo(0, 20)
                  .threePointArc((4, 22), (8, 20))
                  .lineTo(8, -lever_radius/2)
                  .close()
                  .extrude(5.0)
                  .edges("|Z").fillet(2.0)
                  .edges(">Z").fillet(1.0)
                  )

# Decorative pin on top of lever pivot
pin = (cq.Workplane("XY")
       .workplane(offset=lever_base_z + 5.0)
       .center(lever_pos_x, lever_pos_y)
       .circle(2.0)
       .extrude(1.5)
       )

# 7. Bottom Fins / Latch
# Curved structure underneath the neck/body junction
# Create a base shape on the XZ plane
fin_shape = (cq.Workplane("XZ")
             .workplane(offset=0)
             .moveTo(0, -body_height/2)
             .lineTo(0, -body_height/2 - 6)
             .threePointArc((8, -body_height/2 - 8), (14, -body_height/2 - 4))
             .lineTo(14, -body_height/2 + 2)
             .close()
             .extrude(body_width/2 - 2, both=True) # Extrude symmetrically
             )

# Cutters to slice the block into ribs
cut_width = 4.0
cut_tool = (cq.Workplane("XY")
            .workplane(offset=-20)
            .rect(20, cut_width)
            .extrude(20)
            )

# Create specific cuts to form a 3-rib structure
gap1 = cut_tool.translate((5, 6, 0))
gap2 = cut_tool.translate((5, -6, 0))

fins = fin_shape.cut(gap1).cut(gap2)

# --- Assembly ---
# Union all components into a single solid
result = (body
          .union(neck)
          .union(ball)
          .union(shaft)
          .union(tip)
          .union(pivot)
          .union(handle_profile)
          .union(pin)
          .union(fins)
          )