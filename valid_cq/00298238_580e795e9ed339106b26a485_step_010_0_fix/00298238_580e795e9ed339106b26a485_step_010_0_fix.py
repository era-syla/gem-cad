import cadquery as cq

hex_width = 10
hex_thickness = 5
shaft_radius = 3
shaft_length = 40
thread_length = 25
thread_diameter = 6
thread_pitch = 1.5

# Create the hex head
hex_head = (cq.Workplane("XY")
            .polygon(6, hex_width)
            .extrude(hex_thickness))

# Create the shaft
shaft = (cq.Workplane("XY")
         .circle(shaft_radius)
         .extrude(shaft_length))

# Combine the hex head and shaft
bolt = hex_head.union(shaft)

# Create the threaded part
thread = (cq.Workplane("XY", origin=(0, 0, shaft_length))
          .circle(thread_diameter / 2)
          .extrude(thread_length))

# Combine the bolt with the thread
result = bolt.union(thread)