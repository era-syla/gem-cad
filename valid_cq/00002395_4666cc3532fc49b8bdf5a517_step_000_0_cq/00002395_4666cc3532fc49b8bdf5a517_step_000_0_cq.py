import cadquery as cq
import math

# --- Dimensions and Parameters ---

# Vertical Bar
bar_width = 10.0
bar_thickness = 5.0
bar_height = 80.0
hole_diams = [5.0, 4.0, 3.0]
hole_spacing = 12.0

# Triangular Wedge
wedge_base_width = 10.0
wedge_height = 10.0
wedge_length = 20.0

# Curved Pipe / Torus Segment
pipe_radius = 6.0
pipe_bend_radius = 25.0
pipe_angle = 130.0

# Main Donut / Torus
torus_major_radius = 25.0
torus_minor_radius = 10.0

# Curved Spout / Loft
spout_base_radius = 8.0
spout_top_radius = 5.0
spout_height = 60.0
spout_bend_offset = 20.0  # How much it bends sideways

# --- Construction ---

# 1. The Vertical Bar with holes
# Origin is roughly at the connection point of the pipe
bar = (cq.Workplane("YZ")
       .box(bar_width, bar_height, bar_thickness, centered=(True, True, True))
       .translate((-bar_thickness/2, -bar_height/4, 0)) # Position relative to origin
      )

# Add holes to the bottom section of the bar
# We find the bottom face or use coordinates
# Let's just use absolute coordinates based on the bar's position
# Bar center is at y = -20. Holes go downwards from there.
hole_start_y = -30
for i, diam in enumerate(hole_diams):
    y_pos = hole_start_y - (i * hole_spacing)
    bar = bar.faces(">X").workplane().moveTo(0, y_pos).hole(diam)


# 2. Triangular Wedge Feature
# Sticking out of the bar. Looks like a chamfered protrusion or a separate prism.
# Let's make a prism.
wedge = (cq.Workplane("XY")
         .moveTo(-wedge_length, -wedge_base_width/2)
         .lineTo(0, -wedge_base_width/2)
         .lineTo(0, wedge_base_width/2)
         .close()
         .extrude(wedge_height)
         .rotate((0,0,0), (0,0,1), 180) # Orient facing "left" relative to the bar
         .translate((-bar_thickness, 0, 5)) # Attach to the bar
        )
# A second, smaller rectangular protrusion near the top
top_rect = (cq.Workplane("XY")
            .box(15, 5, 5)
            .translate((-10, 15, 5))
           )


# 3. The Connecting Pipe (Bent Tube)
# Connects the bar to the Torus area.
# A sweep along a path.
path = (cq.Workplane("XZ")
        .moveTo(0, 0)
        .threePointArc((pipe_bend_radius, pipe_bend_radius), (pipe_bend_radius*2, 0))
        )
# Simpler approach: Revolve a circle
pipe = (cq.Workplane("XY")
        .circle(pipe_radius)
        .revolve(180, (pipe_bend_radius, 0, 0), (pipe_bend_radius, 1, 0))
        .rotate((0,0,0),(0,0,1), 90)
        .translate((0, 0, 0))
       )
# Cut a triangular window into the pipe/bar junction area as seen in the image
cutout = (cq.Workplane("YZ")
          .moveTo(10, 5)
          .lineTo(25, 5)
          .lineTo(10, 20)
          .close()
          .extrude(20)
          .translate((-10, -5, -5))
          )


# 4. The Main Torus (Donut)
torus = (cq.Workplane("XY")
         .parametricCurve(lambda t: (
             (torus_major_radius + torus_minor_radius * math.cos(t)) * math.cos(0),
             (torus_major_radius + torus_minor_radius * math.cos(t)) * math.sin(0),
             torus_minor_radius * math.sin(t)
         )) # This is just a circle, we need the solid
        )
# Easier standard torus creation
torus_solid = (cq.Solid.makeTorus(torus_major_radius, torus_minor_radius)
               .translate((pipe_bend_radius * 2.5, 0, -torus_minor_radius/2))
              )


# 5. The Curved Spout/Horn
# This looks like a loft between a circle on the torus and a square/shape at the top.
# Or a sweep along a spline.
spout_path_pts = [
    (0, 0, 0),
    (5, 5, 20),
    (spout_bend_offset, spout_bend_offset, spout_height)
]

# We will create a wire for the path
spout_path = cq.Workplane("XZ").spline(spout_path_pts)

# Create the profile at the base (on the torus)
base_plane = cq.Workplane("XY").translate((pipe_bend_radius * 2.5, 0, torus_minor_radius/2))
spout = (base_plane
         .circle(spout_base_radius)
         .workplane(offset=spout_height/2)
         .center(5, 5) # Offset for the mid-section
         .circle(spout_base_radius * 0.8)
         .workplane(offset=spout_height/2)
         .center(spout_bend_offset-5, spout_bend_offset-5) # Offset for the top
         .rect(spout_top_radius*2, spout_top_radius*2) # Transition to rectangle at top
         .loft()
        )
# Adjust spout position to sit on the torus
spout = spout.translate((0, 0, 0)) 


# --- Assembly ---
# Combine all parts
result = (bar
          .union(wedge)
          .union(top_rect)
          .union(pipe)
          .cut(cutout)
          .union(torus_solid)
          .union(spout)
         )

# Export for visualization (optional in some contexts, but 'result' is the requirement)