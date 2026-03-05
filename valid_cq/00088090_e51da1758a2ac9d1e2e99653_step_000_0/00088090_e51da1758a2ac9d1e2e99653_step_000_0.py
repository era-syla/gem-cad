import cadquery as cq

# ==========================================
# Parameters (Estimated from Image)
# ==========================================

# Overall Dimensions
total_length = 240.0
main_diameter = 10.0   # Diameter for both smooth shaft and thread major
flange_diameter = 18.0
flange_thickness = 4.0

# Section Lengths
# Threaded section appears to be slightly more than half the length
thread_length = 130.0
# Calculate smooth shaft length based on total
smooth_shaft_total_length = total_length - thread_length - flange_thickness

# Tip Detail Dimensions (Left End)
hole_diameter = 3.0
hole_distance_from_tip = 15.0
groove_width = 1.2
groove_diameter = 8.5      # Slightly smaller than main diameter
groove_distance_from_tip = 5.0
tip_chamfer = 1.0

# ==========================================
# 3D Model Construction
# ==========================================

# Strategy: Build the part in segments along the X-axis starting from X=0 (Left Tip)

# 1. Tip Segment (Before Groove)
# A short cylinder at the very tip
tip_segment = (cq.Workplane("YZ")
               .circle(main_diameter / 2.0)
               .extrude(groove_distance_from_tip))

# 2. Groove Segment
# A smaller diameter cylinder for the retaining ring groove
groove_segment = (cq.Workplane("YZ")
                  .workplane(offset=groove_distance_from_tip)
                  .circle(groove_diameter / 2.0)
                  .extrude(groove_width))

# 3. Main Smooth Shaft Segment
# The rest of the smooth shaft up to the flange
shaft_start_pos = groove_distance_from_tip + groove_width
shaft_segment_length = smooth_shaft_total_length - shaft_start_pos

shaft_segment = (cq.Workplane("YZ")
                 .workplane(offset=shaft_start_pos)
                 .circle(main_diameter / 2.0)
                 .extrude(shaft_segment_length))

# 4. Flange (Collar)
# Larger diameter disc separating shaft and threads
flange_start_pos = smooth_shaft_total_length
flange = (cq.Workplane("YZ")
          .workplane(offset=flange_start_pos)
          .circle(flange_diameter / 2.0)
          .extrude(flange_thickness))

# 5. Threaded Section
# Cylinder representing the threaded rod (Major diameter)
thread_start_pos = flange_start_pos + flange_thickness
thread_segment = (cq.Workplane("YZ")
                  .workplane(offset=thread_start_pos)
                  .circle(main_diameter / 2.0)
                  .extrude(thread_length))

# Union all segments into a single solid
result = tip_segment.union(groove_segment).union(shaft_segment).union(flange).union(thread_segment)

# ==========================================
# Features and Machining
# ==========================================

# 6. Cross Hole
# Cut a hole perpendicular to the shaft axis near the tip
# We use the XZ plane (Y=0) to place the circle center, then extrude cut along Y
result = result.cut(
    cq.Workplane("XZ")
    .center(hole_distance_from_tip, 0)  # X = distance, Z = 0 (axis center)
    .circle(hole_diameter / 2.0)
    .extrude(flange_diameter, both=True) # Extrude through the part
)

# 7. Chamfers
# Add chamfers to the start and end of the rod
result = result.faces("<X").chamfer(tip_chamfer) # Left tip
result = result.faces(">X").chamfer(tip_chamfer) # Right threaded end