import cadquery as cq
import math

# --- Geometric Parameters ---
num_teeth = 8
rim_height = 15.0
floor_thickness = 3.0
outer_radius_tip = 25.0   # Maximum radius at the tip of the tooth
outer_radius_base = 20.0  # Minimum radius at the valley of the tooth
inner_radius = 18.0       # Radius of the inner cylindrical recess
tooth_bulge = 1.5         # Parameter to control the convexity of the tooth curve

def create_turbine_wheel():
    """Generates a single turbine/ratchet wheel solid."""
    
    # 1. construct the outer profile (the ratchet shape)
    edges = []
    angle_step = 360.0 / num_teeth
    
    for i in range(num_teeth):
        # Angles for the start and end of the current tooth segment
        start_angle = i * angle_step
        end_angle = (i + 1) * angle_step
        
        # Convert polar to Cartesian coordinates
        
        # Point A: Start of the tooth (at the base radius)
        rad_start = math.radians(start_angle)
        pt_a = cq.Vector(
            outer_radius_base * math.cos(rad_start),
            outer_radius_base * math.sin(rad_start),
            0
        )
        
        # Point B: Tip of the tooth (at the tip radius)
        rad_end = math.radians(end_angle)
        pt_b = cq.Vector(
            outer_radius_tip * math.cos(rad_end),
            outer_radius_tip * math.sin(rad_end),
            0
        )
        
        # Point C: Midpoint control for the curved edge (creating the 'fin' shape)
        # We calculate a radius slightly larger than the linear average to bulge it out
        rad_mid = math.radians((start_angle + end_angle) / 2.0)
        r_mid = (outer_radius_base + outer_radius_tip) / 2.0 + tooth_bulge
        pt_mid = cq.Vector(
            r_mid * math.cos(rad_mid),
            r_mid * math.sin(rad_mid),
            0
        )
        
        # Point D: The 'drop' point. Matches Point B angle but at base radius.
        # This forms the sharp radial face of the ratchet.
        pt_d = cq.Vector(
            outer_radius_base * math.cos(rad_end),
            outer_radius_base * math.sin(rad_end),
            0
        )
        
        # Create the curved outer edge (Three Point Arc)
        arc = cq.Edge.makeThreePointArc(pt_a, pt_mid, pt_b)
        edges.append(arc)
        
        # Create the radial line connecting the tip back to the base radius
        line = cq.Edge.makeLine(pt_b, pt_d)
        edges.append(line)
        
    # Assemble the edges into a closed wire
    outer_wire = cq.Wire.assembleEdges(edges)
    
    # 2. Construct the inner profile (Circle)
    inner_wire = cq.Wire.makeCircle(inner_radius, cq.Vector(0,0,0), cq.Vector(0,0,1))
    
    # 3. Create the rim face by defining the area between outer and inner wires
    rim_face = cq.Face.makeFromWires(outer_wire, [inner_wire])
    
    # 4. Extrude the rim face to create the wall
    # We load the face into a Workplane to perform the extrusion
    rim_solid = cq.Workplane(obj=rim_face).extrude(rim_height)
    
    # 5. Create the base floor
    # Simple cylinder at the origin with the inner radius
    floor_solid = cq.Workplane("XY").circle(inner_radius).extrude(floor_thickness)
    
    # 6. Union the rim and the floor
    part = rim_solid.union(floor_solid)
    
    # 7. Add fillets
    # Fillet the top edges of the rim for a smooth appearance similar to the image
    part = part.faces(">Z").edges().fillet(0.5)
    
    return part

# --- Assembly ---

# Create the first wheel
wheel1 = create_turbine_wheel()

# Create a second wheel and translate it to match the composition in the image
# Placed adjacent to the first one
wheel2 = create_turbine_wheel().translate((0, outer_radius_tip * 2.1, 0))

# Combine both into the final result
result = wheel1.union(wheel2)