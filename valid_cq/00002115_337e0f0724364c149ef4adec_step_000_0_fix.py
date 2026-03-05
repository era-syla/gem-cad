import cadquery as cq

# Parameters
bar_w = 4       # cross-section width of square bars
bar_h = 4       # cross-section height
frame_length = 200  # length of the long horizontal bars
frame_width = 60    # width between the two long bars
post_height = 80    # height of vertical posts
base_length = 80    # length of base feet

# Build the structure as a union of rectangular bars

def make_bar(length, width, height):
    return cq.Workplane("XY").box(length, width, height)

# Two long horizontal rails along X axis
rail_y_offset = frame_width / 2

rail1 = (cq.Workplane("XY")
         .center(0, rail_y_offset)
         .box(frame_length, bar_w, bar_h))

rail2 = (cq.Workplane("XY")
         .center(0, -rail_y_offset)
         .box(frame_length, bar_w, bar_h))

# Two cross members along Y axis at each end
cross_offset = frame_length / 2 - bar_w / 2

cross1 = (cq.Workplane("XY")
          .center(-cross_offset, 0)
          .box(bar_w, frame_width + bar_w * 2 + base_length, bar_h))

cross2 = (cq.Workplane("XY")
          .center(cross_offset, 0)
          .box(bar_w, frame_width + bar_w * 2 + base_length, bar_h))

# Vertical posts at each end, rising from the cross members
post_z_center = bar_h / 2 + post_height / 2

post1 = (cq.Workplane("XY")
         .center(-cross_offset, 0)
         .workplane(offset=bar_h)
         .box(bar_w, bar_w, post_height))

post2 = (cq.Workplane("XY")
         .center(cross_offset, 0)
         .workplane(offset=bar_h)
         .box(bar_w, bar_w, post_height))

# Base feet (horizontal bars at bottom of posts, along Y direction extended outward)
# Each end has a T-foot: the cross member already extends, but we add foot pads along X
foot_z = 0  # sitting on ground plane

# Left end feet along Y - already part of cross1, but add feet along X direction
foot1_left = (cq.Workplane("XY")
              .center(-cross_offset, (frame_width / 2 + bar_w / 2 + base_length / 4))
              .box(base_length, bar_w, bar_h))

foot1_right = (cq.Workplane("XY")
               .center(-cross_offset, -(frame_width / 2 + bar_w / 2 + base_length / 4))
               .box(base_length, bar_w, bar_h))

foot2_left = (cq.Workplane("XY")
              .center(cross_offset, (frame_width / 2 + bar_w / 2 + base_length / 4))
              .box(base_length, bar_w, bar_h))

foot2_right = (cq.Workplane("XY")
               .center(cross_offset, -(frame_width / 2 + bar_w / 2 + base_length / 4))
               .box(base_length, bar_w, bar_h))

# Combine all parts
result = (rail1
          .union(rail2)
          .union(cross1)
          .union(cross2)
          .union(post1)
          .union(post2)
          .union(foot1_left)
          .union(foot1_right)
          .union(foot2_left)
          .union(foot2_right))