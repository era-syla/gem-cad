import cadquery as cq

# --- Part 1: Slotted Bar ---
# Profile on XZ plane, extruded along Y to align with visual perspective
bar_length = 140
bar = (cq.Workplane("XZ")
       .moveTo(-5, 0).lineTo(5, 0)
       .lineTo(5, 6).lineTo(1.5, 6)
       .lineTo(1.5, 4).lineTo(-1.5, 4)
       .lineTo(-1.5, 6).lineTo(-5, 6)
       .close()
       .extrude(bar_length)
       .translate((0, -bar_length/2, 0)))

# Cut a thin notch to simulate the middle seam visible in the image
notch = cq.Workplane("XY").box(12, 0.2, 6).translate((0, 0, 4))
bar = bar.cut(notch)

# Move the bar to its final layout position
bar = bar.translate((-40, 0, 0))

# --- Part 2: V-Notched Plate with Grooves ---
plate_w = 50
plate_t = 4
h_left = 50
h_right = 80
h_mid = 40
x_mid = 25

# Base plate
plate = (cq.Workplane("XZ")
         .polyline([(0,0), (plate_w,0), (plate_w, h_right), (x_mid, h_mid), (0, h_left)])
         .close()
         .extrude(plate_t))

# Add V-grooves to the front face (+Y face)
# Slopes used to extend the cut polygons beyond the plate boundaries for clean cuts
m_left = (h_left - h_mid) / (0 - x_mid)   # (50 - 40) / -25 = -0.4
m_right = (h_right - h_mid) / (plate_w - x_mid) # (80 - 40) / 25 = 1.6

x_ext_left = -2
x_ext_right = plate_w + 2

for offset in [12, 24, 36]:
    y_mid_off = h_mid - offset
    y_left_off = y_mid_off + m_left * (x_ext_left - x_mid)
    y_right_off = y_mid_off + m_right * (x_ext_right - x_mid)
    
    cut_tool = (cq.Workplane("XZ", origin=(0, plate_t, 0))
                .polyline([
                    (x_ext_left, y_left_off + 0.4),
                    (x_mid, y_mid_off + 0.4),
                    (x_ext_right, y_right_off + 0.4),
                    (x_ext_right, y_right_off - 0.4),
                    (x_mid, y_mid_off - 0.4),
                    (x_ext_left, y_left_off - 0.4)
                ])
                .close()
                .extrude(-1.0)) # Cut 1mm into the front face
    plate = plate.cut(cut_tool)

# Move plate to final position
plate = plate.translate((10, 20, 0))

# --- Part 3: Small Block ---
block = cq.Workplane("XY").box(14, 9, 4).translate((70, 10, 2))

# --- Final Assembly ---
result = bar.union(plate).union(block)