import cadquery as cq

# Main box dimensions
box_w = 80
box_d = 40
box_h = 50
wall = 3

# Create the main outer box (open top)
outer_box = cq.Workplane("XY").box(box_w, box_d, box_h, centered=(True, True, False))

# Create inner cutout (hollow the box from top)
inner_box = cq.Workplane("XY").box(
    box_w - 2*wall, box_d - 2*wall, box_h - wall,
    centered=(True, True, False)
).translate((0, 0, wall))

result = outer_box.cut(inner_box)

# Add two cylindrical bumps/indentations inside the box
# Two side-by-side rounded indentations visible from the top interior
cyl_r = (box_w - 2*wall) / 4.0
cyl_h = box_h - wall

# Left cylinder indentation
left_cyl = cq.Workplane("XY").cylinder(cyl_h, cyl_r).translate((-cyl_r, 0, wall + cyl_h/2))
# Right cylinder indentation  
right_cyl = cq.Workplane("XY").cylinder(cyl_h, cyl_r).translate((cyl_r, 0, wall + cyl_h/2))

# Cut the cylindrical shapes from inside to create the curved interior walls
result = result.cut(left_cyl).cut(right_cyl)

# Add a vertical fin/tab on the front-bottom (the flat panel sticking out below)
# This appears as a flat rectangular plate on the front face extending downward
fin_w = 20
fin_h = 35
fin_d = wall

fin = cq.Workplane("XY").box(fin_w, fin_d, fin_h, centered=(True, True, False))
fin = fin.translate((0, -(box_d/2 + fin_d/2 - fin_d), -fin_h))

# Actually position fin at front face going down
fin = (cq.Workplane("XY")
       .box(fin_w, fin_d, fin_h, centered=(True, True, False))
       .translate((0, -(box_d/2), -fin_h)))

result = result.union(fin)

# Add a small rounded protrusion/tab on the right side (connector tab)
tab_w = wall
tab_d = 20
tab_h = 20

tab = (cq.Workplane("XY")
       .box(tab_w, tab_d, tab_h, centered=(True, True, False))
       .translate((box_w/2, -tab_d/2 + box_d/4, 0)))

result = result.union(tab)

# Add cylinder tab on right side bottom
cyl_tab_r = 8
cyl_tab_h = 15
cyl_tab = (cq.Workplane("XY")
           .cylinder(cyl_tab_h, cyl_tab_r)
           .translate((box_w/2 + cyl_tab_r, 0, cyl_tab_h/2)))

result = result.union(cyl_tab)