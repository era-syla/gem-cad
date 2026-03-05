import cadquery as cq
import math

def create_plunger_model():
    # --- Parametric Dimensions ---
    
    # 1. Rear Button/Post Section
    button_dia = 10.0
    button_len = 10.0
    
    # 2. Narrow Neck/Groove Section
    neck_dia = 8.0
    neck_len = 3.0
    
    # 3. Main Body Section
    body_dia = 20.0
    body_len = 15.0
    
    # 4. Front Flange Section
    flange_dia = 26.0
    flange_len = 5.0
    
    # 5. Front Pin/Needle Section
    pin_dia = 4.0
    pin_len = 10.0
    pin_tip_len = 3.0  # Length of the conical tip
    
    # 6. Cosmetic Spring (approximate representation)
    spring_wire_dia = 0.3
    spring_coil_dia = 5.0
    spring_pitch = 2.0
    spring_turns = 5
    
    # --- Geometry Creation ---
    
    # Start building from the rear (left side of image) to the front
    
    # 1. Rear Button
    part = cq.Workplane("XY").circle(button_dia/2).extrude(button_len)
    
    # 2. Neck/Groove
    part = part.faces(">Z").workplane().circle(neck_dia/2).extrude(neck_len)
    
    # 3. Main Body
    part = part.faces(">Z").workplane().circle(body_dia/2).extrude(body_len)
    
    # 4. Front Flange
    part = part.faces(">Z").workplane().circle(flange_dia/2).extrude(flange_len)
    
    # 5. Front Pin Shaft
    part = part.faces(">Z").workplane().circle(pin_dia/2).extrude(pin_len)
    
    # 6. Front Pin Conical Tip
    # Create a cone by extruding with a taper or lofting. 
    # Here, a revolve is simple and robust for a cone.
    # We locate the workplane at the end of the pin.
    current_z = button_len + neck_len + body_len + flange_len + pin_len
    
    # Method: Draw triangle profile and revolve
    tip = (
        cq.Workplane("XZ")
        .workplane(offset=current_z) # Move to the end of the pin
        .moveTo(0, 0)
        .lineTo(pin_dia/2, 0)
        .lineTo(0, pin_tip_len)
        .close()
        .revolve()
    )
    
    result = part.union(tip)

    # 7. Add Cosmetic Threads/Ridges to the Pin
    # The image shows ridges on the pin. Let's add small cuts.
    # We'll make ring cuts along the pin length.
    ridge_count = 8
    ridge_spacing = 0.8
    ridge_depth = 0.2
    ridge_width = 0.4
    
    start_ridges_z = button_len + neck_len + body_len + flange_len + 1.0
    
    for i in range(ridge_count):
        z_pos = start_ridges_z + (i * ridge_spacing)
        
        # Create a cutting tool for the groove
        cutter = (
            cq.Workplane("XY")
            .workplane(offset=z_pos)
            .circle(pin_dia/2 + 0.1) # Outer boundary for cut
            .circle(pin_dia/2 - ridge_depth) # Inner boundary for cut
            .extrude(ridge_width)
        )
        result = result.cut(cutter)

    # 8. Create the helical spring
    # CadQuery helix creation
    
    def helix_path(pitch, turns, radius):
        # Parametric function for a helix
        def f(t):
            # t goes from 0 to 1
            angle = t * turns * 2 * math.pi
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = t * turns * pitch
            return (x, y, z)
        return f

    spring_start_z = current_z + pin_tip_len/2 # Start slightly overlapping the tip
    
    # Generate points for the helix
    points = []
    num_points = 100
    for i in range(num_points + 1):
        t = i / num_points
        angle = t * spring_turns * 2 * math.pi
        r = spring_coil_dia / 2
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = spring_start_z + (t * spring_turns * spring_pitch)
        points.append((x, y, z))
        
    # Create the spring wire by sweeping a circle along the spline path
    if len(points) > 1:
        path = cq.Workplane("XY").spline(points)
        spring = (
            cq.Workplane("XZ")
            .workplane(offset=0) # Reset workplane
            # Position wire profile at the start of the path
            .center(points[0][0], points[0][2]) 
            .workplane(centerOption="CenterOfMass")
            # We need to orient the circle normal to the path direction roughly
            # For simplicity in this script, we draw on XZ and it sweeps.
            # A precise normal plane requires more complex Frenet frame logic usually not needed for visual representation.
            .circle(spring_wire_dia/2)
            .sweep(path, isFrenet=True)
        )
        result = result.union(spring)

    return result

# Generate the model
result = create_plunger_model()