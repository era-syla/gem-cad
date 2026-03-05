import cadquery as cq
import math

# Gear and dimension parameters
num_teeth = 40
outer_radius = 50.0
root_radius = 42.0
thickness = 15.0

bore_diameter = 20.0
bolt_circle_radius = 26.0
bolt_hole_diameter = 8.0
num_bolt_holes = 4

# Calculated parameters for tooth profile
pitch_angle = 360.0 / num_teeth

# Generate 2D points for the gear profile
pts = []
for i in range(num_teeth):
    center_angle = i * pitch_angle

    # Angles for trapezoidal approximation of an involute gear tooth
    root_left = math.radians(center_angle - 2.8)
    tip_left = math.radians(center_angle - 1.2)
    tip_right = math.radians(center_angle + 1.2)
    root_right = math.radians(center_angle + 2.8)
    valley_mid = math.radians(center_angle + 4.5)

    # Append points for the current tooth
    pts.append((root_radius * math.cos(root_left), root_radius * math.sin(root_left)))
    pts.append((outer_radius * math.cos(tip_left), outer_radius * math.sin(tip_left)))
    pts.append((outer_radius * math.cos(tip_right), outer_radius * math.sin(tip_right)))
    pts.append((root_radius * math.cos(root_right), root_radius * math.sin(root_right)))
    pts.append((root_radius * math.cos(valley_mid), root_radius * math.sin(valley_mid)))

# Create the base solid gear shape by extruding the 2D profile
gear = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# Cut the central bore
gear = gear.faces(">Z").workplane().hole(bore_diameter)

# Cut the bolt pattern holes
result = (
    gear.faces(">Z")
    .workplane()
    .polarArray(bolt_circle_radius, 0, 360, num_bolt_holes)
    .hole(bolt_hole_diameter)
)