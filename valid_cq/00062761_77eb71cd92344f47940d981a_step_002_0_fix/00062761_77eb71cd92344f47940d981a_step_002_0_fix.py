import cadquery as cq

# Dimensions and initial setup
width = 20
length = 100
height = 20
flange_width = 5
hole_diameter = 2
hole_space = 20
tab_width = 10
tab_height = 2

# Create base plate
base = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))

# Create side flanges
flange1 = (cq.Workplane("XY")
           .transformed(offset=(length/2, 0, height/2), rotate=(0, 30, 0))
           .box(height, width, flange_width, centered=(True, True, False)))

flange2 = (cq.Workplane("XY")
           .transformed(offset=(-length/2, 0, height/2), rotate=(0, 30, 0))
           .box(height, width, flange_width, centered=(True, True, False)))

# Create top tabs
tab1 = (cq.Workplane("XY")
        .transformed(offset=(0, width/2, height + tab_height/2))
        .box(tab_width, tab_height, flange_width, centered=(True, True, False)))

tab2 = (cq.Workplane("XY")
        .transformed(offset=(0, -width/2, height + tab_height/2))
        .box(tab_width, tab_height, flange_width, centered=(True, True, False)))

# Create holes in side flanges
holes = (cq.Workplane("XY")
         .rarray(hole_space, 1, 2, 1)
         .circle(hole_diameter/2)
         .extrude(flange_width))

flange1 = flange1.cut(holes)
flange2 = flange2.cut(holes)

# Combine all parts together
result = base.union(flange1).union(flange2).union(tab1).union(tab2)