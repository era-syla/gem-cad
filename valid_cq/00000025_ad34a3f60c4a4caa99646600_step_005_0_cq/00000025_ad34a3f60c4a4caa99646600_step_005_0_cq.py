import cadquery as cq
import math

# --- Parameters ---
# Main arc dimensions
inner_radius = 50.0
outer_radius = 65.0
arc_angle = 60.0  # Total angle of the segment
thickness = 6.0   # Vertical height of the main arc

# Tab/Protrusion dimensions
tab_width_angle = 15.0 # Angle spanned by the tab
tab_extension = 10.0   # How far out the tab sticks from outer_radius
tab_thickness = 4.0    # Height of the tab (appears thinner than main body)
tab_vertical_offset = 0.0 # From the bottom

# Mounting holes
hole_diameter = 3.5
hole_angle_offset = 20.0 # From center line

# Fillet radius
fillet_radius = 1.0

# --- Geometry Construction ---

# 1. Create the main curved body
# We sketch on the XY plane. We need an arc segment.
# The easiest way is to create a full annulus and cut it, or sketch the profile and extrude.
# Let's sketch the profile on the XY plane.

# Calculate points for the arc segment
# We'll center the arc on the Y-axis for symmetry
start_angle = 90 - (arc_angle / 2)
end_angle = 90 + (arc_angle / 2)

main_body = (
    cq.Workplane("XY")
    .moveTo(inner_radius * math.cos(math.radians(start_angle)), 
            inner_radius * math.sin(math.radians(start_angle)))
    .lineTo(outer_radius * math.cos(math.radians(start_angle)), 
            outer_radius * math.sin(math.radians(start_angle)))
    .radiusArc((outer_radius * math.cos(math.radians(end_angle)), 
                outer_radius * math.sin(math.radians(end_angle))), 
               -outer_radius) # Negative radius for concave path relative to start
    .lineTo(inner_radius * math.cos(math.radians(end_angle)), 
            inner_radius * math.sin(math.radians(end_angle)))
    .radiusArc((inner_radius * math.cos(math.radians(start_angle)), 
                inner_radius * math.sin(math.radians(start_angle))), 
               inner_radius)
    .close()
    .extrude(thickness)
)

# 2. Create the tab protrusion
# This is another arc segment, extending from outer_radius to outer_radius + tab_extension
# It is centered at angle 90.

tab_start_angle = 90 - (tab_width_angle / 2)
tab_end_angle = 90 + (tab_width_angle / 2)
tab_outer_r = outer_radius + tab_extension

tab_sketch = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start at bottom
    .moveTo(outer_radius * math.cos(math.radians(tab_start_angle)), 
            outer_radius * math.sin(math.radians(tab_start_angle)))
    .lineTo(tab_outer_r * math.cos(math.radians(tab_start_angle)), 
            tab_outer_r * math.sin(math.radians(tab_start_angle)))
    .radiusArc((tab_outer_r * math.cos(math.radians(tab_end_angle)), 
                tab_outer_r * math.sin(math.radians(tab_end_angle))), 
               -tab_outer_r)
    .lineTo(outer_radius * math.cos(math.radians(tab_end_angle)), 
            outer_radius * math.sin(math.radians(tab_end_angle)))
    .radiusArc((outer_radius * math.cos(math.radians(tab_start_angle)), 
                outer_radius * math.sin(math.radians(tab_start_angle))), 
               outer_radius)
    .close()
    .extrude(tab_thickness)
)

# Union the main body and the tab
part = main_body.union(tab_sketch)

# 3. Add Mounting Holes
# We need two holes on top face, symmetric around the center
# Calculate hole positions
hole_r = inner_radius + (outer_radius - inner_radius) / 2
h1_angle = 90 - hole_angle_offset
h1_x = hole_r * math.cos(math.radians(h1_angle))
h1_y = hole_r * math.sin(math.radians(h1_angle))

h2_angle = 90 + hole_angle_offset
h2_x = hole_r * math.cos(math.radians(h2_angle))
h2_y = hole_r * math.sin(math.radians(h2_angle))

part = (
    part.faces(">Z").workplane()
    .pushPoints([(h1_x, h1_y), (h2_x, h2_y)])
    .hole(hole_diameter)
)

# 4. Add Fillets
# The image shows rounded edges, especially on the top outer edge and the tab
try:
    part = part.edges("|Z").fillet(fillet_radius)
    part = part.edges(">Z").fillet(fillet_radius)
    # Bottom edges might be sharp or chamfered, leaving them sharp based on typical printing/molding
except Exception as e:
    # Fallback if fillet fails on complex geometry intersections
    print(f"Fillet warning: {e}")

result = part