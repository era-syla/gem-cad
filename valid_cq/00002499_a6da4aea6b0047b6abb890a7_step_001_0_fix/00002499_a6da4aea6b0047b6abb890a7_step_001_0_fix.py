import cadquery as cq

# Parameters
leg = 30          # length of each flange in cross-section (mm)
thickness = 3     # flange thickness (mm)
depth = 200       # bracket length (mm)
hole_d = 5        # hole diameter (mm)
spacing = 20      # center-to-center spacing along length (mm)
offset_end = 10   # distance from end to first hole center (mm)

# Build L-section and extrude
result = (
    cq.Workplane("XY")
      .polyline([
          (0, 0),
          (leg, 0),
          (leg, thickness),
          (thickness, thickness),
          (thickness, leg),
          (0, leg)
      ])
      .close()
      .extrude(depth)
)

# Compute hole positions along depth
count = int((depth - 2 * offset_end) // spacing) + 1
z_positions = [offset_end + i * spacing for i in range(count) if offset_end + i * spacing <= depth - offset_end]

# Drill holes through horizontal flange (face normal +Y)
result = (
    result
      .faces(">Y")
      .workplane()
      .pushPoints([(leg / 2, z) for z in z_positions])
      .hole(hole_d)
)

# Drill holes through vertical flange (face normal +X)
result = (
    result
      .faces(">X")
      .workplane()
      .pushPoints([(leg / 2, z) for z in z_positions])
      .hole(hole_d)
)