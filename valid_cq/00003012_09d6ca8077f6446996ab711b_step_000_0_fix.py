import cadquery as cq

# Main plate dimensions
plate_w = 100
plate_h = 80
plate_t = 8

# Create the main rectangular plate
result = cq.Workplane("XY").rect(plate_w, plate_h).extrude(plate_t)

# Cut stair steps on the left side (bottom-left corner steps)
# Steps go from bottom-left going up-right
step_w = 10
step_h = 10

for i in range(4):
    x_cut = -plate_w/2 + i * step_w
    y_cut = -plate_h/2 + i * step_h
    cut_w = plate_w - i * step_w
    cut_h = plate_h - i * step_h
    # Cut the bottom-left stair
    result = result.cut(
        cq.Workplane("XY")
        .box(step_w * (4 - i), step_h, plate_t + 2)
        .translate((x_cut + step_w * (4 - i) / 2 - plate_w/2 + step_w * i / 2 - plate_w/2 + (step_w * i + step_w * (4 - i)) / 2 - plate_w/2, 
                    -plate_h/2 + i * step_h / 2, plate_t/2))
    )

# Let me redo this more carefully
# Rebuild from scratch with proper stair cuts

result = cq.Workplane("XY").rect(plate_w, plate_h).extrude(plate_t)

# Left-side staircase: cut progressively larger rectangles from left
# Step 1: bottom row
for i in range(4):
    step_cut_w = (4 - i) * step_w
    step_cut_h = step_h
    x_center = -plate_w/2 + step_cut_w/2
    y_center = -plate_h/2 + i * step_h + step_h/2
    result = result.cut(
        cq.Workplane("XY")
        .box(step_cut_w, step_cut_h, plate_t + 2)
        .translate((x_center, y_center, plate_t/2))
    )

# Top-right staircase (teeth/serrations) on top-right
# Small teeth along top-right edge
tooth_w = 8
tooth_h = 8
num_teeth = 4

for i in range(num_teeth):
    x_center = plate_w/2 - (i + 0.5) * tooth_w
    y_center = plate_h/2 - tooth_h * (num_teeth - i) / 2
    # Cut teeth from top
    for j in range(num_teeth - i):
        tx = plate_w/2 - (i + 0.5) * tooth_w
        ty = plate_h/2 - (j + 0.5) * tooth_h
        result = result.cut(
            cq.Workplane("XY")
            .box(tooth_w, tooth_h, plate_t + 2)
            .translate((tx, ty, plate_t/2))
        )

# Now add the holes
# Large hole - left center area
result = result.cut(
    cq.Workplane("XY").circle(16).extrude(plate_t + 2).translate((-28, -8, -1))
)

# Large hole - top center
result = result.cut(
    cq.Workplane("XY").circle(16).extrude(plate_t + 2).translate((5, 15, -1))
)

# Medium hole - bottom center-right
result = result.cut(
    cq.Workplane("XY").circle(12).extrude(plate_t + 2).translate((10, -18, -1))
)

# Small hole - right side upper
result = result.cut(
    cq.Workplane("XY").circle(7).extrude(plate_t + 2).translate((32, 15, -1))
)

# Tiny hole - far right
result = result.cut(
    cq.Workplane("XY").circle(4).extrude(plate_t + 2).translate((42, 20, -1))
)

# Countersink/recess for large holes (pockets)
result = result.cut(
    cq.Workplane("XY").circle(20).extrude(3).translate((-28, -8, plate_t - 3))
)
result = result.cut(
    cq.Workplane("XY").circle(20).extrude(3).translate((5, 15, plate_t - 3))
)
result = result.cut(
    cq.Workplane("XY").circle(15).extrude(3).translate((10, -18, plate_t - 3))
)
result = result.cut(
    cq.Workplane("XY").circle(9).extrude(3).translate((32, 15, plate_t - 3))
)