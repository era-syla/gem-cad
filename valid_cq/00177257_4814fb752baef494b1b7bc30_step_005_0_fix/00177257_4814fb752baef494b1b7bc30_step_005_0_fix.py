import cadquery as cq

# Parameters
L = 120        # length of plate
W = 80         # width of plate
T = 5          # thickness of plate
corner_r = 5   # fillet radius on vertical edges
tri_base = 60  # base length of each triangular cutout
hole_dia = 4   # diameter of small holes
hole_margin = 10  # margin from plate edge to hole center
hx_hole = 30      # horizontal offset for holes from center
hy_hole = W/2 - hole_margin  # vertical offset for holes from center
stand_dia = 6     # diameter of standoffs
stand_h = 10      # height of standoffs
stand_margin = 10 # margin from plate edge for standoffs
cut_r = 20        # radius for side concave cutout

result = (
    cq.Workplane("XY")
    # Base plate
    .rect(L, W)
    .extrude(T)
    .edges("|Z").fillet(corner_r)
    # Triangular cutouts on top face
    .faces(">Z").workplane()
    .polyline([(-tri_base/2,  W/2), ( tri_base/2,  W/2), (0, 0)]).close().cutThruAll()
    .faces(">Z").workplane()
    .polyline([(-tri_base/2, -W/2), ( tri_base/2, -W/2), (0, 0)]).close().cutThruAll()
    .faces(">Z").workplane()
    .polyline([ (L/2, -tri_base/2), ( L/2,  tri_base/2), (0, 0)]).close().cutThruAll()
    .faces(">Z").workplane()
    .polyline([(-L/2, -tri_base/2), (-L/2,  tri_base/2), (0, 0)]).close().cutThruAll()
    # Small through-holes on top and bottom rows
    .faces(">Z").workplane()
    .pushPoints([
        (-hx_hole,  hy_hole), (0,  hy_hole), ( hx_hole,  hy_hole),
        (-hx_hole, -hy_hole), (0, -hy_hole), ( hx_hole, -hy_hole)
    ])
    .circle(hole_dia/2).cutThruAll()
    # Side concave cutouts (half-cylinders) on long edges
    .faces(">Y").workplane().circle(cut_r).cutThruAll()
    .faces("<Y").workplane().circle(cut_r).cutThruAll()
    # Standoffs on bottom face
    .faces("<Z").workplane()
    .pushPoints([
        (-L/2 + stand_margin, -W/2 + stand_margin),
        (-L/2 + stand_margin,  W/2 - stand_margin),
        ( L/2 - stand_margin, -W/2 + stand_margin),
        ( L/2 - stand_margin,  W/2 - stand_margin),
    ])
    .circle(stand_dia/2).extrude(stand_h)
)

# 'result' holds the final solid
# You can export or display 'result' in your environment
