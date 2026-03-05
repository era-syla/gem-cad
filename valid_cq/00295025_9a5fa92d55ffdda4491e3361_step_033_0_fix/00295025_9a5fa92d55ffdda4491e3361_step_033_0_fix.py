import cadquery as cq

# Parameters
outer_diameter = 20
inner_diameter = 16
length = 100
thread_width = 2
thread_depth = 1
num_threads = 10

# Create the main cylinder
result = cq.Workplane("XY").circle(outer_diameter / 2).extrude(length)

# Hollow the cylinder
result = result.faces(">Z").workplane().circle(inner_diameter / 2).cutBlind(-length)

# Add threads to both ends
for end in ["<Z", ">Z"]:
    result = result.faces(end).workplane() \
        .circle(outer_diameter / 2).circle(outer_diameter / 2 - thread_depth).extrude(thread_width * num_threads)

# Cut threads to create the cosmetic effect
result = result.faces("<Z").workplane(centerOption="CenterOfMass") \
    .polygon(3, outer_diameter).cutBlind(-thread_width * num_threads)
result = result.faces(">Z").workplane(centerOption="CenterOfMass") \
    .polygon(3, outer_diameter).cutBlind(thread_width * num_threads)