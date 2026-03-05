import cadquery as cq
import math

# Parameters
ml = 100    # main length
mw = 20     # main width
bl = 20     # big wing length
sw = 10     # small wing length
th = 3      # thickness
hd = 3      # hole diameter

# Angles in radians
ang_big = math.radians(30)
ang_small = -math.radians(30)

half_ml = ml/2
half_mw = mw/2

# Compute wing tip coordinates
bt_left = (
    -half_ml - bl * math.cos(ang_big),
     half_mw + bl * math.sin(ang_big)
)
bt_right = (
     half_ml + bl * math.cos(ang_big),
     half_mw + bl * math.sin(ang_big)
)
st_right = (
     half_ml + sw * math.cos(ang_small),
    -half_mw + sw * math.sin(ang_small)
)
st_left = (
    -half_ml + sw * math.cos(ang_small),
    -half_mw + sw * math.sin(ang_small)
)

# Define perimeter points
pts = [
    bt_left,
    (-half_ml,  half_mw),
    ( half_ml,  half_mw),
    bt_right,
    ( half_ml,  half_mw),
    ( half_ml, -half_mw),
    st_right,
    ( half_ml, -half_mw),
    (-half_ml, -half_mw),
    st_left,
    (-half_ml, -half_mw),
]

# Build the solid and add holes
result = (
    cq.Workplane("XY")
      .polyline(pts)
      .close()
      .extrude(th)
      .faces(">Z")
      .workplane()
      .pushPoints([bt_left, bt_right])
      .hole(hd)
)