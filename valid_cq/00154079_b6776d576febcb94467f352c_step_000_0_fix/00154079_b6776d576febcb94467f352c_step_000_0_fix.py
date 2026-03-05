import cadquery as cq

# Parameters
base_length = 200
base_width = 10
base_thickness = 2
tab_thickness = 3
tab_height = 20
lip_length = 5
lip_thickness = 2

# X positions for the three tabs (left, center, right)
tab_xs = [
    -base_length/2 + tab_thickness/2,
     0,
     base_length/2 - tab_thickness/2,
]

# Base plate
base = cq.Workplane("XY").rect(base_length, base_width).extrude(base_thickness)

result = base

# Create tabs and lips and union them into the result
for x in tab_xs:
    # Vertical tab
    tab = (
        cq.Workplane("XY")
        .transformed(offset=(x, 0, base_thickness))
        .rect(tab_thickness, base_width)
        .extrude(tab_height)
    )
    # Horizontal lip on the front (+Y) of the tab
    lip = (
        cq.Workplane("XZ")
        .transformed(offset=(x, base_width/2, base_thickness + tab_height))
        .rect(tab_thickness, lip_thickness)
        .extrude(lip_length)
    )
    result = result.union(tab).union(lip)