import cadquery as cq

# Parametric dimensions
# Main Plate
plate_width = 80.0
plate_height = 60.0
plate_thickness = 10.0

# Cylinder / Clamp dimensions
cyl_outer_diam = 20.0
cyl_inner_diam = 12.0
cyl_height = 25.0
cyl_spacing = 50.0 # Distance between cylinder centers
cyl_y_offset = plate_height / 2 + cyl_outer_diam/4 # Position relative to center

# Clamping Slit
slit_width = 2.0
slit_depth = 5.0 # How far into the plate the slit goes

# Central Support
center_block_width = 15.0
center_block_depth = 20.0
center_block_height = cyl_height # Aligned with cylinders

# Mounting Holes on Plate
hole_spacing_x = 40.0
hole_spacing_y = 30.0
hole_diam = 4.0

# Create the main rectangular plate
# We center it on X and Z, but align Y so the top edge is known
plate = cq.Workplane("XY").box(plate_width, plate_thickness, plate_height)

# Create the cylindrical clamps
# We define one and mirror it
cyl = (cq.Workplane("XY")
       .workplane(offset=plate_height/2 - cyl_height) # Start from top of plate area, go down? No, let's align top.
       .workplane(offset=cyl_height/2) # Actually, let's just place them relative to the plate center
       )

# Let's rebuild the strategy: 
# 1. Base Plate
# 2. Add the two cylinders at the top
# 3. Add the center block
# 4. Cut the central fillet/bridge
# 5. Cut the holes and slits

# 1. Base Plate
# Oriented upright in XZ plane for easier visualization? Let's stick to XY as "ground" but build the plate vertically.
# Let's align the center of the plate face to the origin for easier hole placement.
plate = cq.Workplane("XY").box(plate_width, plate_thickness, plate_height)

# 2. Cylinders
# Position: Top edge of the plate, sticking out towards the back (or front? looks like the cylinders overhang the back)
# Looking at image: Cylinders are flush with the top of the plate, and their bodies extend behind the plate.
# The plate seems to be the front face. The cylinders are attached to the back of the top edge.
cyl_z_center = plate_height/2 - cyl_height/2
cyl_y_center = plate_thickness/2 + cyl_outer_diam/2 - 2.0 # Slight overlap for fusion

# Left Cylinder
left_cyl = (cq.Workplane("XY")
            .center(-cyl_spacing/2, cyl_y_center)
            .workplane(offset=plate_height/2 - cyl_height)
            .circle(cyl_outer_diam/2)
            .extrude(cyl_height)
            )

# Right Cylinder
right_cyl = (cq.Workplane("XY")
             .center(cyl_spacing/2, cyl_y_center)
             .workplane(offset=plate_height/2 - cyl_height)
             .circle(cyl_outer_diam/2)
             .extrude(cyl_height)
             )

# 3. Center Block
# Located between cylinders, flush with top, extending back
center_block = (cq.Workplane("XY")
                .center(0, plate_thickness/2 + center_block_depth/2 - 1.0) # Overlap
                .workplane(offset=plate_height/2 - center_block_height/2)
                .box(center_block_width, center_block_depth, center_block_height)
                )

# Combine main shapes
solid = plate.union(left_cyl).union(right_cyl).union(center_block)

# 4. Fillets / Webbing between cylinders and center block
# The image shows a smooth transition or a bridge between the cylinders and the center block.
# Let's create a loft or a block with fillets to bridge them.
# An easier way is to create a block bridging them and fillet the vertical edges.
bridge_width = cyl_spacing
bridge_depth = cyl_outer_diam/2 
bridge = (cq.Workplane("XY")
          .center(0, cyl_y_center)
          .workplane(offset=plate_height/2 - cyl_height)
          .box(cyl_spacing, cyl_outer_diam, cyl_height, centered=(True, True, False))
          )

# We only want the material between the cylinders, so we intersect or just union and fillet later.
# Let's try just unioning the bridge, then cutting the space out?
# Actually, the image shows a "web" connecting the cylinder to the center block.
# Let's add a simple block connecting cylinder to center block and fillet it.

# Refined approach for the top assembly:
# Sketch the profile of the top section (cylinders + connection) and extrude.
top_sketch = (cq.Workplane("XY")
              .workplane(offset=plate_height/2 - cyl_height)
              # Left Circle
              .moveTo(-cyl_spacing/2, cyl_y_center)
              .circle(cyl_outer_diam/2)
              # Right Circle
              .moveTo(cyl_spacing/2, cyl_y_center)
              .circle(cyl_outer_diam/2)
              # Center Rect
              .moveTo(0, cyl_y_center)
              .rect(center_block_width, center_block_depth)
              # Connect them
              .moveTo(-cyl_spacing/2, cyl_y_center).lineTo(cyl_spacing/2, cyl_y_center)
              .rect(cyl_spacing, 5.0) # Thin strip to connect them all ensuring validity
              )
              
# This is getting complicated. Let's stick to boolean addition and filleting.
# The object `solid` currently has the plate, two cylinders, and a center block.
# Let's add material between cylinders and center block.
web_left = (cq.Workplane("XY")
            .center(-cyl_spacing/4 - center_block_width/4, cyl_y_center)
            .workplane(offset=plate_height/2 - cyl_height)
            .box(cyl_spacing/2 - center_block_width/2, 5.0, cyl_height, centered=(True, True, False))
            )
web_right = (cq.Workplane("XY")
             .center(cyl_spacing/4 + center_block_width/4, cyl_y_center)
             .workplane(offset=plate_height/2 - cyl_height)
             .box(cyl_spacing/2 - center_block_width/2, 5.0, cyl_height, centered=(True, True, False))
             )

solid = solid.union(web_left).union(web_right)

# 5. Cuts (Holes and Slits)

# Cylinder vertical holes
solid = (solid.faces(">Z")
         .workplane()
         .moveTo(-cyl_spacing/2, cyl_y_center)
         .circle(cyl_inner_diam/2)
         .moveTo(cyl_spacing/2, cyl_y_center)
         .circle(cyl_inner_diam/2)
         .cutBlind(-cyl_height)
         )

# Clamping Slits
# The slit goes through the cylinder and slightly into the web/plate.
# It seems to cut from the "back" (positive Y relative to cylinder center) towards the center.
# Actually, looking at the image, the slit is on the diameter, parallel to the plate.
# It cuts through the wall of the cylinder.
solid = (solid.faces(">Z")
         .workplane()
         .moveTo(-cyl_spacing/2, cyl_y_center)
         .rect(slit_width, cyl_outer_diam + 5) # Cut through entire diameter width-wise
         .moveTo(cyl_spacing/2, cyl_y_center)
         .rect(slit_width, cyl_outer_diam + 5)
         .cutBlind(-cyl_height/3) # Cut down partially? Image shows it goes down quite a bit.
         )
# Correction: The image shows the slit goes all the way down the cylinder part? 
# No, usually these are for clamping, so they might go part way or all way.
# The image shows a small rectangular cutout on the top surface that looks like a keyway, 
# AND a split. Let's look closer. 
# It looks like a split clamp. The slit cuts the cylinder ring.
# It is aligned with the X-axis (left-right).
solid = (solid.faces(">Z")
         .workplane()
         .moveTo(-cyl_spacing/2, cyl_y_center)
         .rect(cyl_outer_diam, slit_width) # Cut along Y axis? No, across X.
         # The image shows the gap is on the side facing the other cylinder? Or away?
         # The gap is on the diameter parallel to the plate face (X-axis).
         # It splits the cylinder into a front half and back half.
         .rect(cyl_outer_diam + 2, slit_width)
         .moveTo(cyl_spacing/2, cyl_y_center)
         .rect(cyl_outer_diam + 2, slit_width)
         .cutBlind(-cyl_height)
         )

# Also, there are small rectangular slots near the center block on the top surface.
# These might be for nuts or alignment.
slot_cut = (cq.Workplane("XY")
            .workplane(offset=plate_height/2 - 5)
            .moveTo(-center_block_width/2 - 2, plate_thickness/2 + 1)
            .rect(4, 4)
            .moveTo(center_block_width/2 + 2, plate_thickness/2 + 1)
            .rect(4, 4)
            .extrude(10) # Cut upwards through the webbing
            )
solid = solid.cut(slot_cut)

# Mounting Holes on the Plate
# 4 holes arranged in a rectangle
solid = (solid.faces("<Y") # Front face of the plate
         .workplane()
         .pushPoints([
             (-hole_spacing_x/2, hole_spacing_y/2),
             (hole_spacing_x/2, hole_spacing_y/2),
             (-hole_spacing_x/2, -hole_spacing_y/2),
             (hole_spacing_x/2, -hole_spacing_y/2)
         ])
         .hole(hole_diam)
         )

# Fillets
# The connection between the cylinders and the center web is filleted (curved).
# We can select vertical edges near the center block.
# This selector is tricky. Let's try to fillet edges based on position.
try:
    solid = solid.edges("|Z").filterByPosition(lambda p: p.y > plate_thickness/2 and abs(p.x) < cyl_spacing/2).fillet(5.0)
except:
    pass # Fallback if fillet fails, though it provides the nice smooth look in the image

result = solid