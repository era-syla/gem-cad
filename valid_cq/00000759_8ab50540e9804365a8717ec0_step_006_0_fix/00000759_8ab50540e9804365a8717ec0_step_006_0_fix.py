import cadquery as cq

# Main cylinder (roller/pin shape)
radius = 10
length = 60
small_radius = 4
small_length = 5

# Create the main body - large cylinder
main_body = (
    cq.Workplane("YZ")
    .circle(radius)
    .extrude(length)
)

# Add a small cylindrical stub on one end (the small cap visible in image)
small_stub = (
    cq.Workplane("YZ")
    .circle(small_radius)
    .extrude(small_length)
)

# Combine
result = main_body.union(small_stub)

# Fillet the edge where main cylinder meets the flat end (far end)
# Select edges at the far end face
try:
    result = (
        cq.Workplane("YZ")
        .circle(radius)
        .extrude(length)
    )
    
    # Add small stub on left end (negative x direction)
    stub = (
        cq.Workplane("YZ")
        .circle(small_radius)
        .extrude(small_length)
    )
    
    result = result.union(stub)
    
    # Fillet the circular edge at the far end of the main cylinder
    # Find edges at x = length position (the rim edge)
    result = result.edges("|X").fillet(1.5)
    
except Exception:
    # Fallback without fillet
    result = (
        cq.Workplane("YZ")
        .circle(radius)
        .extrude(length)
    )
    stub = (
        cq.Workplane("YZ")
        .circle(small_radius)
        .extrude(small_length)
    )
    result = result.union(stub)