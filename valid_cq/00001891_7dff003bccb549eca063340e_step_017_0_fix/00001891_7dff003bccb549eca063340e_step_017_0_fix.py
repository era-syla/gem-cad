import cadquery as cq
import math

# Parameters
R = 30        # Base radius
A = 8         # Amplitude of wave
N = 12        # Number of waves around circumference
H0 = 3        # Base thickness
H1 = 15       # Total height at wave peaks
segments = 120  # Number of points to sample

# Generate point lists for bottom and top profiles
angles = [i * 2 * math.pi / segments for i in range(segments)]
bottom_pts = [(R * math.cos(a), R * math.sin(a)) for a in angles]
top_pts = [((R + A * math.sin(N * a)) * math.cos(a),
            (R + A * math.sin(N * a)) * math.sin(a))
           for a in angles]

# Build the base cylinder
base = cq.Workplane("XY").circle(R).extrude(H0)

# Build the wavy side by lofting between bottom and top profiles
shell = (
    cq.Workplane("XY")
      .workplane(offset=H0)
      .polyline(bottom_pts).close()
      .workplane(offset=(H1 - H0))
      .polyline(top_pts).close()
      .loft(combine=True)
)

# Combine base and shell
result = base.union(shell)