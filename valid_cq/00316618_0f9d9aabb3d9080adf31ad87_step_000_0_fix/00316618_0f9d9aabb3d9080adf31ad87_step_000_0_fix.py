import cadquery as cq

# Parameters
open_end_width = 10
open_end_thickness = 3
ring_outer_diameter = 14
ring_inner_diameter = 10
ring_thickness = 4
handle_width = 6
handle_thickness = 2
handle_length = 30

# Open end
open_end = (cq.Workplane("XY")
            .rect(open_end_width, open_end_thickness)
            .extrude(open_end_thickness))

# Ring end
ring_end = (cq.Workplane("XY")
            .circle(ring_outer_diameter / 2)
            .circle(ring_inner_diameter / 2)
            .extrude(ring_thickness))

# Handle
handle = (cq.Workplane("XZ")
          .rect(handle_length, handle_width)
          .extrude(handle_thickness))

# Position parts
open_end = open_end.translate((-handle_length/2 - open_end_thickness/2, 0, 0))
ring_end = ring_end.translate((handle_length/2 + ring_thickness/2, 0, 0))

# Union parts
result = open_end.union(handle).union(ring_end)