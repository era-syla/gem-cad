import cadquery as cq

# --- Parameters ---

# Base dimensions
base_radius = 25.0
base_height = 8.0

# Stem dimensions
stem_cone_bottom_radius = 5.0
stem_cone_top_radius = 12.0
stem_cone_height = 15.0
stem_sphere_radius = 8.0

# Top Platform dimensions
platform_radius = 35.0
platform_height = 5.0
platform_rim_height = 2.0  # Extra thickness for the rim visual

# "Cityscape" Blocks (approximate layout based on visual inspection)
# We will define a list of (shape_type, x, y, width, depth, height, rotation)
# or specific construction logic for the irregular shapes.

# --- Construction ---

# 1. Base Assembly
# Bottom disk
base = cq.Workplane("XY").circle(base_radius).extrude(base_height)

# 2. Stem Construction
# A tapered cone section sitting on the base
stem_cone = (cq.Workplane("XY")
             .workplane(offset=base_height)
             .circle(stem_cone_top_radius)
             .workplane(offset=stem_cone_height)
             .circle(stem_cone_bottom_radius)
             .loft(combine=True))

# A sphere sitting on top of the cone
sphere_center_z = base_height + stem_cone_height + stem_sphere_radius * 0.7 # Slight overlap
stem_sphere = (cq.Workplane("XY")
               .workplane(offset=sphere_center_z)
               .sphere(stem_sphere_radius))

# 3. Top Platform
# The circular table top
platform_z = sphere_center_z + stem_sphere_radius * 0.7
platform = (cq.Workplane("XY")
            .workplane(offset=platform_z)
            .circle(platform_radius)
            .extrude(platform_height))

# A slight rim or second layer to give it the "thick" look
platform_rim = (cq.Workplane("XY")
                .workplane(offset=platform_z + platform_height)
                .circle(platform_radius * 0.95) # slightly smaller
                .extrude(platform_rim_height))

# 4. Geometric Features on Top (The "City")
# We will build these on the top face of the rim/platform
top_surface = platform_z + platform_height + platform_rim_height

# Feature 1: The Tallest Tower (Left side)
# Looks like a modified rectangle with a chamfered top or smaller box on top
tower1_h = 40.0
tower1_w = 12.0
tower1_d = 12.0
tower1 = (cq.Workplane("XY")
          .workplane(offset=top_surface)
          .center(-15, 5)
          .rect(tower1_w, tower1_d)
          .extrude(tower1_h))

# Detail on top of Tower 1
tower1_detail = (cq.Workplane("XY")
                 .workplane(offset=top_surface + tower1_h)
                 .center(-15, 5)
                 .rect(tower1_w * 0.6, tower1_d * 0.6)
                 .extrude(3.0))

# Feature 2: Triangular Prism / Wedge (Front/Center)
wedge1_h = 15.0
wedge1 = (cq.Workplane("XY")
          .workplane(offset=top_surface)
          .center(0, -15)
          .polyline([(0,0), (10, 5), (10, -5), (0,0)]) # Triangle shape
          .close()
          .extrude(wedge1_h))

# Feature 3: Medium Block (Center)
block_h = 20.0
block_center = (cq.Workplane("XY")
                .workplane(offset=top_surface)
                .center(-2, -2)
                .rect(10, 10)
                .extrude(block_h))

# Feature 4: Irregular Polygon Block (Back)
poly_h = 15.0
poly_block = (cq.Workplane("XY")
              .workplane(offset=top_surface)
              .center(0, 10)
              .polyline([(-5, 0), (5, 0), (10, 8), (0, 12), (-8, 8), (-5, 0)])
              .close()
              .extrude(poly_h))

# Feature 5: Thin Tall Tower (Right side)
tower2_h = 30.0
tower2 = (cq.Workplane("XY")
          .workplane(offset=top_surface)
          .center(20, 0)
          .rect(6, 6)
          .extrude(tower2_h))

# Feature 6: Triangular cutout or negative space shape (Center Right)
# In the image, there is a distinct triangular prism shape lying flat or extruding up
wedge2_h = 10.0
wedge2 = (cq.Workplane("XY")
          .workplane(offset=top_surface)
          .center(10, -5)
          .polyline([(0,0), (8, 0), (4, 8), (0,0)])
          .close()
          .extrude(wedge2_h))


# 5. Combine everything
result = (base
          .union(stem_cone)
          .union(stem_sphere)
          .union(platform)
          .union(platform_rim)
          .union(tower1)
          .union(tower1_detail)
          .union(wedge1)
          .union(block_center)
          .union(poly_block)
          .union(tower2)
          .union(wedge2)
          )

# Optional: Add the specific pentagonal hole seen in the image near the center-right
# The image shows a hole, let's cut it through the platform
hole_shape = (cq.Workplane("XY")
              .workplane(offset=top_surface)
              .center(12, 5)
              .polygon(5, 6.0) # 5 sides, diameter
              .extrude(-20) # Cut downwards
              )

# Apply the cut
result = result.cut(hole_shape)

# Export or display logic is handled by the environment, 
# but 'result' is the variable required.