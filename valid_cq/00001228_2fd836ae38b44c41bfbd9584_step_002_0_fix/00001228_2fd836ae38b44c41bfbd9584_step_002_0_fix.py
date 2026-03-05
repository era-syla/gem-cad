import cadquery as cq

# Parameters
R = 25      # Base circle radius
T = 5       # Thickness of the disc and tabs
nTabs = 8   # Number of tabs
tabLength = 5  # Radial length of each tab
tabWidth = 8   # Tangential width of each tab

# Create the base disc
result = cq.Workplane("XY").circle(R).extrude(T)

# Add tabs around the perimeter
for i in range(nTabs):
    angle = 360.0 / nTabs * i
    tab = (
        cq.Workplane("XY")
        .transformed(offset=(R + tabLength / 2, 0, T / 2), rotate=(0, 0, angle))
        .box(tabLength, tabWidth, T)
    )
    result = result.union(tab)