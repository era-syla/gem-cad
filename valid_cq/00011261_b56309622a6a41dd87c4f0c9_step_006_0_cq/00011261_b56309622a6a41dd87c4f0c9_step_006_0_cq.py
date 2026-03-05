import cadquery as cq

# --- Parametric Definitions ---
# Main body dimensions
main_diameter = 40.0
main_height = 12.0

# Chamfer at the top edge
top_chamfer = 2.0

# Top recessed area (creating the raised rim)
rim_thickness = 1.0  # Width of the rim at the top
recess_depth = 0.5   # How deep the main top face is recessed relative to the rim

# Central feature (button/boss)
center_boss_diameter = 16.0
center_boss_height = 0.5  # Height relative to the recessed surface

# Bottom feature (visible as a smaller cylinder protruding from the bottom)
bottom_boss_diameter = 15.0
bottom_boss_height = 3.0

# --- Modeling ---

# 1. Create the main cylindrical body
main_body = cq.Workplane("XY").circle(main_diameter / 2).extrude(main_height)

# 2. Create the bottom boss
# We select the bottom face ("<Z") and extrude downwards
result = (main_body
          .faces("<Z")
          .workplane()
          .circle(bottom_boss_diameter / 2)
          .extrude(bottom_boss_height)
         )

# 3. Create the top chamfer
# Select the top edge of the main cylinder
result = result.edges(cq.selectors.RadiusNthSelector(1)).chamfer(top_chamfer)

# 4. Create the recessed top face to form the rim
# We cut a pocket into the top, leaving a rim
# The cut diameter needs to account for the chamfer geometry effectively
# The chamfer reduces the top diameter. 
# Original Radius = 20. Chamfer = 2. Top Radius = 18.
# We want a thin rim, so let's cut inside that.
current_top_radius = (main_diameter / 2) - top_chamfer
cut_radius = current_top_radius - rim_thickness

result = (result
          .faces(">Z")
          .workplane()
          .circle(cut_radius)
          .cutBlind(-recess_depth)
         )

# 5. Create the central boss
# We select the newly created recessed face and extrude up
result = (result
          .faces(">Z[1]") # Select the recessed face (should be the second highest Z face now)
          .workplane()
          .circle(center_boss_diameter / 2)
          .extrude(center_boss_height)
         )

# If the center boss is meant to be flush with the rim or slightly raised/lowered,
# the extrusion height can be adjusted. Visually, it looks slightly raised 
# above the recess but possibly flush or slightly below the outer rim height.
# The current parameters put it 0.5mm above the recess floor.

# Refine geometry with fillets if necessary (image shows mostly sharp or chamfered edges)
# The image shows a subtle groove or step around the center boss, 
# which is achieved by the extrusion from the recessed face.

# Final check of the 'result' variable
# The code produces:
# 1. Bottom cylinder
# 2. Main cylinder on top of it
# 3. Chamfered top edge
# 4. Recessed face leaving a rim
# 5. Center boss rising from the recess