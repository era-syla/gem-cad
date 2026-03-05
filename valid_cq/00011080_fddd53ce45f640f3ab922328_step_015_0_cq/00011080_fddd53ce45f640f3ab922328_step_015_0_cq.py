import cadquery as cq

# --- Parameters ---

# Rail Dimensions
rail_length = 300.0
rail_width = 20.0     # Total width at the base
rail_height = 15.0    # Approximate height from base to top of rod
rod_diameter = 6.0    # Diameter of the integrated circular rails
base_thickness = 4.0  # Thickness of the flat base plate connecting rails
hole_spacing = 60.0   # Spacing between mounting holes along the rail length
hole_diameter = 3.5   # Diameter of rail mounting holes

# Carriage Block Dimensions
block_length = 45.0
block_width = 40.0
block_height = 10.0   # Thickness of the main block body
block_offset_z = rail_height - (rod_diameter/2) # Height where the block sits relative to rail base
bearing_radius = rod_diameter / 2 + 0.5 # Clearance/fit for the rail

# Mounting Holes on Block
block_hole_pattern_x = 30.0
block_hole_pattern_y = 30.0
block_hole_diam = 3.2 # M3 clearance

# --- Modeling the Rail ---

# 1. Create the Rail Profile
# The profile is a base rectangle with two circles on top corners, joined.
# We'll sketch it on the YZ plane to extrude along X.

def create_rail_profile(w, h, rod_d, base_t):
    # Calculate key points
    half_w = w / 2.0
    rod_r = rod_d / 2.0
    
    # Center of the rods
    rod_center_y = h - rod_r
    rod_center_x = half_w - rod_r
    
    # Sketch
    s = (
        cq.Sketch()
        .rect(w, base_t) # The base plate
        .push([( -rod_center_x, rod_center_y - base_t/2), ( rod_center_x, rod_center_y - base_t/2)])
        .circle(rod_r) # The rods
        .reset()
        .hull() # Combine the base and rods into a single profile
    )
    return s

# Generate the main rail solid
rail_profile = create_rail_profile(rail_width, rail_height, rod_diameter, base_thickness)
rail = (
    cq.Workplane("YZ")
    .placeSketch(rail_profile)
    .extrude(rail_length)
    .translate((rail_length/2, 0, base_thickness/2)) # Center along X, sit on Z=0
)

# 2. Add mounting holes to the rail
# We need a series of holes along the center line
num_holes = int(rail_length / hole_spacing)
hole_locations = [(x * hole_spacing - (num_holes-1)*hole_spacing/2, 0) for x in range(num_holes)]

rail = (
    rail.faces(">Z").workplane()
    .pushPoints(hole_locations)
    .cboreHole(hole_diameter, hole_diameter * 1.8, hole_diameter) # Counterbore for screw head
)


# --- Modeling the Carriage Block ---

# 1. Main Block Body
block = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .translate((0, 0, block_offset_z + block_height/2))
)

# 2. Cut out the rail path (the "bearings") underneath
# We essentially subtract the rail shape (plus some clearance) from the block.
# Since the rail profile is complex, we can approximate the cut with slots/cylinders.
rail_center_spacing = rail_width - rod_diameter

block = (
    block.faces("<Z").workplane()
    # Left groove
    .moveTo(0, -rail_center_spacing/2)
    .slot2D(block_length, rod_diameter + 1.0, 90) # slightly larger than rod
    .cutThruAll()
    # Right groove
    .moveTo(0, rail_center_spacing/2)
    .slot2D(block_length, rod_diameter + 1.0, 90)
    .cutThruAll()
)

# 3. Add mounting holes to the block
block = (
    block.faces(">Z").workplane()
    .rect(block_hole_pattern_x, block_hole_pattern_y, forConstruction=True)
    .vertices()
    .hole(block_hole_diam)
)

# 4. Add the center groove detail on top of the block (visual detail from image)
block = (
    block.faces(">Z").workplane()
    .moveTo(0, 0)
    .rect(block_length, 2.0)
    .cutBlind(-0.5)
)
block = (
    block.faces(">Z").workplane()
    .moveTo(0, 0)
    .rect(block_length, 20.0)
    .cutBlind(-0.2)
)


# --- Assembly ---

# Position the block somewhere along the rail (e.g., closer to one end as in image)
block_position_x = rail_length * 0.2
block = block.translate((block_position_x - rail_length/2, 0, 0))

# Combine
result = rail.union(block)