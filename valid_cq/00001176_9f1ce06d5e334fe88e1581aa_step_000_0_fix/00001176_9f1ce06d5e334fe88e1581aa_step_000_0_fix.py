import cadquery as cq

# Parameters
L = 200      # base length
W = 80       # base width
Hbase = 20   # base height
rail_h = 10  # rail height
rail_w = 10  # rail width
JahD = 40    # jaw depth
JahW = W     # jaw width
JahH = 40    # jaw height
hole_d = 10  # hole diameter in jaws
screw_r = 3  # screw radius
handle_r = 2 # handle radius
handle_l = 40# handle length

# Base
base = cq.Workplane("XY").box(L, W, Hbase)

# Guide rails
rail_length = L - 20
rail1 = (
    cq.Workplane("XY")
      .workplane(offset=Hbase)
      .transformed(offset=(0,  W/2 - rail_w/2 - 5, 0))
      .rect(rail_length, rail_w)
      .extrude(rail_h)
)
rail2 = (
    cq.Workplane("XY")
      .workplane(offset=Hbase)
      .transformed(offset=(0, - (W/2 - rail_w/2 - 5), 0))
      .rect(rail_length, rail_w)
      .extrude(rail_h)
)
rails = rail1.union(rail2)

# Fixed jaw
fixed_jaw = (
    cq.Workplane("XY")
      .workplane(offset=Hbase + rail_h)
      .transformed(offset=(L/2 - JahD/2, 0, 0))
      .box(JahD, JahW, JahH)
      .faces(">X")
      .workplane()
      .pushPoints([(0,  JahW/4), (0, -JahW/4)])
      .circle(hole_d/2)
      .cutThruAll()
)

# Moving jaw
moving_jaw = (
    cq.Workplane("XY")
      .workplane(offset=Hbase + rail_h)
      .transformed(offset=(-L/2 + JahD/2, 0, 0))
      .box(JahD, JahW, JahH)
      .faces("<X")
      .workplane()
      .pushPoints([(0,  JahW/4), (0, -JahW/4)])
      .circle(hole_d/2)
      .cutThruAll()
)

# Screw
screw = (
    cq.Workplane("YZ")
      .workplane(origin=(-L/2 + JahD, 0, Hbase + rail_h + JahH/2))
      .circle(screw_r)
      .extrude(L - 2*JahD)
)

# Handle
handle = (
    cq.Workplane("YZ")
      .workplane(origin=(-L/2 + JahD, 0, Hbase + rail_h + JahH/2))
      .circle(handle_r)
      .extrude(-handle_l)
)

# Combine all parts
result = base.union(rails).union(fixed_jaw).union(moving_jaw).union(screw).union(handle)