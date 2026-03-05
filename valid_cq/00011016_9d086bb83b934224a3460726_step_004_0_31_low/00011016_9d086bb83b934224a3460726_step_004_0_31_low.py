import cadquery as cq

# Parameters for the bolt
shaft_radius = 4.0
shaft_length = 30.0
head_radius = 7.0
head_thickness = 5.0
chamfer_size = 0.5
thread_pitch = 1.0
thread_depth = 0.8
collar_radius = 4.5
collar_thickness = 1.0

# 1. Create the hex head
head = cq.Workplane("XY").polygon(6, head_radius * 2).extrude(head_thickness)
head = head.faces(">Z").chamfer(chamfer_size)

# 2. Create the collar
collar = cq.Workplane("XY").workplane(offset=-collar_thickness).circle(collar_radius).extrude(collar_thickness)

# 3. Create the shaft
shaft = cq.Workplane("XY").workplane(offset=-(collar_thickness + shaft_length)).circle(shaft_radius).extrude(shaft_length)
shaft = shaft.faces("<Z").chamfer(chamfer_size)

# Combine parts (excluding actual threads to keep it simple and performant, 
# representing threads visually is often done with texture in CAD, 
# but we'll add a simplified grooved appearance if needed. Here we stick to the basic solid.)
result = head.union(collar).union(shaft)

# (Optional) Add decorative threads by cutting small grooves
# This is a simplified representation of threads
num_threads = int(shaft_length / thread_pitch) - 2
for i in range(num_threads):
    z_offset = -(collar_thickness + shaft_length) + (i + 1) * thread_pitch
    groove = cq.Workplane("XY").workplane(offset=z_offset).circle(shaft_radius).circle(shaft_radius - thread_depth/2).extrude(thread_pitch/2)
    result = result.cut(groove)
