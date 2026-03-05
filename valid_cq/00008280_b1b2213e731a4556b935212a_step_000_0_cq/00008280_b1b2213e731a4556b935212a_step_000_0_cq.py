import cadquery as cq

# --- Parametric Dimensions ---
# Standard LEGO dimensions (approximate) in millimeters
stud_pitch = 8.0     # Distance between stud centers
brick_width = 2 * stud_pitch
brick_length = 3 * stud_pitch
brick_height = 9.6   # Standard brick height (excluding studs)
stud_diameter = 4.8
stud_height = 1.7
wall_thickness = 1.2

# --- Modeling ---

# 1. Create the main brick body
# We create a box centered on XY, sitting on Z=0
brick = cq.Workplane("XY").box(brick_length, brick_width, brick_height)

# 2. Create the studs on top
# We define a grid of points on the top face of the brick
stud_locations = []

# Calculate starting positions to center the 2x3 grid
# x coordinates: -pitch, 0, +pitch
# y coordinates: -pitch/2, +pitch/2
x_start = -stud_pitch
y_start = -stud_pitch / 2

for i in range(3): # 3 columns
    for j in range(2): # 2 rows
        x_pos = x_start + (i * stud_pitch)
        y_pos = y_start + (j * stud_pitch)
        stud_locations.append((x_pos, y_pos))

# Select the top face and extrude the studs
result = (brick.faces(">Z").workplane()
          .pushPoints(stud_locations)
          .circle(stud_diameter / 2)
          .extrude(stud_height))

# 3. Hollow out the bottom (Optional but typical for this shape)
# While the image view is top-down, a true brick is hollow.
# Since the prompt asks for the "model based on the image", the top view is critical.
# However, adding a shell makes it a valid "brick".
# If we strictly stick to visual surface geometry from the top, just the box + studs is enough.
# But for a "good" CAD model, shelling is better practice.
# Let's stick to the visual representation which implies a solid block unless seen otherwise,
# but usually, these scripts are better if they produce a shell. 
# To be safe and strictly follow the "visual" prompt which shows a solid-looking object from the top,
# I will leave it solid to ensure the code creates exactly what is seen without assuming internal geometry.
# (If I shelled it, it wouldn't change the top view, but might complicate the simple request).

# Final Result
result = result