import cadquery as cq

# --- Parameters ---
# Main Rail/Beam
beam_length = 200.0
beam_width = 20.0
beam_height = 40.0
beam_thickness = 5.0 # For the I-beam or C-channel like profile

# Side Supports (Legs)
support_width = 30.0
support_height = 80.0
support_base_depth = 60.0
support_top_depth = 20.0 # Tapered top
support_thickness = 10.0

# Base Rails (on the ground)
base_rail_length = 200.0
base_rail_width = 10.0
base_rail_height = 10.0
base_rail_offset = 60.0 # From center

# Carriage/Slider
carriage_width = 40.0
carriage_height = 60.0
carriage_thickness = 15.0
carriage_back_plate_height = 80.0
carriage_back_plate_thickness = 5.0

# --- Geometry Construction ---

# 1. Base Rails (The long thin bars on the ground)
def create_base_rail(offset_y):
    return (cq.Workplane("XY")
            .box(base_rail_length, base_rail_width, base_rail_height)
            .translate((0, offset_y, base_rail_height/2)))

rail_left = create_base_rail(-base_rail_offset)
rail_right = create_base_rail(base_rail_offset)

# 2. Side Supports (The trapezoidal legs)
def create_support(side_multiplier):
    # Sketching the trapezoidal profile on the YZ plane (side view)
    pts = [
        (0, 0),
        (support_base_depth, 0),
        (support_base_depth, support_height * 0.2), # Small vertical step up
        (support_top_depth + (support_base_depth-support_top_depth)/2 + 10, support_height), # Angled part
        ((support_base_depth-support_top_depth)/2 - 10, support_height),
        (0, support_height * 0.2)
    ]
    
    # Simplified approach: Extrude a trapezoid and cut or union
    # Let's try a direct extrusion of the profile from the side
    
    # Coordinates relative to the rail position
    # The support sits on the rail
    
    s = (cq.Workplane("YZ")
         .moveTo(-support_base_depth/2, base_rail_height)
         .lineTo(support_base_depth/2, base_rail_height)
         .lineTo(support_top_depth/2, base_rail_height + support_height)
         .lineTo(-support_top_depth/2, base_rail_height + support_height)
         .close()
         .extrude(support_width)
         )
    
    # Move to correct X position
    x_pos = side_multiplier * (beam_length/2 - support_width/2)
    
    # The rails are at Y = +/- base_rail_offset. 
    # The image shows the legs perpendicular to the rails, connecting the rails to the beam.
    # Actually, looking closer, the long rails are perpendicular to the main beam.
    # The "legs" slide on the rails? Or are fixed? Let's assume fixed for this static model.
    # The main beam spans X. The rails span Y.
    
    # Let's re-orient. 
    # Long rails along Y axis.
    # Main beam along X axis.
    
    # Re-doing the support logic based on this orientation.
    # Support is an extrusion along X. Profile is in YZ.
    
    y_pos = side_multiplier * base_rail_offset
    
    # Create the triangular/trapezoidal shape
    support_geo = (cq.Workplane("YZ")
                   .workplane(offset= -support_width/2) # Start face
                   .moveTo(-support_base_depth/2, base_rail_height)
                   .lineTo(support_base_depth/2, base_rail_height)
                   .lineTo(support_top_depth, base_rail_height + support_height)
                   .lineTo(-support_top_depth, base_rail_height + support_height)
                   .close()
                   .extrude(support_width)
                   .translate((0, y_pos, 0)) # Move to rail
                   )
    return support_geo

# Wait, re-evaluating the image perspective.
# The long thin bars are parallel. Let's call them Guide Rails.
# The structure spans across them.
# Let's align Guide Rails along Y.
# The Gantry Beam is along X.

# Refined Dimensions
rail_dist_y = 120.0
rail_len_y = 250.0
gantry_height = 60.0
beam_len_x = rail_dist_y + 40.0 

# --- RESTARTING BUILD WITH Y-AXIS RAILS ---

# 1. Guide Rails (Along Y)
guide_rail_geo = (cq.Workplane("XY")
    .box(10, rail_len_y, 10)
    .translate((beam_len_x/2 - 10, 0, 5))
)
guide_rail_geo_2 = (cq.Workplane("XY")
    .box(10, rail_len_y, 10)
    .translate((-beam_len_x/2 + 10, 0, 5))
)

# 2. Side Risers (Trapezoids connecting rails to beam)
def make_riser(x_pos):
    pts = [
        (-30, 0), (30, 0), # Base width 60
        (30, 10), # Vertical step
        (15, gantry_height), # Top width ~30
        (-15, gantry_height),
        (-30, 10)
    ]
    riser = (cq.Workplane("YZ")
             .polyline(pts).close()
             .extrude(15) # Thickness of the riser plate
             .translate((x_pos, 0, 10)) # Sit on top of the 10mm rail
             )
    return riser

riser_left = make_riser(-beam_len_x/2 + 10)
riser_right = make_riser(beam_len_x/2 - 10)

# 3. Main Horizontal Beam (Spanning X)
# It has a "C" or recessed profile on the front face.
beam_outer = (cq.Workplane("XZ")
              .box(beam_len_x - 40, 40, 40) # Length, Depth (Y), Height (Z)
              .translate((0, 20, 10 + gantry_height - 20)) # Align top with riser top
              )

# Cut the recess into the beam to make it look like a linear actuator base
beam_recess = (cq.Workplane("XZ")
               .box(beam_len_x - 50, 20, 25) 
               .translate((0, 31, 10 + gantry_height - 20)) # Shifted forward (Y+)
               )

beam = beam_outer.cut(beam_recess)


# 4. The Carriage (Center Assembly)
# Back plate (slides in the beam)
carriage_plate = (cq.Workplane("XY")
                  .box(30, 10, 70)
                  .translate((0, 30, 10 + gantry_height - 10)) # Z Center
                  )

# Front block (Main body of the carriage)
carriage_block = (cq.Workplane("XY")
                  .box(40, 20, 60)
                  .translate((0, 45, 10 + gantry_height - 20))
                  )

# Small connector/spacer
carriage_connector = (cq.Workplane("XY")
                      .box(20, 10, 40)
                      .translate((0, 35, 10 + gantry_height - 20))
                      )

carriage = carriage_plate.union(carriage_connector).union(carriage_block)

# 5. Rails re-adjustment
# The initial rail placement was a bit off relative to the risers.
# Let's define the rails based on riser position.
rail_l = (cq.Workplane("XY")
          .box(12, 300, 12)
          .translate((-beam_len_x/2 + 10 + 7.5, 0, 6)) # Center under the 15mm riser
          )

rail_r = (cq.Workplane("XY")
          .box(12, 300, 12)
          .translate((beam_len_x/2 - 10 - 7.5, 0, 6))
          )

# Combine everything
result = (rail_l
          .union(rail_r)
          .union(riser_left)
          .union(riser_right)
          .union(beam)
          .union(carriage)
          )