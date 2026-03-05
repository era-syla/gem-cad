import cadquery as cq
import math

# --- Parametric Dimensions ---
outer_radius = 40.0   # Distance from center to the center of tip cylinders
inner_radius = 16.0   # Distance from center to the valleys of the star
thickness = 8.0       # Height of the extrusion
tip_radius = 6.0      # Radius of the cylinders at the star tips
hole_radius = 2.5     # Radius of the blind holes in the tips
hole_depth = 3.0      # Depth of the blind holes

# --- 1. Generate the Star Profile ---
# Calculate vertices for a 6-pointed star.
# Points alternate between outer_radius and inner_radius every 30 degrees.
star_points = []
num_points = 12  # 6 tips + 6 valleys
for i in range(num_points):
    angle_deg = i * (360 / num_points)
    angle_rad = math.radians(angle_deg)
    
    # Even indices correspond to tips (0, 60, 120...), odd to valleys (30, 90...)
    r = outer_radius if i % 2 == 0 else inner_radius
    
    x = r * math.cos(angle_rad)
    y = r * math.sin(angle_rad)
    star_points.append((x, y))

# Create the main star body by extruding the profile
star_body = (
    cq.Workplane("XY")
    .polyline(star_points)
    .close()
    .extrude(thickness)
)

# --- 2. Create the Tip Cylinders ---
# Create cylinders at the tip locations (angles 0, 60, 120, etc.)
tips = (
    cq.Workplane("XY")
    .polarArray(radius=outer_radius, startAngle=0, angle=360, count=6)
    .circle(tip_radius)
    .extrude(thickness)
)

# --- 3. Combine Geometry ---
# Union the star body with the tip cylinders
result = star_body.union(tips)

# --- 4. Add Detail Features ---
# Cut blind holes into the top of each tip cylinder
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=outer_radius, startAngle=0, angle=360, count=6)
    .circle(hole_radius)
    .cutBlind(-hole_depth)
)