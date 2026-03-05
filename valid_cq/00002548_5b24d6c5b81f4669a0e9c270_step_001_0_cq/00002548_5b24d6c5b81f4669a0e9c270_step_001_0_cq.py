import cadquery as cq

# --- Parametric Dimensions (based on standard AA battery) ---
battery_diameter = 14.5
battery_height = 50.5  # Total height including nub
nub_diameter = 5.5
nub_height = 1.0
casing_thickness = 0.5 # For the visual groove detail

# Derived dimensions
main_body_height = battery_height - nub_height
negative_terminal_inset = 0.2  # Slight inset for realism on the bottom
positive_terminal_shoulder_width = 1.0 # Width of the raised ring around the nub
groove_depth = 0.2
groove_width = 0.5

# --- Modeling ---

# 1. Create the main cylindrical body
main_body = cq.Workplane("XY").circle(battery_diameter / 2).extrude(main_body_height)

# 2. Create the positive terminal (the nub)
# We select the top face and extrude a smaller circle
nub = (main_body.faces(">Z").workplane()
       .circle(nub_diameter / 2)
       .extrude(nub_height))

# 3. Create the characteristic crimp/shoulder detail on the positive end
# This is often a slight depression or ring around the nub
shoulder_cut = (nub.faces("<Z").workplane(offset=-0.1) # Start slightly below the very top edge of the main body
                .circle(battery_diameter / 2 - 0.5)
                .circle(nub_diameter / 2 + 1.0)
                .extrude(-0.3, combine='cut')) # Cut a shallow ring

# 4. Create the negative terminal (bottom)
# Usually a slightly indented flat area or just a flat surface. 
# Let's add a small chamfer/fillet to the bottom edge for realism
result = shoulder_cut.edges("<Z").fillet(0.5)

# 5. Add a small groove near the top (positive end) to simulate the crimped casing
# This is a common feature on alkaline batteries
groove = (result.faces(">Z").workplane(offset=-1.5) # Position slightly down from top
          .circle(battery_diameter / 2)
          .circle(battery_diameter / 2 - groove_depth)
          .extrude(-groove_width, combine='cut'))

# 6. Refine the positive nub
# Add a small fillet to the top of the nub
result = groove.edges(">Z").fillet(0.2)

# Final result assignment
result = result