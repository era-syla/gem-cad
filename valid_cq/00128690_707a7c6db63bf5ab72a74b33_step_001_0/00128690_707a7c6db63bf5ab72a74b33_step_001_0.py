import cadquery as cq
import math

# --- Parameters ---
star_outer_radius = 50.0
star_inner_radius = 24.0  # Slightly less than half creates a nice star shape
star_thickness = 4.0
star_points_count = 5

text_content = "Elias"
text_size = 16.0
text_depth = 1.5         # Depth of the text cut
text_font = "Arial"      # Standard sans-serif font

# --- Geometry Generation ---

# Calculate vertices for the star
points = []
# Start at 90 degrees (top point) so the star stands upright
start_angle = 90.0
# Total steps is 2 * number of points (outer + inner vertices)
total_steps = star_points_count * 2
angle_step = 360.0 / total_steps

for i in range(total_steps):
    # Alternate between outer and inner radius
    r = star_outer_radius if i % 2 == 0 else star_inner_radius
    
    # Calculate coordinates
    angle_rad = math.radians(start_angle + i * angle_step)
    x = r * math.cos(angle_rad)
    y = r * math.sin(angle_rad)
    points.append((x, y))

# Create the base star solid
# Draw polyline, close it, and extrude
base_star = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(star_thickness)
)

# Create the text feature
# Select the top face, create a workplane, and cut the text
result = (
    base_star
    .faces(">Z")
    .workplane()
    .text(
        text_content, 
        fontsize=text_size, 
        distance=-text_depth, # Negative distance to cut into the material
        cut=True, 
        font=text_font,
        halign="center", 
        valign="center"
    )
)