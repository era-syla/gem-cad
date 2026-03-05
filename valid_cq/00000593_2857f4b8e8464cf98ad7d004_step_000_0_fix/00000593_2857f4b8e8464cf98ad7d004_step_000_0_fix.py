import cadquery as cq

# Create a stack of discs to simulate the ribbed cylinder appearance
result = cq.Workplane("XY")

num_discs = 20
disc_radius = 30
disc_height = 4
gap = 0.5

total_height = num_discs * (disc_height + gap)

# Start with the first disc
result = cq.Workplane("XY").circle(disc_radius).extrude(disc_height)

# Stack additional discs
for i in range(1, num_discs):
    z_offset = i * (disc_height + gap)
    new_disc = cq.Workplane("XY").workplane(offset=z_offset).circle(disc_radius).extrude(disc_height)
    result = result.union(new_disc)