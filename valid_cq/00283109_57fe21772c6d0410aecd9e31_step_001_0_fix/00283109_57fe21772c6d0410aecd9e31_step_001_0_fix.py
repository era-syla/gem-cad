import cadquery as cq

L = 200
ch_root = 50
ch_tip = 15
height = 20
rib_thk = 2
bar_thk = 3
n_ribs = 10

def chord(x):
    return ch_root + (ch_tip - ch_root) * (x / L)

# Leading spar (bottom front bar)
bar1 = cq.Workplane("XY").box(L, bar_thk, bar_thk, centered=(False, False, False))

# Trailing spar (top bar) as tapered plate
bar2 = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, height - bar_thk))
    .polyline([
        (0, ch_root),
        (L, ch_tip),
        (L, ch_tip - bar_thk),
        (0, ch_root - bar_thk)
    ])
    .close()
    .extrude(bar_thk)
)

# Ribs connecting spar1 to spar2
ribs = cq.Workplane("XY")
for i in range(n_ribs + 1):
    x = i * L / n_ribs
    ch = chord(x)
    rib = (
        cq.Workplane("YZ")
        .transformed(offset=(x, 0, 0))
        .rect(ch, height, centered=(False, False))
        .extrude(rib_thk)
    )
    ribs = ribs.union(rib)

result = bar1.union(bar2).union(ribs)