import cadquery as cq

# Parametric dimensions for the wall/door frame structure
# Overall dimensions
overall_width = 1500.0  # Total width of the assembly
overall_height = 2000.0 # Total height of the assembly
frame_depth = 100.0     # Depth of the wall frame (thickness)
frame_thickness = 40.0  # Thickness of the individual framing members

# Structural details
# The structure is divided into two main sections: a solid paneled section (left) and an open frame section (right).
panel_section_width = overall_width / 2.0
open_section_width = overall_width - panel_section_width
header_height = 200.0   # Height of the top header beam in the open section

# Create the main outline of the left section (Solid Panel / Pocket)
# We start with a solid block and shell it or pocket it out.
# Based on the image, it looks like a frame with a thin backing panel.

# Left Section Construction
left_frame_center = (-open_section_width / 2.0, 0, 0)

# Create the outer rim of the left frame
left_frame_outline = (
    cq.Workplane("XY")
    .rect(panel_section_width, overall_height)
    .extrude(frame_depth)
)

# Cut out the inside to make it a frame
left_frame_cutout = (
    cq.Workplane("XY")
    .rect(panel_section_width - 2 * frame_thickness, overall_height - 2 * frame_thickness)
    .extrude(frame_depth)
)

# Create a thin panel on the "back" side of the left frame (simulating a wall panel or pocket side)
panel_thickness = 10.0
left_panel = (
    cq.Workplane("XY")
    .rect(panel_section_width, overall_height)
    .extrude(panel_thickness)
    .translate((0, 0, -frame_depth/2 + panel_thickness/2)) # Align to back
)

# Combine left frame parts
left_section = left_frame_outline.cut(left_frame_cutout).union(left_panel)
# Move to correct position relative to origin
left_section = left_section.translate((-panel_section_width/2, 0, 0))


# Right Section Construction (Open Frame)
# This consists of top/bottom plates, side studs, and a header.

# Top Plate (full width of right section)
right_top_plate = (
    cq.Workplane("XY")
    .rect(open_section_width, frame_thickness)
    .extrude(frame_depth)
    .translate((open_section_width/2, overall_height/2 - frame_thickness/2, 0))
)

# Bottom Plate (full width of right section)
right_bottom_plate = (
    cq.Workplane("XY")
    .rect(open_section_width, frame_thickness)
    .extrude(frame_depth)
    .translate((open_section_width/2, -overall_height/2 + frame_thickness/2, 0))
)

# Rightmost vertical stud
right_stud = (
    cq.Workplane("XY")
    .rect(frame_thickness, overall_height - 2 * frame_thickness) # Fit between plates
    .extrude(frame_depth)
    .translate((open_section_width - frame_thickness/2, 0, 0))
)

# Middle vertical stud (between left and right sections)
# This often acts as the jamb for the pocket
middle_stud = (
    cq.Workplane("XY")
    .rect(frame_thickness, overall_height - 2 * frame_thickness)
    .extrude(frame_depth)
    .translate((frame_thickness/2, 0, 0))
)

# Header (Horizontal beam below the top plate)
# Positioned down from the top plate
header_y_pos = overall_height/2 - frame_thickness - header_height/2
header = (
    cq.Workplane("XY")
    .rect(open_section_width - 2 * frame_thickness, frame_thickness)
    .extrude(frame_depth)
    .translate((open_section_width/2, header_y_pos, 0))
)

# Additional vertical support inside the pocket opening/header area (as seen in image)
# There appears to be a vertical member extending down from the header, often for door stops or track support
inner_vertical_support_x = frame_thickness * 2.5 # Offset slightly from the middle stud
inner_vertical = (
    cq.Workplane("XY")
    .rect(frame_thickness, overall_height - 2 * frame_thickness) 
    .extrude(frame_depth)
    .translate((inner_vertical_support_x, 0, 0))
)

# In the specific image, there's a wider board/header filling the top area
top_infill_panel = (
    cq.Workplane("XY")
    .rect(open_section_width - 2*frame_thickness, header_height)
    .extrude(frame_thickness) # Thinner, like a board
    .translate((open_section_width/2, overall_height/2 - frame_thickness - header_height/2, frame_depth/2 - frame_thickness/2))
)


# Combine all right section parts
right_section = (
    right_top_plate
    .union(right_bottom_plate)
    .union(right_stud)
    .union(middle_stud)
    .union(header)
    .union(inner_vertical)
    .union(top_infill_panel)
)

# Combine the left and right sections into the final result
result = left_section.union(right_section)

# Optional: Adjust the origin to the bottom center or corner if preferred. 
# Currently centered on the XY plane.