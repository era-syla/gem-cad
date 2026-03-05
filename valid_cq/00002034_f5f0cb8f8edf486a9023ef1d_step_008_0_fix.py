import cadquery as cq

# Main cylindrical bushing/sleeve with flanges and grooves
# Overall dimensions estimated from image

main_radius = 20
main_height = 40
hole_radius = 8
flange_radius = 25
flange_height = 3
groove_depth = 2
groove_width = 3

# Build the main body as a series of revolved profiles
# Using revolve to create the complex profile

# Profile points for revolution (cross-section, on the right side of axis)
# Bottom to top, defining the outer profile

result = (
    cq.Workplane("XY")
    # Start with main cylinder
    .cylinder(main_height, main_radius)
)

# Add bottom flange
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cylinder(flange_height, flange_radius)
    .union(
        cq.Workplane("XY")
        .workplane(offset=0)
        .cylinder(flange_height, flange_radius)
        .translate((0, 0, -flange_height))
    )
)

# Rebuild using a cleaner approach with explicit union of parts

# Main cylinder body
body = cq.Workplane("XY").cylinder(main_height, main_radius)

# Top flange
top_flange = (cq.Workplane("XY")
    .workplane(offset=main_height/2)
    .cylinder(flange_height, flange_radius)
    .translate((0, 0, main_height/2 + flange_height/2))
)

# Bottom flange  
bot_flange = (cq.Workplane("XY")
    .cylinder(flange_height, flange_radius)
    .translate((0, 0, -main_height/2 - flange_height/2))
)

# Combine body with flanges
combined = body.union(top_flange).union(bot_flange)

# Add grooves at top and bottom of main cylinder (where flanges meet body)
# Top groove ring
top_groove = (cq.Workplane("XY")
    .workplane(offset=main_height/2 - groove_width)
    .cylinder(groove_width * 2, main_radius - groove_depth + 0.1)
    .translate((0, 0, main_height/2))
)

bot_groove = (cq.Workplane("XY")
    .cylinder(groove_width * 2, main_radius - groove_depth + 0.1)
    .translate((0, 0, -main_height/2))
)

# Use revolve approach for cleaner result
# Create profile in XZ plane and revolve

pts_outer = [
    (hole_radius, -main_height/2 - flange_height),  # inner bottom
    (flange_radius, -main_height/2 - flange_height),  # outer bottom flange
    (flange_radius, -main_height/2),                  # outer bottom flange top
    (main_radius, -main_height/2 + groove_width),     # bottom groove top
    (main_radius, main_height/2 - groove_width),      # top groove bottom
    (flange_radius, main_height/2),                   # outer top flange bottom
    (flange_radius, main_height/2 + flange_height),   # outer top
    (hole_radius, main_height/2 + flange_height),     # inner top
]

# Build via revolve
profile = (
    cq.Workplane("XZ")
    .polyline([
        (hole_radius, -main_height/2 - flange_height),
        (flange_radius, -main_height/2 - flange_height),
        (flange_radius, -main_height/2 + groove_width),
        (main_radius, -main_height/2 + groove_width*2),
        (main_radius, main_height/2 - groove_width*2),
        (flange_radius, main_height/2 - groove_width),
        (flange_radius, main_height/2 + flange_height),
        (hole_radius, main_height/2 + flange_height),
    ])
    .close()
)

result = profile.revolve(360, (0, 0, 0), (0, 1, 0))