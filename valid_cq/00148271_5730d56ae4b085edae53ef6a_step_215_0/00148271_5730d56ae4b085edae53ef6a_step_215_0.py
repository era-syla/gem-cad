import cadquery as cq
import math

# --- Parameters ---
# Overall Dimensions
od = 100.0                # Outer Diameter of the disk
thickness = 2.0           # Thickness of the disk

# Bolt Pattern
bcd = 75.0                # Bolt Circle Diameter
hole_lg_dia = 12.0        # Diameter of large holes (vertical pair)
hole_sm_dia = 7.0         # Diameter of small holes (horizontal pair)

# Central Spline/Hole
spline_id_inner = 40.0    # Inner diameter (tips of teeth)
spline_id_outer = 52.0    # Outer diameter (bottom of gaps)
num_teeth = 4             # Number of teeth/gaps
gap_angle = 45.0          # Angular width of the gap in degrees

# --- Helper Calculations ---
r_gap = spline_id_outer / 2.0
half_gap_rad = math.radians(gap_angle / 2.0)

# Calculate points for the gap sector profile (aligned with X-axis)
# Center
p0 = (0, 0)
# Start of arc (bottom)
p1 = (r_gap * math.cos(-half_gap_rad), r_gap * math.sin(-half_gap_rad))
# Midpoint of arc (on X-axis)
p_mid = (r_gap, 0)
# End of arc (top)
p2 = (r_gap * math.cos(half_gap_rad), r_gap * math.sin(half_gap_rad))

# --- Model Generation ---

# 1. Create Base Disk
result = cq.Workplane("XY").circle(od / 2.0).extrude(thickness)

# 2. Cut the Base Inner Hole (Circle at inner radius)
result = (
    result.faces(">Z").workplane()
    .circle(spline_id_inner / 2.0)
    .cutThruAll()
)

# 3. Cut the Spline Gaps
# We rotate the workplane for each gap and cut a sector shape
for i in range(num_teeth):
    angle = i * (360.0 / num_teeth)
    result = (
        result.faces(">Z")
        .workplane()
        .transformed(rotate=(0, 0, angle))
        .moveTo(*p0)
        .lineTo(*p1)
        .threePointArc(p_mid, p2)
        .close()
        .cutThruAll()
    )

# 4. Cut Large Mounting Holes (Top and Bottom - Y Axis)
result = (
    result.faces(">Z").workplane()
    .pushPoints([(0, bcd/2.0), (0, -bcd/2.0)])
    .hole(hole_lg_dia)
)

# 5. Cut Small Mounting Holes (Left and Right - X Axis)
result = (
    result.faces(">Z").workplane()
    .pushPoints([(bcd/2.0, 0), (-bcd/2.0, 0)])
    .hole(hole_sm_dia)
)