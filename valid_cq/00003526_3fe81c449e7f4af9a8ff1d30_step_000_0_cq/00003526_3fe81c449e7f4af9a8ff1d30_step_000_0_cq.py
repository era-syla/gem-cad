import cadquery as cq

# Parametric dimensions
body_diameter = 20.0
body_length = 40.0
shaft_diameter = 4.0
shaft_length_ext = 10.0  # Extension length from each side
groove_width = 0.5
groove_depth = 0.5

# Calculate total shaft length (body + extensions)
total_shaft_length = body_length + (2 * shaft_length_ext)

# Create the main central body
# We create a cylinder centered on the origin
main_body = cq.Workplane("XY").circle(body_diameter / 2).extrude(body_length)

# Create the shaft
# The shaft runs through the center, extending out both sides
# We start from the bottom plane of the main body extended downwards
shaft = (cq.Workplane("XY")
         .workplane(offset=-shaft_length_ext)
         .circle(shaft_diameter / 2)
         .extrude(total_shaft_length))

# Create the central groove
# We cut a small ring around the center of the main body
# Center of body is at Z = body_length / 2 relative to the base sketch
groove = (cq.Workplane("XY")
          .workplane(offset=body_length / 2 - groove_width / 2)
          .circle(body_diameter / 2)
          .extrude(groove_width)
          .faces(">Z").workplane()
          .circle((body_diameter / 2) - groove_depth)
          .cutThruAll()) # This is one way, but let's use a simpler boolean cut

# Alternative, more robust construction method:
# 1. Create the shaft
# 2. Create the two body halves or one body with a cut

# Let's rebuild for cleaner CSG
# Center the whole assembly on the origin for better symmetry

# 1. Main Shaft
shaft_geo = cq.Workplane("XY").circle(shaft_diameter/2).extrude(total_shaft_length).translate((0, 0, -shaft_length_ext))

# 2. Main Body Cylinder
body_geo = cq.Workplane("XY").circle(body_diameter/2).extrude(body_length)

# 3. Central Groove Cut
# Create a tool to cut the groove. It's a slightly larger cylinder that we subtract, 
# or simpler: cut a torus or a cylinder from the middle.
# Let's use a simple revolving cut approach for the groove or just cut a cylinder.
groove_cutter = (cq.Workplane("XY")
                 .workplane(offset=(body_length/2) - (groove_width/2))
                 .circle(body_diameter/2 + 1) # Outer radius (large enough to clear)
                 .circle(body_diameter/2 - groove_depth) # Inner radius (depth of groove)
                 .extrude(groove_width))

# Combine parts
# Start with body
result = body_geo.cut(groove_cutter)
# Add shaft
result = result.union(shaft_geo)

# Center the final object
result = result.translate((0, 0, -body_length/2))