import cadquery as cq
import math

# Bolt Parameters (Approximate M12 Dimensions)
major_dia = 12.0
pitch = 1.75
shaft_length = 50.0
head_flats = 19.0  # Distance across flats
head_height = 7.5

# derived parameters
head_radius = head_flats / (2 * math.cos(math.radians(30)))
minor_dia = major_dia - (1.08 * pitch)  # Approximate minor diameter for ISO threads

# 1. Create the Hex Head
# We create a hexagon and extrude it
head = (
    cq.Workplane("XY")
    .polygon(6, head_radius * 2)
    .extrude(head_height)
)

# 2. Chamfer the top of the Hex Head (Washer Face)
# We revolve a cutting tool to remove the corners on the top face
# The chamfer usually starts at the inscribed circle (the flat distance)
chamfer_angle = 30  # degrees
chamfer_cut_profile = (
    cq.Workplane("XZ", origin=(0, 0, head_height))
    .moveTo(head_flats / 2.0, 0)
    .lineTo(head_radius * 1.2, 0)  # Go past the corner
    .lineTo(head_radius * 1.2, - (head_radius * 1.2 - head_flats / 2.0) * math.tan(math.radians(chamfer_angle)))
    .close()
)

head = head.cut(chamfer_cut_profile.revolve())

# 3. Create the Shaft
# Simple cylinder extending from the bottom of the head
shaft = (
    cq.Workplane("XY")
    .circle(major_dia / 2.0)
    .extrude(shaft_length + head_height)
)

# Combine Head and Shaft
bolt = head.union(shaft)

# 4. Create Threads
# For robustness and performance in parametric models, we simulate threads 
# using revolved concentric grooves (ISO profile approximation).
# This is much faster/stable than a true helical sweep and visually nearly identical.

# Create the cutting profile for the threads (Zig-Zag pattern)
thread_cutter_path = cq.Workplane("XZ", origin=(0, 0, head_height))

# Define thread bounds
thread_start = head_height
thread_end = head_height + shaft_length - (pitch * 1.5) # Stop before the very tip for chamfer
num_threads = int((thread_end - thread_start) / pitch)

# Build the zig-zag wire for the cutter
# We construct a list of points for the groove profile
groove_points = []
current_z = thread_start

for i in range(num_threads):
    # ISO Thread Gap Profile (approximate)
    # Start at major diameter
    p1 = (major_dia / 2.0, current_z + (pitch * 0.125))
    # Bottom of thread (minor diameter)
    p2 = (minor_dia / 2.0, current_z + (pitch * 0.5))
    # End at major diameter
    p3 = (major_dia / 2.0, current_z + (pitch * 0.875))
    
    groove_points.append(p1)
    groove_points.append(p2)
    groove_points.append(p3)
    
    current_z += pitch

# If we have threads, create the cutter and subtract
if groove_points:
    # We need to close the shape to revolve it properly
    # Connect the last point to the first point via a box outside the bolt
    start_p = groove_points[0]
    end_p = groove_points[-1]
    
    outer_radius = major_dia + 2.0
    
    # Close the loop
    groove_points.append((outer_radius, end_p[1]))
    groove_points.append((outer_radius, start_p[1]))
    groove_points.append(start_p)
    
    # Create the cutter
    cutter = (
        cq.Workplane("XZ", origin=(0, 0, 0))
        .polyline(groove_points)
        .close()
        .revolve()
    )
    
    # Cut the threads from the bolt
    bolt = bolt.cut(cutter)

# 5. Chamfer the tip of the bolt
result = bolt.edges(">Z").chamfer(pitch * 0.75)