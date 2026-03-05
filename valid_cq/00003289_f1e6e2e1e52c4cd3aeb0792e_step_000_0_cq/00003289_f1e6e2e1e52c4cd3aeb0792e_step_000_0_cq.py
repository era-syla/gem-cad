import cadquery as cq

# --- Parameters ---
# Main side plates (ribs)
rib_length = 200.0
rib_height_front = 50.0  # Height at the taller end
rib_height_rear = 5.0    # Height at the pointy end
rib_thickness = 2.0
rib_spacing = 100.0      # Distance between the two main ribs

# Lightening holes in ribs
hole_diameters = [30.0, 20.0, 15.0]
hole_positions = [40.0, 80.0, 110.0] # X positions relative to front

# Front notch
notch_depth = 10.0
notch_angle = 60.0

# Cross bracing / Spars
spar_width = 15.0
spar_thickness = 2.0
spar_pos_x = 90.0  # Position along the rib
spar_height = 40.0

# Rear Flap / Control surface
flap_chord = 40.0
flap_thickness = 2.0
flap_angle = -15.0 # Degrees deflection

# Internal Mechanism (simplified)
actuator_box_width = 40.0
actuator_box_height = 15.0
actuator_box_length = 60.0


# --- Geometry Construction ---

# 1. Create a single Side Rib Profile
def create_rib_profile():
    # Points for the wedge shape
    pts = [
        (0, 0),
        (rib_length, (rib_height_front - rib_height_rear)/2.0 - rib_height_front/2.0), # Bottom rear
        (rib_length, (rib_height_front - rib_height_rear)/2.0 + rib_height_rear/2.0), # Top rear
        (0, rib_height_front),
    ]
    
    # Base shape
    rib = cq.Workplane("XY").polyline(pts).close().extrude(rib_thickness)
    
    # Add the V-notch at the front
    notch = (cq.Workplane("XY")
             .moveTo(0, rib_height_front/2.0)
             .polygon(3, notch_depth*2) # Triangle
             .extrude(rib_thickness * 2)
             .rotate((0,0,0), (0,0,1), 30) # Align triangle
             .translate((-notch_depth/2.0, 0, 0))
            )
    rib = rib.cut(notch)
    
    # Cut lightening holes
    for x_pos, dia in zip(hole_positions, hole_diameters):
        # Calculate Y center based on the tapering geometry
        # Slope calculation: m = (y2-y1)/(x2-x1)
        # Top edge line: (0, H) to (L, H_rear_top)
        # Bottom edge line: (0, 0) to (L, H_rear_bot)
        # Approximate geometric center line for simplicity
        y_center = (rib_height_front / 2.0) - (x_pos / rib_length) * ((rib_height_front - rib_height_rear) / 2.0)
        
        hole = (cq.Workplane("XY")
                .moveTo(x_pos, y_center)
                .circle(dia/2.0)
                .extrude(rib_thickness * 2))
        rib = rib.cut(hole)
        
    return rib

# Instantiate Ribs
left_rib = create_rib_profile().translate((0, 0, -rib_spacing/2.0))
right_rib = create_rib_profile().translate((0, 0, rib_spacing/2.0 - rib_thickness))

# 2. Cross Spar (The vertical plate connecting ribs)
spar = (cq.Workplane("YZ")
        .rect(rib_spacing - 2*rib_thickness, spar_height)
        .extrude(spar_width)
        .translate((spar_pos_x, spar_height/2.0, 0))
       )

# Add lightening holes to spar
spar_hole_dia = spar_height * 0.6
spar_holes = (cq.Workplane("YZ")
              .workplane(offset=spar_pos_x + spar_width/2.0)
              .moveTo(0, spar_height/2.0)
              .circle(spar_hole_dia/2.0)
              .extrude(spar_width * 2) # Cut through
              )
# We need to distribute holes along the spar
spar_cutout_left = spar_holes.translate((-rib_spacing/4.0, 0, 0))
spar_cutout_right = spar_holes.translate((rib_spacing/4.0, 0, 0))
spar_cutout_center = spar_holes

spar = spar.cut(spar_cutout_left).cut(spar_cutout_right).cut(spar_cutout_center)


# 3. Rear Flap / Trailing Edge
# It's a flat plate attached at the end
flap = (cq.Workplane("XY")
        .rect(flap_chord, rib_spacing)
        .extrude(flap_thickness)
        .rotate((0,0,0), (0,1,0), flap_angle) # Deflect down
        .translate((rib_length + flap_chord/2.0, 0, 0)) # Position at end
       )


# 4. Internal Mechanism Box (Actuator housing)
# Located between the ribs, somewhat forward of the spar
box = (cq.Workplane("XY")
       .rect(actuator_box_length, actuator_box_width)
       .extrude(actuator_box_height)
       .rotate((0,0,0), (1,0,0), 90) # Orient correctly
       .translate((spar_pos_x + 20, actuator_box_height/2.0, 0))
      )

# 5. Connecting Rods / Linkages (Simplified)
rod_diam = 2.0
rod = (cq.Workplane("XY")
       .circle(rod_diam/2.0)
       .extrude(rib_spacing)
       .rotate((0,0,0), (1,0,0), 90)
       .translate((spar_pos_x, spar_height, -rib_spacing/2.0))
      )

# Diagonal brace for flap
brace_pts = [(0,0), (30, 5), (30, -5)]
brace = (cq.Workplane("XY")
         .polyline(brace_pts).close()
         .extrude(2)
         .rotate((0,0,0), (0,1,0), -10)
         .translate((rib_length - 10, 5, 0))
        )

# Pivot point visual at the rear of the rib
pivot_pin = (cq.Workplane("YZ")
             .circle(3.0)
             .extrude(rib_spacing + 10)
             .translate((rib_length - 10, 5, -(rib_spacing + 10)/2.0))
             )


# --- Assembly ---
result = (left_rib
          .union(right_rib)
          .union(spar)
          .union(flap)
          .union(box)
          .union(rod)
          .union(pivot_pin)
          )

# Optional: Add the small triangular bracket visible near the spar
bracket_size = 15.0
bracket = (cq.Workplane("XY")
           .moveTo(0,0)
           .lineTo(bracket_size, 0)
           .lineTo(0, bracket_size)
           .close()
           .extrude(2.0)
           .rotate((0,0,0), (1,0,0), 90)
           .translate((spar_pos_x - bracket_size, 0, -rib_spacing/2.0 + rib_thickness))
           )
bracket2 = bracket.translate((0,0, 5)) # A double bracket often seen
result = result.union(bracket).union(bracket2)

# Ensure the final object is centered nicely
result = result.translate((-rib_length/2.0, 0, 0))