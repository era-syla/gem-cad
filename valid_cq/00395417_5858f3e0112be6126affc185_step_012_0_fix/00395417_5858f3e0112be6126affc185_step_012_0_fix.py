import cadquery as cq
import math

num_teeth = 12
module = 2.5
pitch_diameter = num_teeth * module
pitch_radius = pitch_diameter / 2
addendum = module
dedendum = 1.25 * module
root_radius = pitch_radius - dedendum
outer_radius = pitch_radius + addendum

span_teeth = 8
angular_pitch = 360.0 / num_teeth
angle_span = span_teeth * angular_pitch
half_span = angle_span / 2.0

thickness = 8.0
hole_diameter = 6.0

# Create the base segment (from root circle to outer circle)
points = [
    (root_radius * math.cos(math.radians(-half_span)), root_radius * math.sin(math.radians(-half_span))),
    (outer_radius * math.cos(math.radians(-half_span)), outer_radius * math.sin(math.radians(-half_span))),
    (outer_radius * math.cos(math.radians(half_span)),  outer_radius * math.sin(math.radians(half_span))),
    (root_radius * math.cos(math.radians(half_span)),  root_radius * math.sin(math.radians(half_span))),
]

result = cq.Workplane("XY").polyline(points).close().extrude(thickness)

# Approximate teeth as simple rectangular extrusions
tooth_height = outer_radius - root_radius
# approximate tooth width along arc (reduce a bit for clearance)
tooth_width = angular_pitch * math.pi * pitch_radius / num_teeth * 0.6

for i in range(span_teeth):
    angle = -half_span + angular_pitch * (i + 0.5)
    tooth = (
        cq.Workplane("XY")
          .transformed(rotate=(0, 0, angle))
          .center(root_radius + tooth_height/2, 0)
          .rect(tooth_height, tooth_width)
          .extrude(thickness)
    )
    result = result.union(tooth)

# Drill a central hole
result = result.faces(">Z").workplane().hole(hole_diameter)