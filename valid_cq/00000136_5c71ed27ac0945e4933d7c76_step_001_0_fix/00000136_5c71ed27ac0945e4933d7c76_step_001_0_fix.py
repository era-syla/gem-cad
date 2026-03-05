import cadquery as cq

# Parameters
main_r = 10
main_len = 60
neck_r = 7.5
neck_len = 20
cap_len = neck_r
boss_r = 2
boss_len = 4

# 2D profile in X-Z plane
profile = (
    cq.Workplane("XZ")
    .moveTo(0, main_r)
    .lineTo(main_len, main_r)
    .lineTo(main_len, neck_r)
    .lineTo(main_len + neck_len, neck_r)
    .radiusArc((main_len + neck_len + cap_len, 0), cap_len)
    .lineTo(0, 0)
    .close()
)

# Revolve profile around X axis
body = profile.revolve(360)

# Add small boss at front
x_end = main_len + neck_len + cap_len
boss = (
    cq.Workplane("YZ", origin=(x_end, 0, 0))
    .circle(boss_r)
    .extrude(boss_len)
)

result = body.union(boss)