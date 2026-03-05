import cadquery as cq

# Parametric dimensions
H = 150.0           # Total height of the panel
W = 120.0           # Width of the main panel
T = 3.0             # Thickness of the panel
R_rod = 2.5         # Radius of the hinge rod
R_bracket = 4.5     # Radius of the hinge brackets
H_bracket = 8.0     # Height of the hinge brackets
L_bracket = 12.0    # Extension length of the brackets from the rod center
rod_ext = 2.0       # Extension of the rod above and below the brackets

# 1. Hinge Pin (Rod)
rod = (
    cq.Workplane("XY")
    .workplane(offset=-rod_ext)
    .circle(R_rod)
    .extrude(H + 2 * rod_ext)
    .edges(">Z or <Z")
    .chamfer(0.5)
)

# 2. Bottom Bracket
bot_bracket = (
    cq.Workplane("XY")
    .moveTo(0, R_bracket)
    .lineTo(L_bracket, R_bracket)
    .lineTo(L_bracket, -R_bracket)
    .lineTo(0, -R_bracket)
    .threePointArc((-R_bracket, 0), (0, R_bracket))
    .close()
    .extrude(H_bracket)
    .edges("<Z")
    .fillet(0.5)
)

# 3. Top Bracket
top_bracket = (
    cq.Workplane("XY")
    .workplane(offset=H - H_bracket)
    .moveTo(0, R_bracket)
    .lineTo(L_bracket, R_bracket)
    .lineTo(L_bracket, -R_bracket)
    .lineTo(0, -R_bracket)
    .threePointArc((-R_bracket, 0), (0, R_bracket))
    .close()
    .extrude(H_bracket)
    .edges(">Z")
    .fillet(0.5)
)

# 4. Main Panel
panel = (
    cq.Workplane("XY")
    .center(L_bracket + W / 2.0, 0)
    .box(W, T, H, centered=(True, True, False))
    .edges(">X or >Z or <Z")
    .fillet(1.0)
)

# Combine all components into the final result
result = rod.union(bot_bracket).union(top_bracket).union(panel)