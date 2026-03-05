import cadquery as cq

# Main box dimensions
box_width = 60
box_depth = 50
box_height = 50
wall_thickness = 5

# Create the outer box
outer_box = cq.Workplane("XY").box(box_width, box_depth, box_height)

# Create inner cavity (open top box)
inner_width = box_width - 2 * wall_thickness
inner_depth = box_depth - 2 * wall_thickness
inner_height = box_height - wall_thickness  # open top, has bottom

inner_cavity = cq.Workplane("XY").box(inner_width, inner_depth, inner_height).translate((0, 0, wall_thickness))

# Subtract inner cavity from outer box
box_with_cavity = outer_box.cut(inner_cavity)

# Add a flange/lip on the back-top area
# The flange extends horizontally from the back top edge
flange_width = box_width + 10  # extends slightly on sides
flange_depth = 15
flange_thickness = wall_thickness

# Flange positioned at the top back
flange = (cq.Workplane("XY")
          .box(flange_width, flange_depth, flange_thickness)
          .translate((0, (box_depth + flange_depth) / 2 - flange_depth/2 + flange_depth/2, box_height/2 + flange_thickness/2))
         )

# Actually let's recalculate flange position
# Back of box is at y = box_depth/2
# Flange extends behind and at top
flange2 = (cq.Workplane("XY")
           .box(flange_width, flange_depth, flange_thickness)
          )

# Position flange at top back
# Center of flange in Y: box_depth/2 + flange_depth/2 - small overlap
flange_y = box_depth/2 - flange_depth/2 + 2  # slight overlap with back wall
flange_z = box_height/2 + flange_thickness/2

flange_positioned = flange2.translate((0, flange_y, flange_z))

# Now cut the notch on the left side of the flange area
# Looking at image: there's a rectangular notch cut from the top-left corner area
# The notch appears to cut into the left front area of the top

# Combine box with cavity and flange
combined = box_with_cavity.union(flange_positioned)

# Cut a notch from the top-left front area
# The notch is a rectangular cutout on the top-left
notch_width = box_width / 2
notch_depth = box_depth / 2
notch_height = wall_thickness + 2

notch = (cq.Workplane("XY")
         .box(notch_width, notch_depth, notch_height)
         .translate((-box_width/4, -box_depth/4 - notch_depth/4 + 2, box_height/2 + notch_height/2 - 1))
        )

result = combined.cut(notch)