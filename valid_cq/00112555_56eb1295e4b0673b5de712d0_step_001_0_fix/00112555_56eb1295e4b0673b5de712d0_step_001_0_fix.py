import cadquery as cq

# Parameters
L = 120    # outer length
W = 80     # outer width
T = 5      # thickness
WT = 5     # wall thickness

# Create base plate
result = cq.Workplane("XY").rect(L, W).extrude(T)

# Cut out the central cavity
result = result.cut(
    cq.Workplane("XY")
      .rect(L - 2*WT, W - 2*WT)
      .extrude(T)
)

# Bottom-left pocket
result = result.cut(
    cq.Workplane("XY")
      .moveTo(-L/2 + WT + 20, -W/2 + WT + 10)
      .rect(40, 20)
      .extrude(T)
)

# Top-right pocket
result = result.cut(
    cq.Workplane("XY")
      .moveTo(L/2 - WT - 20, W/2 - WT - 10)
      .rect(40, 20)
      .extrude(T)
)

# Right-side slot
result = result.cut(
    cq.Workplane("XY")
      .moveTo(L/2 - WT/2, 0)
      .rect(WT, W - 2*WT)
      .extrude(T)
)