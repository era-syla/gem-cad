import cadquery as cq

# -- Parametric Dimensions --
rod_diameter = 14.0
rod_length = 70.0
chamfer_size = 1.5

# Small locating pin dimensions
pin_diameter = 4.0
pin_length = 5.0
pin_offset_from_end = 8.0  # Distance from rod end to pin center

# Assembly spacing
spacing_y = 40.0

def create_pin_rod():
    """Creates a cylindrical rod with chamfered ends and a small radial pin."""
    
    # 1. Create the main rod body aligned with the X-axis
    # Starting on YZ plane and extruding along X
    rod = cq.Workplane("YZ").circle(rod_diameter / 2.0).extrude(rod_length)
    
    # 2. Apply chamfers to both ends
    # Select all circular edges (which are the ends of the cylinder)
    rod = rod.edges("%CIRCLE").chamfer(chamfer_size)
    
    # 3. Create the small perpendicular pin
    # Positioned near the end of the rod, pointing downwards (-Z)
    pin_x = rod_length - pin_offset_from_end
    pin_z_start = -rod_diameter / 2.0
    
    pin = (
        cq.Workplane("XY")
        .workplane(offset=pin_z_start)
        .center(pin_x, 0)
        .circle(pin_diameter / 2.0)
        .extrude(-pin_length)  # Extrude downwards (negative Z relative to plane)
    )
    
    # 4. Unite the pin with the main rod
    final_shape = rod.union(pin)
    return final_shape

# Create the first rod (foreground)
rod1 = create_pin_rod()

# Create the second rod (background), translated in Y
rod2 = create_pin_rod().translate((0, spacing_y, 0))

# Combine into a single compound object
result = rod1.union(rod2)