import cadquery as cq
import math

# Main cylinder
base_radius = 40
base_height = 30

result = cq.Workplane("XY").cylinder(base_height, base_radius)

# Add rounded rectangular tabs on top surface
# 8 tabs arranged radially, each rotated at 45 degree increments
tab_length = 22
tab_width = 8
tab_height = 6
tab_corner_radius = 3.5
tab_offset = 18  # distance from center to tab center

num_tabs = 8

for i in range(num_tabs):
    angle_deg = i * (360.0 / num_tabs)
    angle_rad = math.radians(angle_deg)
    
    # Position of tab center
    x = tab_offset * math.cos(angle_rad)
    y = tab_offset * math.sin(angle_rad)
    
    # Create a rounded rectangle (slot shape) for the tab
    # The tab is oriented radially (along the angle direction)
    tab = (
        cq.Workplane("XY")
        .transformed(offset=(x, y, base_height), rotate=(0, 0, angle_deg))
        .slot2D(tab_length, tab_width)
        .extrude(tab_height)
    )
    
    result = result.union(tab)