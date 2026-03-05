import cadquery as cq

# Parameters
L = 120        # total bar length
W = 10         # bar width
T = 3          # thickness
Rb = 12        # bulge radius at center
hole1 = 6      # diameter of central hole
hole2 = 4      # diameter of offset hole
hole2_offset = 30   # x offset for the smaller hole
end_tab_len = 6     # length of the tab on the right end
end_tab_w = 8       # width of that tab
hook_cut_dia = 8    # diameter of hook cut at left end
hook_cut_offset = 12  # distance from left end to hook cut center

# Main bar
bar = cq.Workplane("XY").box(L, W, T, centered=(True, True, False))

# Central bulge
bulge = cq.Workplane("XY").circle(Rb).extrude(T)

# Right-end tab
end_tab = (
    cq.Workplane("XY")
    .center(L/2 + end_tab_len/2, 0)
    .rect(end_tab_len, end_tab_w)
    .extrude(T)
)

# Combine solids
result = bar.union(bulge).union(end_tab)

# Central hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(hole1/2)
    .cutThruAll()
)

# Offset hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole2_offset, 0)
    .circle(hole2/2)
    .cutThruAll()
)

# Hook cut at left end
hook_cut = (
    cq.Workplane("XY")
    .center(-L/2 + hook_cut_offset, 0)
    .circle(hook_cut_dia/2)
    .extrude(T + 1)
)
result = result.cut(hook_cut)