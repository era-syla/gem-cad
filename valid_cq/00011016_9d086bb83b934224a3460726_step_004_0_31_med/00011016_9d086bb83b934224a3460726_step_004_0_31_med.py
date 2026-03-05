import cadquery as cq
import math

# Parameters for the hex bolt
shaft_diameter = 10.0           # M10
thread_pitch = 1.5              # Standard pitch for M10
head_across_flats = 16.0        # Hex head width across flats
head_height = 6.4               # Hex head thickness
shaft_length = 40.0             # Total length of the shaft
shoulder_length = 3.0           # Unthreaded neck length under the head
chamfer_head = 0.8              # Chamfer size for the top of the head
chamfer_shaft = 1.0             # Chamfer size for the tip of the shaft
thread_depth_ratio = 1.2        # Determines the depth of the V-groove

# Calculate circumscribed diameter for the hexagon (point-to-point distance)
head_outer_diameter = head_across_flats / math.cos(math.radians(30))

# Create the base solid: Hex head + Cylindrical shaft
bolt = (
    cq.Workplane("XY")
    .polygon(6, head_outer_diameter)
    .extrude(head_height)
    .faces("<Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
    .edges(">Z").chamfer(chamfer_head)
    .edges("<Z").chamfer(chamfer_shaft)
)

# Thread generation using annular V-grooves for a robust 3D representation
thread_length = shaft_length - shoulder_length - chamfer_shaft
num_grooves = int(thread_length / thread_pitch)

# Define the center points for each thread groove along the shaft
# The shaft was extruded downward from Z=0 to Z=-shaft_length
groove_points = [
    (shaft_diameter / 2, -shoulder_length - i * thread_pitch - thread_pitch / 2) 
    for i in range(num_grooves)
]

# Create the V-groove cutter
# A 4-sided polygon creates a diamond shape when placed, acting as a perfect V-thread cutter
cutter = (
    cq.Workplane("XZ")
    .pushPoints(groove_points)
    .polygon(4, thread_pitch * thread_depth_ratio)
    .revolve(360, (0, 0), (0, 1))
)

# Cut the grooves into the base body to form the threads
result = bolt.cut(cutter)