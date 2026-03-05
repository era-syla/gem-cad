import cadquery as cq

# Central body by revolving an outer profile and subtracting an inner profile
outer_profile = [(0, 0), (15, 0), (20, 8), (15, 16), (10, 18), (0, 18)]
inner_profile = [(0, 2), (13, 2), (18, 8), (13, 14), (8, 16), (0, 16)]

outer = (
    cq.Workplane("XZ")
    .polyline(outer_profile)
    .close()
    .revolve(360)
)

inner = (
    cq.Workplane("XZ")
    .polyline(inner_profile)
    .close()
    .revolve(360)
)

body = outer.cut(inner)

# Single fin profile extruded in Z
fin_2d = [(13, 2), (30, 10), (30, -10), (13, -2)]
fin = (
    cq.Workplane("XY")
    .polyline(fin_2d)
    .close()
    .extrude(18)
)

# Create three fins by rotating the first one
fin1 = fin
fin2 = fin1.rotate((0, 0, 0), (0, 0, 1), 120)
fin3 = fin1.rotate((0, 0, 0), (0, 0, 1), 240)

# Combine body and fins, then apply edge fillets
result = (
    body
    .union(fin1)
    .union(fin2)
    .union(fin3)
    .edges("|Z")
    .fillet(1)
)