import cadquery as cq

# Approximate Texas silhouette coordinates
tx_coords = [
    (-105, 50), (-100, 20), (-105, -10), (-95, -30), (-90, -60),
    (-80, -90), (-60, -100), (-30, -120), (0, -110), (30, -120),
    (50, -100), (80, -80), (95, -50), (120, -10), (115, 50),
    (95, 70), (60, 90), (30, 100), (0, 90), (-30, 80),
    (-60, 70), (-90, 60), (-105, 50)
]

# Create base silhouette and extrude
base = cq.Workplane("XY").polyline(tx_coords).close().extrude(5)

# Create towers on top face of base
top_face = base.faces(">Z")
tower1 = top_face.workplane().center(20, 100).rect(15, 10).extrude(15)
tower2 = top_face.workplane().center(80, 50).rect(10, 8).extrude(15)

# Combine all solids
result = base.union(tower1).union(tower2)