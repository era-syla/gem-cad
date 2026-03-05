import cadquery as cq

# Parameters for the propeller
hub_radius = 6.0
hub_height = 10.0
hole_radius = 1.5

# Blade profile parameters at different sections along the length
# Distances from the center
y_offsets = [5.0, 15.0, 35.0, 60.0, 85.0]
# Half-chords (width of the blade)
chords = [3.0, 7.0, 11.0, 8.0, 1.5]
# Half-thicknesses
thicknesses = [2.5, 1.8, 1.2, 0.8, 0.3]
# Twist angles in degrees
angles = [45, 35, 20, 10, 2]

# Create the central hub
hub = (
    cq.Workplane("XY")
    .circle(hub_radius)
    .extrude(hub_height)
    .faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutThruAll()
)

# Create the first blade using a lofted profile
# Start on XZ plane and shift to the middle of the hub's height
blade = cq.Workplane("XZ").transformed(offset=(0, hub_height / 2.0, 0))

for i in range(len(y_offsets)):
    dy = y_offsets[i] if i == 0 else y_offsets[i] - y_offsets[i-1]
    da = angles[i] if i == 0 else angles[i] - angles[i-1]
    
    # Move along local Z (global Y) and rotate around local Z (global Y)
    blade = (
        blade.workplane(offset=dy)
        .transformed(rotate=(0, 0, da))
        .ellipse(chords[i], thicknesses[i])
    )

blade1 = blade.loft()

# Create the second blade by rotating the first one by 180 degrees
blade2 = blade1.rotate((0, 0, 0), (0, 0, 1), 180)

# Combine the hub and blades into a single solid
result = hub.union(blade1).union(blade2)