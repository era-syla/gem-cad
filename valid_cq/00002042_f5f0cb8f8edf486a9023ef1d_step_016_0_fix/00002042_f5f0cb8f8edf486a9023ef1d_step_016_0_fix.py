import cadquery as cq

def make_propeller():
    # Hub
    hub = cq.Workplane("XY").circle(3).extrude(4)
    # Blade profile (approximate)
    blade_profile = [(3, -1), (60, -8), (60, 8), (3, 1)]
    blade = (
        cq.Workplane("XY")
        .polyline(blade_profile)
        .close()
        .extrude(2)
        .translate((0, 0, 1))  # center on hub thickness
    )
    # Second blade opposite
    blade2 = blade.rotate((0, 0, 0), (0, 0, 1), 180)
    return hub.union(blade).union(blade2)

# Create four propellers with different positions and tilts
positions = [(0, 0, 0), (70, 0, 0), (0, 70, 0), (70, 70, 0)]
rotations = [(0, 0, 0), (0, 20, 0), (20, 0, 0), (0, 0, 30)]

props = []
for pos, rot in zip(positions, rotations):
    prop = make_propeller()
    prop = prop.rotate((0, 0, 0), (1, 0, 0), rot[0])
    prop = prop.rotate((0, 0, 0), (0, 1, 0), rot[1])
    prop = prop.rotate((0, 0, 0), (0, 0, 1), rot[2])
    prop = prop.translate(pos)
    props.append(prop)

result = props[0].union(props[1]).union(props[2]).union(props[3])