import cadquery as cq

# Create a puzzle piece shape
# Base dimensions
w = 60
h = 60
t = 8  # thickness

# Tab size
tab_r = 8
tab_offset = 0

# Create the base square
base = cq.Workplane("XY").rect(w, h).extrude(t)

# Add tabs on each side (bumps)
# Top tab
top_tab = (cq.Workplane("XY")
           .transformed(offset=(0, h/2, 0))
           .circle(tab_r)
           .extrude(t))

# Bottom tab (indent - we'll subtract)
bottom_tab = (cq.Workplane("XY")
              .transformed(offset=(0, -h/2, 0))
              .circle(tab_r)
              .extrude(t))

# Right tab
right_tab = (cq.Workplane("XY")
             .transformed(offset=(w/2, 0, 0))
             .circle(tab_r)
             .extrude(t))

# Left tab (indent)
left_tab = (cq.Workplane("XY")
            .transformed(offset=(-w/2, 0, 0))
            .circle(tab_r)
            .extrude(t))

# Combine: add top and right tabs, subtract bottom and left tabs
result = (base
          .union(top_tab)
          .union(right_tab)
          .cut(bottom_tab)
          .cut(left_tab))