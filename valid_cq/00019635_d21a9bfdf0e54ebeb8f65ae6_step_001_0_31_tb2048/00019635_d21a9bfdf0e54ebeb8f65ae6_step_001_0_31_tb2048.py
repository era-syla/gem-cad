import cadquery as cq

# Propeller Parameters
hub_radius = 6.0
hub_height = 8.0
hole_radius = 1.5

# Blade Profile Parameters
distances = [4, 15, 35, 60, 85, 100]
twists = [60, 45, 30, 15, 8, 2]
chords = [6.0, 14.0, 22.0, 20.0, 12.0, 2.0]
thicks = [4.0, 2.5, 1.8, 1.2, 0.8, 0.4]

# Create Central Hub
hub = (
    cq.Workplane("XY")
    .circle(hub_radius)
    .circle(hole_radius)
    .extrude(hub_height / 2.0, both=True)
)

# Create First Blade using Loft
blade1_wp = cq.Workplane("YZ")
for i in range(len(distances)):
    offset_val = distances[0] if i == 0 else distances[i] - distances[i-1]
    blade1_wp = (
        blade1_wp.workplane(offset=offset_val)
        .transformed(rotate=cq.Vector(0, 0, twists[i]))
        .ellipse(chords[i] / 2.0, thicks[i] / 2.0)
    )

blade1 = blade1_wp.loft()

# Create Second Blade by rotating 180 degrees around Z axis
blade2 = blade1.rotate((0, 0, 0), (0, 0, 1), 180)

# Combine Geometry
result = hub.union(blade1, clean=True).union(blade2, clean=True)