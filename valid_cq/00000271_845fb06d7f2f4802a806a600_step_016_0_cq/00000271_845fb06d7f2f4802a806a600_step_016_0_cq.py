import cadquery as cq

# Parametric dimensions
total_length = 50.0  # Estimated total length
hex_head_flat_to_flat = 19.0  # Estimated hex size (like a standard M12 or M14 bolt head)
hex_head_height = 6.0   # Thickness of the hex head

# Main body sections (moving from hex head to tip)
shank_diameter_large = 12.0 # The main cylindrical section
shank_length_large = 25.0

shoulder_diameter = 14.0 # The slightly wider section near the head
shoulder_length = 6.0
shoulder_chamfer = 1.0   # Chamfer connecting shoulder to shank

tip_diameter = 10.0     # The reduced diameter at the end
tip_length = 13.0       # Remaining length

# Groove details (near the tip)
groove_width = 2.0
groove_depth = 1.0
groove_pos_from_tip = 4.0 # Distance from the very end face to the start of the groove

# Central bore (hole through the center)
bore_diameter = 5.0

# Construction

# 1. Create the Hex Head
# We start by drawing a hexagon and extruding it
head = (cq.Workplane("XY")
        .polygon(6, hex_head_flat_to_flat * 1.1547) # 1.1547 factor converts flat-to-flat to diameter
        .extrude(hex_head_height)
       )

# 2. Add the Shoulder (widest cylindrical part near head)
# We select the top face of the hex head and extrude
shoulder = (head.faces(">Z")
            .circle(shoulder_diameter / 2.0)
            .extrude(shoulder_length)
           )

# 3. Add the Main Shank
# Extrude from the shoulder
shank = (shoulder.faces(">Z")
         .circle(shank_diameter_large / 2.0)
         .extrude(shank_length_large)
        )

# 4. Add the Tip Section
# Extrude from the shank
tip = (shank.faces(">Z")
       .circle(tip_diameter / 2.0)
       .extrude(tip_length)
      )

# 5. Add the Groove
# We create a cutting profile. Since we are building up, we can just cut a ring.
# We need to locate the plane relative to the start of the tip.
# Total height so far = hex_head_height + shoulder_length + shank_length_large
current_z = hex_head_height + shoulder_length + shank_length_large
groove_z_center = current_z + tip_length - groove_pos_from_tip - (groove_width / 2.0)

# Create a temporary solid to cut the groove
# Or simpler: Select the face at the specific Z height and cut
# Let's use the workplane offset method for clarity
part_with_groove = (tip.faces(">Z")
                    .workplane(offset = -(groove_pos_from_tip + groove_width))
                    .circle(tip_diameter / 2.0) # Outer boundary of cut
                    .circle((tip_diameter / 2.0) - groove_depth) # Inner boundary of cut
                    .extrude(groove_width, combine="cut") # Cut inward (or rather, cut the ring shape)
                    # Actually, extrude(combine='cut') with two circles creates a ring cut
                   )
                   
# 6. Add the Central Bore
# Cut a hole through the entire assembly
final_shape = (part_with_groove.faces("<Z") # Select bottom of hex head
               .circle(bore_diameter / 2.0)
               .cutBlind(-1000) # Cut all the way through (negative direction relative to face normal)
              )

# 7. Add Chamfers/Fillets for realism
# Chamfer between Shoulder and Main Shank
# We need to select the edge at the transition.
# The transition is at Z = hex_head_height + shoulder_length
transition_z = hex_head_height + shoulder_length
result = final_shape.edges(cq.selectors.NearestToPointSelector((0, 0, transition_z))).chamfer(0.5)

# Chamfer at the very tip
result = result.edges(">Z").chamfer(0.5)

# Slight fillet on the groove edges? Optional, but good for machining.
# Let's add a small chamfer to the hex head top for standard bolt look
result = result.edges(cq.selectors.BoxSelector(
    (-100, -100, hex_head_height - 0.1), 
    (100, 100, hex_head_height + 0.1)
)).chamfer(0.5)

# Optional: Washer face underneath the hex head (a small circular protrusion often found on bolts)
# This is implied by the image where the hex meets the cylinder, usually there's a small boss.
# We'll skip adding extra geometry to keep it clean, but ensure the connection is solid.

# Assign to result variable
result = result