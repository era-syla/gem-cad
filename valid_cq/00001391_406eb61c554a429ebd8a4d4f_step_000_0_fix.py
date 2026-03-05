import cadquery as cq

# Base plate dimensions
base_length = 80
base_width = 40
base_height = 5

# Cleat/bollard dimensions
cleat_height = 25
cleat_width = 60
cleat_depth = 12
hole_radius = 7
wall_thickness = 4

# Create the base plate
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# Create the main cleat body - a U-shaped structure
# The cleat sits on top of the base plate
# Build the cleat as a solid block first, then cut holes through it

# Cleat body: rectangular block with arch top
cleat_x = cleat_width
cleat_y = cleat_depth
cleat_z = cleat_height

# Create the arch/cleat body
# We'll build it as an extruded profile
# Profile: rectangle with semicircular top

def make_cleat_profile():
    # Create a 2D profile for the cleat (side view - in XZ plane)
    # Rectangle with semicircle on top
    w = cleat_y  # depth (Y direction becomes width in profile)
    h = cleat_z  # height
    r = cleat_y / 2  # radius of semicircle = half the depth
    
    pts = [
        (-w/2, 0),
        (-w/2, h - r),
        (w/2, h - r),
        (w/2, 0),
    ]
    
    result = (cq.Workplane("YZ")
              .polyline(pts)
              .radiusArc((0, h + r - r), r)  
              )
    return result

# Build the cleat using a different approach
# Create a swept/extruded U-arch shape

# The cleat is a bar that goes up, arches over, comes back down
# with 3 holes through it

# Create the cleat body as a box with rounded top
cleat_body = (cq.Workplane("XY")
              .workplane(offset=base_height)
              .rect(cleat_x, cleat_y)
              .extrude(cleat_z - cleat_y/2)
              )

# Add semicylinder on top
cleat_top = (cq.Workplane("XZ")
             .workplane(offset=0)
             .center(0, base_height + cleat_z - cleat_y/2)
             .circle(cleat_y/2)
             .extrude(cleat_x/2)
             )

# Use a profile approach instead
# Side profile of cleat in YZ plane, extruded along X
half_w = cleat_y / 2
h_rect = cleat_z - half_w

cleat = (cq.Workplane("YZ")
         .center(0, base_height)
         .rect(cleat_y, h_rect * 2, centered=False)
         .val()
         )

# Simpler: build cleat as union of box + cylinder
cleat_box = (cq.Workplane("XY")
             .box(cleat_x, cleat_y, cleat_z - cleat_y/2, centered=(True, True, False))
             .translate((0, 0, base_height))
             )

cleat_cyl = (cq.Workplane("XY")
             .workplane(offset=base_height + cleat_z - cleat_y/2)
             .center(0, 0)
             .rect(cleat_x, cleat_y)
             )

# Build cleat top as a cylinder along X axis
top_cyl = (cq.Workplane("YZ")
           .circle(cleat_y/2)
           .extrude(cleat_x/2)
           .translate((0, 0, base_height + cleat_z - cleat_y/2))
           )

cleat_solid = cleat_box.union(top_cyl)

# Now cut 3 holes through the cleat (along X axis)
# Holes are circular, going through the depth (Y direction)
hole_spacing = cleat_x / 4
hole_centers = [-hole_spacing, 0, hole_spacing]

for hx in hole_centers:
    hole = (cq.Workplane("XZ")
            .center(hx, base_height + cleat_y/2 + 1)
            .circle(hole_radius)
            .extrude(cleat_y + 2)
            .translate((0, -(cleat_y/2 + 1), 0))
            )
    cleat_solid = cleat_solid.cut(hole)

# Combine base and cleat
result = base.union(cleat_solid)

# Add fillets to smooth edges
result = result.edges("|Z").fillet(2)