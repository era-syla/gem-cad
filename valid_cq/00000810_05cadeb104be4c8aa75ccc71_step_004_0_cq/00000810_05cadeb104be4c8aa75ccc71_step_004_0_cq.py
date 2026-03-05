import cadquery as cq
import math

def involute_gear(module, teeth, width, pressure_angle=20, helix_angle=0, clearance=0.0):
    """
    Helper function to generate a simplified helical gear profile.
    This creates a solid gear that can be unioned with the shaft.
    """
    # Basic gear parameters
    pitch_radius = module * teeth / 2.0
    base_radius = pitch_radius * math.cos(math.radians(pressure_angle))
    addendum = module
    dedendum = 1.25 * module
    outside_radius = pitch_radius + addendum
    root_radius = pitch_radius - dedendum

    # Create the base 2D profile for a single tooth space
    # (Simplified approach for visual representation)
    
    # Create the main cylinder
    gear_solid = cq.Workplane("XY").circle(outside_radius).extrude(width)
    
    # Calculate helix twist
    # twist = 360 * width * tan(helix_angle) / (PI * diameter)
    twist_angle = 0
    if helix_angle != 0:
        twist_angle = (360.0 * width * math.tan(math.radians(helix_angle))) / (2 * math.pi * pitch_radius)

    # We will use cadquery.Workplane.gear if available, but to stick to standard CQ 
    # without external plugins, we construct a helical gear manually or simply
    # represent it. Since exact involute generation is complex in raw script without
    # plugins, we'll use a built-in twisting extrusion of a gear-like profile.

    # Approximating the gear profile
    # Create points for a star/gear shape
    pts = []
    num_teeth = teeth
    for i in range(num_teeth * 2):
        angle = (math.pi * 2 * i) / (num_teeth * 2)
        r = root_radius if i % 2 == 0 else outside_radius
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        pts.append((x, y))
    
    # Create the profile and extrude with twist
    gear = (cq.Workplane("XY")
            .polyline(pts).close()
            .twistExtrude(width, twist_angle)
           )
    
    return gear

# --- Parametric Definitions ---

# Shaft main dimensions
total_length = 150.0
shaft_diameter_main = 20.0
shaft_diameter_front = 18.0 # Keyway section
shaft_diameter_rear = 16.0 # Behind gear

# Front section (Keyway)
front_length = 50.0
keyway_width = 5.0
keyway_length = 30.0
keyway_depth = 2.5
keyway_offset_from_end = 10.0
center_hole_dia = 6.0

# Gear section
gear_location_z = 70.0 # From front
gear_width = 35.0
gear_module = 2.0
gear_teeth = 15
helix_angle = 30.0 # Degrees

# Rear section
rear_flange_dia = 35.0
rear_flange_thickness = 3.0
rear_section_length = 30.0 # After gear

# --- Modeling ---

# 1. Main Shaft Construction
# Using a stack of cylinders for the main body to handle diameter changes easily
shaft = (cq.Workplane("XY")
         # Front section (Keyway area)
         .circle(shaft_diameter_front/2.0).extrude(front_length)
         # Middle section (Bearing seat before gear)
         .faces(">Z").workplane()
         .circle(shaft_diameter_main/2.0).extrude(gear_location_z - front_length)
         # Gear mounting section (internal to gear)
         .faces(">Z").workplane()
         .circle(shaft_diameter_main/2.0).extrude(gear_width)
         # Rear section
         .faces(">Z").workplane()
         .circle(shaft_diameter_rear/2.0).extrude(rear_section_length)
         # Rear Flange
         .faces(">Z").workplane()
         .circle(rear_flange_dia/2.0).extrude(rear_flange_thickness)
         # Fillet at flange
         .faces("<Z").edges().fillet(2.0)
         )

# 2. Keyway
# Create a slot cut on the front section
# We orient on XZ plane to cut into the side of the cylinder
keyway_center_z = keyway_offset_from_end + keyway_length/2.0

shaft = (shaft.faces("<Z").workplane()
         .transformed(offset=(0, 0, keyway_center_z), rotate=(0, 90, 0))
         .slot2D(keyway_length, keyway_width)
         .cutBlind(keyway_depth + shaft_diameter_front/2.0) # Cut deep enough from surface
         )

# 3. Flat on the front shaft
# The image shows a flat milled on the end of the shaft, perpendicular to keyway or aligned.
# Looking closely, there's a flat surface on the cylindrical face near the front.
flat_cut_depth = 1.0
flat_length = front_length
shaft = (shaft.faces("<Z").workplane()
        .transformed(offset=(shaft_diameter_front/2.0 - flat_cut_depth, 0, front_length/2.0))
        .box(flat_cut_depth*2, shaft_diameter_front, front_length, centered=(True, True, True))
        .cut(shaft) # Intersect to just remove the slice? No, we want to cut the shaft with the box.
        )
# Let's redo the flat more reliably:
shaft = (shaft.faces("<Z").workplane()
         .transformed(offset=(0, 0, front_length/2.0))
         .box(shaft_diameter_front, shaft_diameter_front*2, front_length, centered=(True, True, True))
         .translate((shaft_diameter_front - flat_cut_depth, 0, 0))
         .cut(shaft) # This logic is inverted, we subtract box from shaft
         )
# Actually, the simplest way is to cut the existing result
shaft = shaft.cut(
    cq.Workplane("XY").workplane(offset=front_length/2).
    box(50, 50, front_length, centered=(True,True,True))
    .translate((25 + shaft_diameter_front/2.0 - 1.5, 0, 0)) # 1.5mm flat depth
)

# 4. Center Hole
shaft = (shaft.faces("<Z").workplane()
         .circle(center_hole_dia/2.0)
         .cutBlind(-15.0) # Depth of center hole
         )
         
# 5. Helical Gear
# Generate the gear geometry
gear_geo = involute_gear(gear_module, gear_teeth, gear_width, helix_angle=helix_angle)

# Position the gear
# The gear is generated on XY plane, extruded +Z.
# We need to move it to the correct Z height on the shaft.
gear_geo = gear_geo.translate((0, 0, gear_location_z))

# 6. Combine
result = shaft.union(gear_geo)

# 7. Chamfers and Fillets
# Add a chamfer to the front face
result = result.edges(cq.selectors.NearestToPointSelector((0,0,0))).chamfer(1.0)

# Fillet transition from front shaft to main shaft
result = result.edges(cq.selectors.NearestToPointSelector((0, shaft_diameter_main/2.0, front_length))).fillet(1.0)

# Optional: Fillet behind the gear
result = result.edges(cq.selectors.NearestToPointSelector((0, shaft_diameter_rear/2.0, gear_location_z + gear_width))).fillet(1.0)
