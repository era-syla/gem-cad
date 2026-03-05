import cadquery as cq

# Parameters
R = 20     # radius of each lobe
d = 30     # center-to-center distance of lobes along Y
h = 8      # thickness of the plate

# Create first lobe
lobe1 = cq.Workplane("XY").circle(R).extrude(h)

# Create second lobe, offset along Y
lobe2 = cq.Workplane("XY").transformed(offset=(0, -d, 0)).circle(R).extrude(h)

# Boolean union to fuse lobes into one solid
result = lobe1.union(lobe2)