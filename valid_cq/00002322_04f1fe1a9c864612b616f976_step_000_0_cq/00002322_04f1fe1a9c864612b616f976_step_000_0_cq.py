import cadquery as cq

# --- Parameter Definitions ---

# Panel 1 (Pegboard) parameters
panel1_width = 400.0
panel1_height = 400.0
panel1_thickness = 15.0
hole_spacing_x = 50.0
hole_spacing_y = 50.0
hole_diameter = 5.0
hole_margin = 25.0

# Panel 2 (Solid Backing) parameters
panel2_width = 400.0
panel2_height = 500.0
panel2_thickness = 15.0

# Bracket Assembly parameters
bracket_base_w = 60.0
bracket_base_h = 80.0
bracket_thickness = 3.0
bracket_flange_length = 40.0

main_bracket_height = 180.0
main_bracket_width = 80.0
main_bracket_depth = 80.0  # Width of the side flanges
main_bracket_thickness = 3.0

rod_length = 300.0
rod_diameter = 4.0

# --- Geometry Construction ---

# 1. Create the Pegboard Panel
# Calculate grid points
nx = int((panel1_width - 2 * hole_margin) / hole_spacing_x) + 1
ny = int((panel1_height - 2 * hole_margin) / hole_spacing_y) + 1

pts = []
for i in range(nx):
    for j in range(ny):
        x = -panel1_width/2 + hole_margin + i * hole_spacing_x
        y = -panel1_height/2 + hole_margin + j * hole_spacing_y
        pts.append((x, y))

panel1 = (cq.Workplane("XY")
          .box(panel1_width, panel1_height, panel1_thickness)
          .faces(">Z").workplane()
          .pushPoints(pts)
          .hole(hole_diameter)
          )

# 2. Create the Solid Backing Panel
# Positioned slightly behind/offset from the first panel to match exploded view
panel2 = (cq.Workplane("XY")
          .box(panel2_width, panel2_height, panel2_thickness)
          .translate((150, 50, 0)) # Offset position
          )

# 3. Create the Small Mounting Bracket
# Simple L-bracket or U-bracket shape based on image
small_bracket = (cq.Workplane("XY")
                 .box(bracket_base_w, bracket_base_h, bracket_thickness)
                 .faces(">Z").workplane()
                 # Add some mounting holes
                 .pushPoints([(-15, 20), (15, 20), (-15, -20), (15, -20)])
                 .hole(4.0)
                 # Add a perpendicular flange
                 .faces("<X").workplane()
                 .center(0, 0)
                 .rect(bracket_thickness, bracket_base_h)
                 .extrude(bracket_flange_length)
                 .translate((300, 100, 50)) # Position in exploded view
                 )

# 4. Create the Main Triangular Bracket
# This looks like a large folded sheet metal part or two triangular plates
# We will model the side profile and extrude/shell or combine plates.

# Side plate 1
p1 = (0, 0)
p2 = (main_bracket_depth, 0)
p3 = (0, main_bracket_height)
main_bracket_side = (cq.Workplane("YZ")
                     .polyline([p1, p2, p3, p1]).close()
                     .extrude(main_bracket_thickness)
                     )
# Add holes to side plate
main_bracket_side = (main_bracket_side
                     .faces(">X").workplane()
                     .pushPoints([(20, 40), (20, 80), (20, 120), (40, 40)])
                     .hole(6.0)
                     )

# Duplicate for the other side
main_bracket_side2 = main_bracket_side.translate((main_bracket_width, 0, 0))

# Back plate connecting them
back_plate = (cq.Workplane("XY")
              .box(main_bracket_width + main_bracket_thickness, 
                   main_bracket_thickness, 
                   main_bracket_height)
              .translate((main_bracket_width/2, -main_bracket_thickness/2, main_bracket_height/2))
              )

main_bracket_assy = (main_bracket_side
                     .union(main_bracket_side2)
                     .union(back_plate)
                     .rotate((0,0,0), (0,0,1), 90) # Rotate to face correct way
                     .translate((450, 100, 0)) # Position in exploded view
                     )

# 5. Create the Rod
rod = (cq.Workplane("XY")
       .circle(rod_diameter/2)
       .extrude(rod_length)
       .rotate((0,0,0), (0,1,0), 90) # Horizontal
       .translate((250, 100, 80))
       )

# 6. Small components (nuts/washers/spacers inferred from dots)
spacer = (cq.Workplane("XY")
          .circle(5)
          .circle(2.5)
          .extrude(5)
          .rotate((0,0,0), (0,1,0), 90)
          .translate((400, 100, 80))
          )
          
block = (cq.Workplane("XY")
         .box(20, 30, 10)
         .faces(">Z").workplane().hole(4)
         .rotate((0,0,0), (0,0,1), 90)
         .translate((380, 120, 50))
         )


# --- Assembly ---

# Combine all distinct parts into one result for visualization
# Note: In a real assembly, these would be separate objects in an Assembly class,
# but 'result' usually expects a single compound or object for simple scripts.
result = (panel1
          .union(panel2)
          .union(small_bracket)
          .union(main_bracket_assy)
          .union(rod)
          .union(spacer)
          .union(block)
          )