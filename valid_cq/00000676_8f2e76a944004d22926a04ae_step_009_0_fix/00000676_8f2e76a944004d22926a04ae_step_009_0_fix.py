import cadquery as cq
import math

# Parameters
ramp_length = 200
ramp_width = 20
ramp_thickness = 2
quarter_pipe_radius = 40
quarter_pipe_width = 20
support_height = 35
support_thickness = 2

# Create the flat ramp section
flat_ramp = (
    cq.Workplane("XY")
    .box(ramp_length, ramp_width, ramp_thickness)
    .translate((-ramp_length/2, 0, ramp_thickness/2))
)

# Create quarter pipe surface using loft
# The quarter pipe transitions from the end of the flat ramp (horizontal) to vertical
num_sections = 8
angle_step = 90.0 / num_sections

quarter_sections = []
for i in range(num_sections + 1):
    angle_rad = math.radians(i * angle_step)
    x = quarter_pipe_radius * math.sin(angle_rad)
    z = quarter_pipe_radius * (1 - math.cos(angle_rad))
    # Each section is a rectangle in the width direction
    quarter_sections.append((x, z))

# Build quarter pipe as a shell using sweep along a curved path
# Use a series of thin boxes to approximate the quarter pipe
result_quarter = cq.Workplane("XY")

# Create the quarter pipe by revolving a profile
# Profile: a thin rectangle representing the pipe surface
quarter_pipe = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, 0, 0))
    .moveTo(0, 0)
    .lineTo(ramp_thickness, 0)
    .lineTo(ramp_thickness, quarter_pipe_width)
    .lineTo(0, quarter_pipe_width)
    .close()
    .extrude(ramp_thickness)
)

# Better approach: create quarter pipe as a swept solid
# Create a 2D arc path in XZ plane and sweep a rectangle cross-section

# Quarter pipe main surface
wp = cq.Workplane("XZ")
path = (
    wp.moveTo(0, quarter_pipe_radius)
    .radiusArc((quarter_pipe_radius, 0), -quarter_pipe_radius)
    .val()
)

profile = (
    cq.Workplane("YZ")
    .rect(ramp_width, ramp_thickness)
)

quarter_surface = profile.sweep(path)

# Position quarter pipe at origin (bottom of curve)
quarter_surface = quarter_surface.translate((0, 0, quarter_pipe_radius))

# Create the flat ramp
flat_ramp = (
    cq.Workplane("XY")
    .box(ramp_length, ramp_width, ramp_thickness)
    .translate((-ramp_length/2 - quarter_pipe_radius, 0, quarter_pipe_radius + ramp_thickness/2))
)

# Create support structure under quarter pipe
# Vertical supports
supports = []
support_positions = [
    (quarter_pipe_radius * 0.3, 0),
    (quarter_pipe_radius * 0.6, 0),
    (quarter_pipe_radius * 0.9, 0),
]

support_assembly = cq.Workplane("XY").box(support_thickness, ramp_width * 0.8, 1)

for sx, sy in support_positions:
    angle_rad = math.asin(sx / quarter_pipe_radius)
    sz = quarter_pipe_radius * (1 - math.cos(angle_rad))
    h = sz + quarter_pipe_radius - sz
    if h < 1:
        h = 1
    h = quarter_pipe_radius - sz
    if h > 1:
        sup = (
            cq.Workplane("XY")
            .box(support_thickness, ramp_width * 0.6, h)
            .translate((sx, 0, h/2))
        )
        supports.append(sup)

# Diagonal cross braces
diag1 = (
    cq.Workplane("XZ")
    .box(support_thickness, support_thickness, math.sqrt(quarter_pipe_radius**2 + quarter_pipe_radius**2))
    .rotate((0, 0, 0), (0, 1, 0), 45)
    .translate((quarter_pipe_radius/2, 0, quarter_pipe_radius/2))
)

# Combine everything
result = flat_ramp.union(quarter_surface)

for sup in supports:
    result = result.union(sup)

# Add vertical end support
end_support = (
    cq.Workplane("XY")
    .box(support_thickness, ramp_width * 0.8, quarter_pipe_radius)
    .translate((quarter_pipe_radius, 0, quarter_pipe_radius/2))
)

result = result.union(end_support)