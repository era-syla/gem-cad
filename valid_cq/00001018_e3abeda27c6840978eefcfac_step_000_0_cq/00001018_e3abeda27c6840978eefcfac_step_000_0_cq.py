import cadquery as cq

# Parametric dimensions
# Main block dimensions
main_block_width = 30.0
main_block_depth = 30.0
main_block_height = 60.0

# Side mechanism base dimensions
side_base_width = 25.0  # Extension from the main block
side_base_depth = 15.0
side_base_thickness = 4.0
side_base_z_offset = 10.0 # From the bottom of the main block (relative) - actually it looks mid-height

# Contact block (the L-shaped part on top of the base)
contact_block_width = 12.0
contact_block_depth = side_base_depth
contact_block_height = 6.0

# Small detailed block at the end
end_block_width = 6.0
end_block_depth = side_base_depth
end_block_height = 8.0

# Spring/Wire dimensions
wire_radius = 0.5

# Create the main large block
# Centered on XY, but Z starts from 0 for easier referencing
main_block = cq.Workplane("XY").box(main_block_width, main_block_depth, main_block_height)

# Create the side attachment base
# We want to attach it to the right face (+X) of the main block
# It sits somewhat in the middle vertically
side_assembly_center_z = 0 # Relative to main block center

# 1. The flat plate extending out
plate = (cq.Workplane("XY")
         .workplane(offset=side_assembly_center_z)
         .center(main_block_width/2 + side_base_width/2, 0)
         .box(side_base_width, side_base_depth, side_base_thickness))

# 2. The block on top of the plate (with holes)
# Positioned at the end of the plate
top_block_x_center = main_block_width/2 + side_base_width - contact_block_width/2
top_block = (cq.Workplane("XY")
             .workplane(offset=side_assembly_center_z + side_base_thickness/2 + contact_block_height/2)
             .center(top_block_x_center, 0)
             .box(contact_block_width, contact_block_depth, contact_block_height))

# Add holes to the top block
# One large hole, one small hole
top_block = (top_block.faces(">Z").workplane()
             .center(-2, 0) # Slightly offset
             .hole(3.0) # Large hole
             .center(4, 2) # Offset for small hole
             .hole(1.0))

# 3. The vertical block at the very end (actuator/stop)
end_block_x_center = main_block_width/2 + side_base_width - end_block_width/2
end_stop = (cq.Workplane("XY")
            .workplane(offset=side_assembly_center_z + side_base_thickness/2 + end_block_height/2)
            .center(end_block_x_center + 3, 0) # Shifted slightly further out
            .box(end_block_width, end_block_depth, end_block_height + 4))

# 4. The spring wire
# This is a complex 3D path. We will approximate it with a spline or polyline sweep.
# Path points: Start near main block, loop up, go down to contact block.
start_pt = (main_block_width/2 + 2, 0, side_assembly_center_z + side_base_thickness/2)
mid_pt_1 = (main_block_width/2 + 8, 0, side_assembly_center_z + side_base_thickness/2 + 5)
mid_pt_2 = (main_block_width/2 + 14, 0, side_assembly_center_z + side_base_thickness/2 + 2)
end_pt = (main_block_width/2 + 18, 0, side_assembly_center_z + side_base_thickness/2 + contact_block_height)

path_pts = [start_pt, mid_pt_1, mid_pt_2]

# Creating a wire path
wire_path = cq.Workplane("XY").moveTo(*start_pt[:2]).workplane(offset=start_pt[2])
wire_path = wire_path.spline(path_pts, includeCurrent=True)

# Just modeling the wire as a simple bent shape for robustness if spline fails in some viewers
# Let's try a simple Polyline sweep path
p1 = (main_block_width/2, 0, side_assembly_center_z + side_base_thickness/2)
p2 = (main_block_width/2 + 8, 0, side_assembly_center_z + side_base_thickness/2 + 6)
p3 = (main_block_width/2 + 15, 0, side_assembly_center_z + side_base_thickness/2 + contact_block_height)

# Create a solid wire using a sweep along a generated path
# Define the path on the XZ plane roughly
path = (cq.Workplane("XZ")
        .moveTo(p1[0], p1[2])
        .spline([(p2[0], p2[2]), (p3[0], p3[2])], tangents=[(1, 0.5), (1, -1)]))

# Define the profile to sweep (circle)
wire_solid = (cq.Workplane("YZ")
              .workplane(offset=p1[0])
              .moveTo(p1[2], p1[1]) # Coordinates in local system can be tricky, centering usually works best
              .circle(wire_radius)
              .sweep(path, isFrenet=True))

# There is also a small block "under" the main side mechanism, attached to the main body
# It looks like a support or another component housing
lower_block_height = 20.0
lower_block_z = -main_block_height/2 + lower_block_height/2
lower_side_block = (cq.Workplane("XY")
                    .workplane(offset=lower_block_z)
                    .center(main_block_width/2 + 3, 0)
                    .box(6, side_base_depth, lower_block_height))


# Combine all parts
result = (main_block
          .union(plate)
          .union(top_block)
          .union(end_stop)
          .union(lower_side_block)
          .union(wire_solid)
          )

# Export or display
# cq.exporters.export(result, "model.step")