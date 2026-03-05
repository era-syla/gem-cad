import cadquery as cq

# Parameters
R1 = 20    # Flange radius
t1 = 5     # Flange thickness
R2 = 10    # Small cylinder radius
L2 = 30    # Small cylinder length
R3 = 7     # Inner hole radius
key_w = 4  # Key width (along X)
key_d = 3  # Key thickness (radial, along Y)

# Build flange and small cylinder
result = (
    cq.Workplane("XY")
      .circle(R1)
      .extrude(t1)
      .faces(">Z")
      .workplane()
      .circle(R2)
      .extrude(L2)
      .faces(">Z")
      .workplane()
      .circle(R3)
      .cutThruAll()
)

# Build key and fuse
key = (
    cq.Workplane("XZ", origin=(0, R2, t1 + L2/2))
      .rect(key_w, L2)
      .extrude(key_d)
)

result = result.union(key)