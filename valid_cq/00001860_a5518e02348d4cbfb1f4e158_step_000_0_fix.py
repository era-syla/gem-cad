import cadquery as cq

# Dimensions
width = 40      # X dimension
depth = 25      # Y dimension
total_height = 80  # Z dimension

# Bottom block
bottom_h = 15
bottom = cq.Workplane("XY").rect(width, depth).extrude(bottom_h)

# Middle S-curve section - create profile and extrude
# The S-curve connects bottom block to upper section
# Profile: rectangle with S-curve cutout on front face
# We'll build the S-curve as a 2D profile in XZ plane and extrude in Y

mid_h = 35
mid_bottom_z = bottom_h
mid_top_z = bottom_h + mid_h

# Build the S-curve profile in the XZ plane
# The profile is like a rect but with concave/convex curves on front
# Looking at the image: 
#   - bottom: concave arc (opens upward) 
#   - top: convex arc (bulges forward)
# We'll create a 2D wire profile and extrude it

r = width / 2  # radius = 20

# Profile points for S-curve section (in XZ plane, extruded in Y)
# Left side straight, right side has S-curve shape
# Create profile as a closed wire

# The front face has an S-curve:
# Bottom portion: concave arc (arc curves inward)
# Top portion: convex arc (arc curves outward)

# Build profile on XZ plane (Y=0)
half_w = width / 2

# S-curve profile: 
# bottom arc center at (0, bottom_h + r) - concave opening downward
# top arc center at (0, bottom_h + mid_h - r) - convex bulging up

arc_r = width / 2  # = 20

# Points for the profile:
# We work in a workplane where X is width, Y is height (Z in 3D)

profile = (
    cq.Workplane("XZ")
    .moveTo(-half_w, mid_bottom_z)
    .lineTo(-half_w, mid_top_z)
    .lineTo(half_w, mid_top_z)
    # Top convex arc on right side - arc goes from top-right down
    # Bottom concave arc
    .lineTo(half_w, mid_bottom_z)
    .close()
)

mid_block = profile.extrude(depth)

# Actually, let's do it differently - solid block minus arc cuts

# Full middle block
mid_solid = (cq.Workplane("XY")
    .workplane(offset=bottom_h)
    .rect(width, depth)
    .extrude(mid_h)
)

# Cut bottom concave arc from front face (concave opening upward from bottom)
# Arc center at front face, z = bottom_h + arc_r
cut_bottom = (cq.Workplane("XZ")
    .workplane(offset=depth/2)
    .moveTo(0, bottom_h + arc_r)
    .circle(arc_r)
    .extrude(depth + 2)
)

# Cut top convex: leave convex shape at top
# Actually the top has a convex bump - cut away the area NOT in the bump
# Convex at top means we cut the corners - use a cylinder on outside
cut_top = (cq.Workplane("XZ")
    .workplane(offset=depth/2)
    .moveTo(0, mid_top_z - arc_r)
    .circle(arc_r)
    .extrude(depth + 2)
)

mid_result = mid_solid.cut(cut_bottom)

# Upper shelf/step
shelf_h1 = 8
shelf_h2 = 12
shelf_w = width + 8
shelf_depth = depth + 4

upper_base_z = bottom_h + mid_h

shelf1 = (cq.Workplane("XY")
    .workplane(offset=upper_base_z)
    .rect(shelf_w, shelf_depth)
    .extrude(shelf_h1)
)

shelf2 = (cq.Workplane("XY")
    .workplane(offset=upper_base_z + shelf_h1)
    .rect(width, depth)
    .extrude(shelf_h2)
)

# Combine all
result = (bottom
    .union(mid_result)
    .union(shelf1)
    .union(shelf2)
)