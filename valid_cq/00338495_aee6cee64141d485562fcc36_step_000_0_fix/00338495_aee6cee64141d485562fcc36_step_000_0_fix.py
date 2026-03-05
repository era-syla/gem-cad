import cadquery as cq

# Bottom segment: elliptical prism
base = cq.Workplane("XY").ellipse(15, 10).extrude(10)

# Middle segment: hexagonal prism
mid = cq.Workplane("XY").workplane(offset=10).polygon(6, 20).extrude(15)

# Top segment: triangular tapered prism (pyramid-like)
top = cq.Workplane("XY").workplane(offset=25).polygon(3, 8).extrude(20, taper=-5)

# Combine all segments into final result
result = base.union(mid).union(top)