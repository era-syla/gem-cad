import cadquery as cq

# --- Parameters ---

# Main Platform Dimensions
deck_width = 2000.0
deck_length = 2500.0
deck_thickness = 100.0
toe_guard_height = 200.0
toe_guard_thickness = 10.0

# Lip (Folding ramp)
lip_length = 600.0
lip_width = 1500.0 # Slightly narrower than deck usually
lip_thickness = 20.0
lip_angle = 15.0 # Degrees raised

# Frame / Sub-structure
frame_beam_width = 100.0
frame_beam_height = 150.0

# Handrails (Safety barriers)
rail_height = 1000.0
rail_diameter = 40.0
rail_offset = 50.0

# Pit Frame / Curb Angles (The separate pieces)
curb_length_side = 3000.0 # Long side piece
curb_width_side = 200.0
curb_thickness_side = 10.0
curb_length_front = deck_width + 400.0
tail_length = 3500.0 # The long piece extending out

# --- Geometry Construction ---

# 1. Main Deck
# Create the base plate
deck = (cq.Workplane("XY")
        .box(deck_length, deck_width, deck_thickness)
        .translate((0, 0, deck_thickness/2))
       )

# 2. Side Toe Guards (Side walls of the platform)
# Left Guard
left_guard = (cq.Workplane("XY")
              .box(deck_length, toe_guard_thickness, toe_guard_height)
              .translate((0, deck_width/2 + toe_guard_thickness/2, toe_guard_height/2))
             )

# Right Guard
right_guard = (cq.Workplane("XY")
               .box(deck_length, toe_guard_thickness, toe_guard_height)
               .translate((0, -deck_width/2 - toe_guard_thickness/2, toe_guard_height/2))
              )

# 3. The Lip (Hinged ramp at the front)
# We model it angled up
lip = (cq.Workplane("XY")
       .box(lip_length, lip_width, lip_thickness)
       .rotate((0,0,0), (0,1,0), -lip_angle) # Angle up
       .translate((-deck_length/2 - (lip_length/2 * 0.9), 0, deck_thickness + (lip_length * 0.2))) # Approximate position based on rotation
      )

# Connect lip to main deck (Hinge area simulation)
hinge_block = (cq.Workplane("XY")
               .box(100, lip_width, deck_thickness)
               .translate((-deck_length/2 - 50, 0, deck_thickness/2))
              )

# 4. Safety Handrails (U-shaped railing on sides)
def create_railing(side_offset):
    path = (cq.Workplane("XZ")
            .moveTo(deck_length/2 - 100, 0)
            .lineTo(deck_length/2 - 100, rail_height)
            .lineTo(-deck_length/2 + 500, rail_height) # Top rail doesn't go all the way to the lip
            .lineTo(-deck_length/2 + 500, 0)
           )
    
    rail = (cq.Workplane("XY")
            .translate((0, side_offset, deck_thickness))
            .circle(rail_diameter/2)
            .sweep(path)
           )
    
    # Add a mid-rail
    mid_rail_geo = (cq.Workplane("YZ")
                    .circle(rail_diameter/2)
                    .extrude(deck_length - 600)
                    .translate((-deck_length/2 + 500 + (deck_length-600)/2, side_offset, deck_thickness + rail_height/2))
                    .rotate((0,0,0), (0,1,0), 90) # Fix orientation from YZ
                   )
    return rail.union(mid_rail_geo)

left_rail = create_railing(deck_width/2 - rail_offset)
right_rail = create_railing(-deck_width/2 + rail_offset)

# 5. Detail: Grates/Textured areas on deck
# Simplify as slightly raised recessed boxes
grate_size = 400.0
grate1 = (cq.Workplane("XY")
          .box(grate_size, grate_size, 5)
          .translate((0, 300, deck_thickness + 2.5))
         )
grate2 = (cq.Workplane("XY")
          .box(grate_size, grate_size, 5)
          .translate((0, -300, deck_thickness + 2.5))
         )

# 6. Rear Frame Structure (The mechanism behind the lip)
# Simplified block representation of hydraulics/linkage
rear_mech = (cq.Workplane("XY")
             .box(400, deck_width * 0.8, 400)
             .translate((-deck_length/2 - 200, 0, 200))
            )

# 7. The Ground/Pit Framework (The detached L-shaped and long pieces)

# The "L" shaped curb angle piece (front and side)
# Long side runner
side_curb = (cq.Workplane("XY")
             .box(curb_length_side, curb_width_side, curb_thickness_side) # Top face
             .translate((1000, -deck_width/2 - 400, 0)) # Positioned offset from main deck
            )
# Vertical part of the angle iron
side_curb_vert = (cq.Workplane("XY")
                  .box(curb_length_side, curb_thickness_side, 100)
                  .translate((1000, -deck_width/2 - 400 + curb_width_side/2, -50))
                 )

# The long tail piece (Cable run or guide rail)
tail_piece = (cq.Workplane("XY")
              .box(tail_length, 250, 50)
              .rotate((0,0,0), (0,0,1), -45) # Angled away
              .translate((1500, -1500, -100))
             )
             
# Connection T-piece for the tail
t_connection = (cq.Workplane("XY")
                .box(200, 1500, 50)
                .rotate((0,0,0), (0,0,1), 45) # Perpendicular to tail
                .translate((1500, -1500, -100))
               )

# Another separated floor channel piece
floor_channel = (cq.Workplane("XY")
                 .box(1500, 300, 20) # Flat plate
                 .translate((500, deck_width/2 + 400, 0))
                )
# Add flanges to make it C-channel style
fc_flange1 = (cq.Workplane("XY").box(1500, 20, 80).translate((500, deck_width/2 + 400 - 140, -40)))
fc_flange2 = (cq.Workplane("XY").box(1500, 20, 80).translate((500, deck_width/2 + 400 + 140, -40)))
floor_channel_assy = floor_channel.union(fc_flange1).union(fc_flange2)


# Combine Platform assembly
platform_assy = (deck
                 .union(left_guard)
                 .union(right_guard)
                 .union(lip)
                 .union(hinge_block)
                 .union(left_rail)
                 .union(right_rail)
                 .union(grate1)
                 .union(grate2)
                 .union(rear_mech)
                )

# Combine Pit/Ground components
pit_assy = (side_curb
            .union(side_curb_vert)
            .union(tail_piece)
            .union(t_connection)
            .union(floor_channel_assy)
           )

# Final Result
result = platform_assy.union(pit_assy)