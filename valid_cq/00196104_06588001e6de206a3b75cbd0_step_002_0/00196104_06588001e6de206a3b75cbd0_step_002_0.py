import cadquery as cq

# Parametric dimensions
num_units = 10          # Total number of units in the array
num_l_shaped = 5        # Number of L-shaped units (starting from the left)
pitch = 8.0             # Center-to-center spacing between units
width = 5.0             # Width of each unit along the array axis
depth = 9.0             # Depth of the unit (length front-to-back)
thickness = 2.5         # Thickness of the block
leg_drop = 4.5          # Additional downward length for the L-shape leg

# List to accumulate the generated solids
solids = []

for i in range(num_units):
    # Calculate the position along the array axis (X-axis)
    x_pos = i * pitch
    
    # Create a workplane on the YZ plane (side view), offset to the correct X position.
    # We will sketch the cross-section profile on this plane and extrude along X.
    wp = cq.Workplane("YZ").workplane(offset=x_pos)
    
    if i < num_l_shaped:
        # Define the L-shape profile coordinates (Y, Z)
        # Origin (0,0) is placed at the top-front corner
        profile_points = [
            (0, 0),                                  # Top-Front Corner
            (depth, 0),                              # Top-Back Corner
            (depth, -thickness),                     # Bottom-Back Corner
            (thickness, -thickness),                 # Inner Corner
            (thickness, -(thickness + leg_drop)),    # Leg Inner Bottom
            (0, -(thickness + leg_drop)),            # Leg Outer Bottom
            (0, 0)                                   # Closing the loop
        ]
    else:
        # Define the Flat shape profile coordinates (Y, Z)
        profile_points = [
            (0, 0),                                  # Top-Front Corner
            (depth, 0),                              # Top-Back Corner
            (depth, -thickness),                     # Bottom-Back Corner
            (0, -thickness),                         # Bottom-Front Corner
            (0, 0)                                   # Closing the loop
        ]
        
    # Create the solid by sketching the profile and extruding symmetrically
    # 'both=True' extrudes in both directions, so we use half the width
    item = wp.polyline(profile_points).close().extrude(width / 2.0, both=True)
    solids.append(item)

# Combine all individual solids into a single CadQuery object
result = solids[0]
for s in solids[1:]:
    result = result.union(s)