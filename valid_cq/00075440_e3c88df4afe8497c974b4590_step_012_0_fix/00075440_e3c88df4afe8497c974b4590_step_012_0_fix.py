import cadquery as cq

# Parameters
R = 20          # Radius of front semi-circle
L1 = 30         # Straight length behind the semi-circle
ext_offset = 10 # X-offset of the back extension
ext_w = 15      # Width of the back extension in X
ext_l = 15      # Length of the back extension in Y
thickness = 5   # Thickness in Z
hole_d = 8      # Diameter of the hole in extension

# 2D profile in the XY plane
profile = (
    cq.Workplane("XY")
      .moveTo(-R, 0)
      .threePointArc((0, -R), (R, 0))
      .lineTo(R, L1)
      .lineTo(ext_offset + ext_w, L1)
      .lineTo(ext_offset + ext_w, L1 + ext_l)
      .lineTo(ext_offset,       L1 + ext_l)
      .lineTo(ext_offset,       L1)
      .lineTo(-R,               L1)
      .close()
)

# Extrude and add the hole in the back extension
result = (
    profile
      .extrude(thickness)
      .faces(">Y")             # Select the face at max Y (the back extension face)
      .workplane()             # Workplane centered on that face
      .hole(hole_d, depth=ext_l + 0.1)  # Cut a blind hole through just the extension
)