import cadquery as cq

# --- Geometric Parameters ---
# Dimensions are in millimeters based on typical spark/glow plug sizes

# Tip (Electrode)
l_tip = 3.0
r_tip = 1.0

# Insulator (Ceramic section)
l_ins_cyl = 3.0
l_ins_taper = 12.0
r_ins_start = 2.2
r_ins_end = 3.2

# Washer Seat (Narrow section under washer)
l_seat = 5.0
r_seat = 3.6

# Main Body (Metal Shell)
l_body = 18.0
r_body = 5.8  # Approx 12mm diameter

# Ribbed/Threaded Section
l_ribs = 14.0
r_ribs = 4.8

# Terminal (Connector end)
l_term = 10.0
r_term = 3.0

# Washer
r_washer_od = 9.5
r_washer_id = 3.7
washer_th = 1.0

# --- Construction ---

# 1. Tip: Create the initial cylinder along the X axis
result = cq.Workplane("YZ").circle(r_tip).extrude(l_tip)

# 2. Insulator Start: Cylindrical section
result = result.faces(">X").workplane().circle(r_ins_start).extrude(l_ins_cyl)

# 3. Insulator Taper: Loft from start radius to end radius
result = (result.faces(">X").workplane()
          .circle(r_ins_start)
          .workplane(offset=l_ins_taper)
          .circle(r_ins_end)
          .loft(combine=True))

# 4. Washer Seat
result = result.faces(">X").workplane().circle(r_seat).extrude(l_seat)

# 5. Main Body: Step up to larger diameter
result = result.faces(">X").workplane().circle(r_body).extrude(l_body)

# 6. Ribbed Section: Step down
result = result.faces(">X").workplane().circle(r_ribs).extrude(l_ribs)

# 7. Terminal: Further step down
result = result.faces(">X").workplane().circle(r_term).extrude(l_term)

# --- Feature Refinement ---

# Calculate X positions for feature placement
x_washer = l_tip + l_ins_cyl + l_ins_taper + l_seat - washer_th - 0.5
x_body_start = l_tip + l_ins_cyl + l_ins_taper + l_seat
x_rib_start = x_body_start + l_body
x_term_start = x_rib_start + l_ribs

# A. Create and Union the Washer
washer = (cq.Workplane("YZ")
          .workplane(offset=x_washer)
          .circle(r_washer_od)
          .circle(r_washer_id)
          .extrude(washer_th))
result = result.union(washer)

# B. Cut Ribs (Simulating threads/grooves)
# Create 5 rounded grooves along the ribbed section
for i in range(5):
    groove_center_x = x_rib_start + 2.0 + (i * 2.4)
    # Define a cut profile in the XY plane and revolve it
    cutter = (cq.Workplane("XY")
              .moveTo(groove_center_x, r_ribs)
              .threePointArc((groove_center_x + 0.8, r_ribs - 0.5), 
                             (groove_center_x + 1.6, r_ribs))
              .close()
              .revolve(axisStart=(0,0,0), axisEnd=(1,0,0)))
    result = result.cut(cutter)

# C. Terminal Snap Groove
# Groove near the end of the terminal
groove_x = x_term_start + l_term - 3.5
term_cutter = (cq.Workplane("XY")
               .moveTo(groove_x, r_term)
               .lineTo(groove_x + 0.5, r_term - 0.8)
               .lineTo(groove_x + 1.5, r_term - 0.8)
               .lineTo(groove_x + 2.0, r_term)
               .close()
               .revolve(axisStart=(0,0,0), axisEnd=(1,0,0)))
result = result.cut(term_cutter)

# --- Fillets and Chamfers ---

# Tip rounding
result = result.edges("<X").fillet(0.5)

# Terminal end rounding
result = result.edges(">X").fillet(1.0)

# Smooth transition from Body down to Ribs
# Select the edge at the start of the rib section with the body radius
try:
    result = result.edges(cq.selectors.NearestToPointSelector((x_rib_start, r_body, 0))).fillet(1.0)
except:
    pass # Skip if selection fails due to geometry fusion nuances

# Smooth transition from Seat to Body (Concave fillet)
# Select the inner corner where seat meets body
try:
    result = result.edges(cq.selectors.NearestToPointSelector((x_body_start, r_seat, 0))).fillet(0.5)
except:
    pass
