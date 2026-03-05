import cadquery as cq

# Sheet metal bracket with S-curve profile
# Thickness of the sheet metal
t = 3.0

# Create the main bracket profile using a 2D sketch then extrude
# The bracket has:
# - A bottom foot/base flange (horizontal, pointing forward)
# - A vertical lower section
# - An S-curve transition
# - A large main plate section with holes
# - An upper S-curve
# - A top mounting flange

width = 50.0  # width of bracket (extrusion depth)

# Build the profile as a series of connected points in the XZ plane
# Bottom to top, describing the outer edge, then back along inner edge

# Profile points (outer edge of sheet metal, 2D in XZ plane)
# Origin at bottom-left of foot

# Key dimensions
foot_length = 30.0      # horizontal foot length
foot_height = t         # foot thickness
lower_vert_h = 40.0    # lower vertical section height
s_curve_h = 20.0       # height of s-curve transition
main_plate_h = 80.0    # main plate height
upper_curve_h = 20.0   # upper s-curve height
top_flange = 35.0      # top flange length
step_back = 20.0       # how far back the s-curves offset

# Build profile using workplane and polyline/spline approach
# Simpler: use a wire path and extrude

# Define 2D profile points (x=horizontal, y=vertical)
# Outer profile (front face)
pts_outer = [
    (0, 0),                                    # bottom-left of foot
    (foot_length, 0),                          # bottom-right of foot
    (foot_length, foot_height),               # top-right of foot step
    (t, foot_height),                          # inner edge of foot
    (t, foot_height + lower_vert_h),          # top of lower vertical
    # s-curve going back (positive x direction)
    (t + step_back, foot_height + lower_vert_h + s_curve_h),  # after s-curve
    (t + step_back, foot_height + lower_vert_h + s_curve_h + main_plate_h),  # top of main plate
    # upper s-curve going back further
    (step_back, foot_height + lower_vert_h + s_curve_h + main_plate_h + upper_curve_h),
    (step_back, foot_height + lower_vert_h + s_curve_h + main_plate_h + upper_curve_h + foot_height),
    (step_back + top_flange, foot_height + lower_vert_h + s_curve_h + main_plate_h + upper_curve_h + foot_height),
    (step_back + top_flange, foot_height + lower_vert_h + s_curve_h + main_plate_h + upper_curve_h),
    (step_back + t, foot_height + lower_vert_h + s_curve_h + main_plate_h + upper_curve_h),
    (step_back + t, foot_height + lower_vert_h + s_curve_h + main_plate_h),
    # back down s-curve
    (t + step_back + t, foot_height + lower_vert_h + s_curve_h + main_plate_h),
    (t + step_back + t, foot_height + lower_vert_h + s_curve_h),
    (2*t, foot_height + lower_vert_h + s_curve_h),
    (2*t, foot_height + lower_vert_h),
    (t + step_back + t, foot_height + lower_vert_h),
    (t + step_back + t, foot_height),
    (foot_length + t, foot_height),
    (foot_length + t, 0),
    (foot_length + t + t, 0),
    (foot_length + t + t, foot_height + t),
    (0, foot_height + t),
]

# Use a simpler approach - build solid box-based shapes and union them

# Bottom foot (horizontal base plate)
foot = (cq.Workplane("XY")
        .box(foot_length, width, t)
        .translate((foot_length/2, width/2, t/2))
        )

# Lower vertical riser
riser = (cq.Workplane("XY")
         .box(t, width, lower_vert_h)
         .translate((t/2, width/2, t + lower_vert_h/2))
         )

# Main diagonal/s-curve plate - approximate as vertical plate offset
main_plate = (cq.Workplane("XY")
              .box(t, width, main_plate_h + s_curve_h + upper_curve_h)
              .translate((t + step_back + t/2, width/2, t + lower_vert_h + (main_plate_h + s_curve_h + upper_curve_h)/2))
              )

# S-curve connectors (simplified as angled boxes)
total_h = t + lower_vert_h + s_curve_h + main_plate_h + upper_curve_h

# Lower s-curve connector
lower_conn = (cq.Workplane("XY")
              .box(step_back + t, width, t)
              .translate((t + (step_back + t)/2, width/2, t + lower_vert_h + t/2))
              )

# Upper s-curve connector  
upper_h_pos = t + lower_vert_h + s_curve_h + main_plate_h
upper_conn = (cq.Workplane("XY")
              .box(step_back + t, width, t)
              .translate((t/2 + (step_back + t)/2 - step_back/2, width/2, upper_h_pos + t/2))
              )

# Top flange
top_flange_solid = (cq.Workplane("XY")
                    .box(top_flange + t, width, t)
                    .translate((step_back + t + (top_flange + t)/2 - t, width/2, upper_h_pos + t + t/2))
                    )

# Right side foot (small L at bottom right)
right_foot = (cq.Workplane("XY")
              .box(t, width, t)
              .translate((foot_length + t + t/2, width/2, t/2))
              )

# Combine all parts
result = (foot
          .union(riser)
          .union(main_plate)
          .union(lower_conn)
          .union(upper_conn)
          .union(top_flange_solid)
          .union(right_foot)
          )

# Add holes to main plate area
# Large center hole
hole_x = t + step_back + t/2
hole_z1 = t + lower_vert_h + s_curve_h + main_plate_h * 0.4

result = (result
          .faces(">Z")
          .workplane()
          )

# Cut holes using box subtraction approach
hole_r = 8.0
small_r = 3.0

# Main large hole
cyl1 = cq.Workplane("XY").cylinder(width + 2, hole_r).rotate((0,0,0),(1,0,0),90).translate((hole_x, -1, hole_z1))
# Small holes
cyl2 = cq.Workplane("XY").cylinder(width + 2, small_r).rotate((0,0,0),(1,0,0),90).translate((hole_x - 12, -1, hole_z1 + 25))
cyl3 = cq.Workplane("XY").cylinder(width + 2, small_r).rotate((0,0,0),(1,0,0),90).translate((hole_x + 12, -1, hole_z1 - 20))

# Top flange slot
slot_x = step_back + t + top_flange * 0.5
slot_z = upper_h_pos + t + t/2
slot = cq.Workplane("XY").box(12, 5, t + 2).translate((slot_x, width/2, slot_z))

# Bottom foot hole
bot_hole = cq.Workplane("XY").cylinder(width+2, small_r).rotate((0,0,0),(1,0,0),90).translate((foot_length*0.6, -1, t/2+1))

result = (result
          .cut(cyl1)
          .cut(cyl2)
          .cut(cyl3)
          .cut(slot)
          .cut(bot_hole)
          )