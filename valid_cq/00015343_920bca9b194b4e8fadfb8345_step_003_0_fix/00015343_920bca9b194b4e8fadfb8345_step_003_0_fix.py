import cadquery as cq

L = 80    # total length of top plate
W = 20    # width of top plate
t = 5     # thickness of top plate
h_below = 20  # total support height below top plate
floor_t = 3   # thickness of bottom floor under cavity
r = W/2       # radius of semicircle on left
cavity_start = 40           # x position where cavity begins
cavity_length = L - cavity_start

# Top plate with semicircular left end
top = (
    cq.Workplane("XY")
      .polyline([(r, W/2), (L, W/2), (L, -W/2), (r, -W/2)])
      .threePointArc((0, 0), (r, W/2))
      .close()
      .extrude(t)
)

# Solid support block under the right rectangular portion of the top
base = (
    cq.Workplane("XY")
      .rect(L - r, W)
      .extrude(-h_below)
      .translate(((r + L) / 2, 0, 0))
)

# Rectangular cavity cut under the right side, leaving a floor of thickness floor_t
cavity = (
    cq.Workplane("XY")
      .transformed(offset=((cavity_start + L) / 2, 0, t))
      .rect(cavity_length, W - 2 * floor_t)
      .extrude(-(h_below - floor_t))
)

result = top.union(base).cut(cavity)