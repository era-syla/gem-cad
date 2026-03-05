import cadquery as cq

# --- Parameter Definitions ---
# Main body dimensions
main_cyl_diameter = 60.0
main_cyl_height = 25.0
main_wall_thickness = 2.0

# Air outlet (square protrusion at bottom)
outlet_width = 20.0
outlet_length = 15.0  # Extension from cylinder
outlet_height = 25.0  # Matches cylinder height

# Motor mount / Intake section (upper left)
intake_cyl_outer_diam = 28.0
intake_cyl_inner_diam = 24.0
intake_length = 35.0
intake_offset_y = 35.0 # Distance from main center to intake center

# Mounting flange (top)
flange_width = 30.0
flange_height = 35.0
flange_thickness = 4.0
flange_angle = 45.0 # Angle of the top flange

# Mounting holes and bosses
boss_diam = 8.0
boss_hole_diam = 3.5

# Clip/feature details on the side
clip_width = 10.0
clip_protrusion = 5.0

# --- Geometry Construction ---

# 1. Main Blower Housing (The large cylinder)
# Create the base cylinder
housing_outer = cq.Workplane("XY").circle(main_cyl_diameter/2).extrude(main_cyl_height)

# Create the outlet extension (tangent to cylinder)
# Position a rectangle so it merges tangentially for a blower shape
outlet = (cq.Workplane("XY")
          .center(main_cyl_diameter/4, -main_cyl_diameter/2) # Approximate positioning
          .rect(main_cyl_diameter/2 + outlet_length, outlet_width)
          .extrude(main_cyl_height))

# Combine housing and outlet
main_body = housing_outer.union(outlet)

# Shelling the main body (hollow inside)
# We select the top face to be open, or just shell inwards. 
# Looking at the image, it seems like a 2-part assembly. This part is a cover.
# Let's shell it inwards leaving the top face (Z-max) open? 
# No, the image shows a solid-looking cover with an intake tube attached.
# Let's assume a uniform wall thickness for the main cavity.
main_body_hollow = main_body.faces("<Z").shell(-main_wall_thickness)

# 2. Intake Tube (Vertical cylinder on the side)
# This sits "behind" or offset from the main spiral
intake = (cq.Workplane("YZ")
          .workplane(offset=-main_cyl_diameter/2 + 5) # Shift to side
          .center(intake_offset_y, main_cyl_height/2)
          .circle(intake_cyl_outer_diam/2)
          .extrude(intake_length + 10)) # Extrude out

# Hollow out the intake
intake_hole = (cq.Workplane("YZ")
               .workplane(offset=-main_cyl_diameter/2 + 5 - 1)
               .center(intake_offset_y, main_cyl_height/2)
               .circle(intake_cyl_inner_diam/2)
               .extrude(intake_length + 20))

intake_structure = intake.cut(intake_hole)

# 3. Transition/Top Structure (Connecting intake to main body and flange)
# Create a block that connects the top of the main housing to the intake area
transition_block = (cq.Workplane("XY")
                    .center(0, intake_offset_y/2)
                    .rect(main_cyl_diameter/2, intake_offset_y)
                    .extrude(main_cyl_height))

# 4. Top Mounting Flange
# Angled plane for the top bracket
flange = (cq.Workplane("XY")
          .workplane(offset=main_cyl_height/2)
          .center(-10, intake_offset_y + 15)
          .box(flange_width, 5, flange_height) # Rough vertical plate
          .rotateAboutCenter((1,0,0), -30) # Tilt it
          )

# Add ribs to the flange
rib1 = (cq.Workplane("XY")
        .center(-5, intake_offset_y + 5)
        .rect(2, 20)
        .extrude(main_cyl_height + 15)
        )
        
rib2 = (cq.Workplane("XY")
        .center(-15, intake_offset_y + 5)
        .rect(2, 20)
        .extrude(main_cyl_height + 10)
        )

# 5. Mounting Bosses
# Boss 1: Near the outlet/bottom right
boss1 = (cq.Workplane("XY")
         .center(main_cyl_diameter/2 - 5, -main_cyl_diameter/2 + 5)
         .circle(boss_diam/2)
         .extrude(main_cyl_height))
boss1_hole = (cq.Workplane("XY")
         .center(main_cyl_diameter/2 - 5, -main_cyl_diameter/2 + 5)
         .circle(boss_hole_diam/2)
         .extrude(main_cyl_height))

# Boss 2: Near the intake junction
boss2 = (cq.Workplane("XY")
         .center(-main_cyl_diameter/4, 20)
         .circle(boss_diam/2)
         .extrude(main_cyl_height))
boss2_hole = (cq.Workplane("XY")
          .center(-main_cyl_diameter/4, 20)
          .circle(boss_hole_diam/2)
          .extrude(main_cyl_height))
          
# 6. Clip Feature on the back of intake
clip = (cq.Workplane("YZ")
        .workplane(offset=0)
        .center(intake_offset_y - 10, main_cyl_height/2)
        .rect(10, 8)
        .extrude(15))
        
clip_slot = (cq.Workplane("YZ")
        .workplane(offset=0)
        .center(intake_offset_y - 10, main_cyl_height/2)
        .rect(12, 2)
        .extrude(15))

clip_final = clip.cut(clip_slot)

# --- Assembly/Union Operations ---

# Start combining pieces
part = main_body_hollow.union(intake_structure)
part = part.union(transition_block)
part = part.union(flange)
part = part.union(rib1).union(rib2)
part = part.union(boss1).cut(boss1_hole)
part = part.union(boss2).cut(boss2_hole)
part = part.union(clip_final)

# Refine shapes (Cut off excess to match the visual style)
# Cut the intake area to reveal the semi-circle shape at the bottom
cut_cyl = (cq.Workplane("YZ")
           .workplane(offset=-20)
           .center(intake_offset_y, main_cyl_height/2)
           .circle(intake_cyl_outer_diam/2)
           .extrude(50))
           
# Create a complex cut to shape the "half-pipe" look on the left
trim_box = (cq.Workplane("XY")
            .center(-main_cyl_diameter, 0)
            .box(main_cyl_diameter, 100, 100))
            
part = part.cut(trim_box)

# Add back the half-pipe bottom part of the intake which was just trimmed
intake_lower_shell = (cq.Workplane("YZ")
          .workplane(offset=-15)
          .center(intake_offset_y - 20, main_cyl_height/2) # Shifted down
          .circle(intake_cyl_outer_diam/2)
          .extrude(15)
          ).faces(">X").shell(-2)

part = part.union(intake_lower_shell)


# Filleting edges for realistic look
try:
    part = part.edges("|Z").fillet(1.0)
except:
    pass # Fillets can be fragile on complex unions

# Final result assignment
result = part