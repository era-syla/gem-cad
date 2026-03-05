import cadquery as cq
import math

# This appears to be a spanner/wrench with a curved jaw (C-shaped arc) and a cylindrical handle

# Parameters
outer_radius = 50  # outer radius of the arc jaw
inner_radius = 38  # inner radius of the arc jaw
arc_angle = 240    # degrees of arc
jaw_height = 8     # height/thickness of the jaw
handle_length = 60
handle_radius = 6
hub_size = 12      # central hub connecting jaw to handle

# Create the arc jaw as a swept profile
# The jaw is a curved band - create it by making an annular sector

def make_arc_jaw(outer_r, inner_r, angle_deg, height):
    # Create arc jaw using revolve of a rectangle
    # Rectangle cross-section swept around partial arc
    arc_width = outer_r - inner_r
    mid_r = (outer_r + inner_r) / 2
    
    # Make a rectangle and revolve it partially
    jaw = (
        cq.Workplane("XZ")
        .transformed(offset=(inner_r, 0, 0))
        .rect(arc_width, height, centered=True)
        .revolve(angle_deg, (0, 0, 0), (0, 0, 1))
    )
    return jaw

# The arc spans about 240 degrees, starting from one side
# Position: arc opens toward bottom-left, handle goes to lower-right

# Create the main arc jaw
jaw = (
    cq.Workplane("XZ")
    .transformed(offset=(inner_radius + (outer_radius - inner_radius)/2, 0, 0))
    .rect(outer_radius - inner_radius, jaw_height)
    .revolve(arc_angle, (-(inner_radius + (outer_radius - inner_radius)/2), 0, 0), 
             (-(inner_radius + (outer_radius - inner_radius)/2), 0, 1))
)

# Simpler approach: build arc jaw directly
mid_r = (outer_radius + inner_radius) / 2

jaw = (
    cq.Workplane("XZ")
    .move(inner_radius, 0)
    .rect(outer_radius - inner_radius, jaw_height)
    .revolve(arc_angle, (0, 0, 0), (0, 0, 1))
)

# Create central hub (box connecting jaw to handle)
hub = (
    cq.Workplane("XY")
    .box(hub_size * 2, hub_size * 2, jaw_height)
)

# Create handle (cylinder extending from hub)
handle = (
    cq.Workplane("YZ")
    .transformed(offset=(handle_length/2, 0, 0))
    .circle(handle_radius)
    .extrude(handle_length)
)

# Reposition handle to extend from hub
handle = (
    cq.Workplane("YZ")
    .circle(handle_radius)
    .extrude(handle_length)
    .translate((handle_length/2 + hub_size, 0, 0))
)

# Combine all parts
# First union hub and jaw
result = jaw.union(hub)

# Add handle
result = result.union(handle)

# Add small ball/knob at the end of the arc
knob_angle = arc_angle
knob_x = outer_radius * math.cos(math.radians(knob_angle))
knob_y = outer_radius * math.sin(math.radians(knob_angle))

knob = (
    cq.Workplane("XY")
    .transformed(offset=(knob_x, 0, knob_y))
    .sphere(5)
)

result = result.union(knob)

# Apply some fillets to smooth edges
try:
    result = result.edges("|Y").fillet(2)
except:
    pass