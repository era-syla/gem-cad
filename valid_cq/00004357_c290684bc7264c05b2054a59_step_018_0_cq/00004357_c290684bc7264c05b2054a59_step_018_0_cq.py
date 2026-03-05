import cadquery as cq
import math

def create_sprocket():
    # --- Parametric Dimensions ---
    # Overall dimensions
    outer_radius = 50.0       # Radius to the tip of teeth
    rim_thickness = 5.0       # Thickness of the outer rim (radial depth)
    rim_height = 8.0          # Height (Z) of the toothed section
    
    # Hub dimensions
    hub_radius = 15.0         # Outer radius of the central hub
    hub_height = 25.0         # Total height of the central hub
    bore_radius = 8.0         # Radius of the central hole
    
    # Spoke dimensions
    num_spokes = 6            # Number of spokes connecting hub and rim
    spoke_width = 6.0         # Thickness of the spokes
    spoke_height = 8.0        # Height (Z) of the spokes
    
    # Tooth parameters
    num_teeth = 24            # Number of teeth on the sprocket
    tooth_depth = 4.0         # Radial depth of the tooth cut
    tooth_base_width_ratio = 0.5 # Width of tooth base relative to pitch
    
    # --- Modeling Steps ---

    # 1. Create the Central Hub
    # Cylinder centered at origin
    hub = cq.Workplane("XY").circle(hub_radius).extrude(hub_height)
    
    # 2. Create the Central Bore
    # Cut a hole through the hub
    hub = hub.faces(">Z").workplane().hole(bore_radius * 2)

    # 3. Create the Outer Rim (Ring)
    # The rim sits around the outside. We model the base ring first.
    # The rim connects to the spokes.
    # Inner radius of the rim is where spokes end.
    rim_inner_radius = outer_radius - rim_thickness - tooth_depth
    
    rim = cq.Workplane("XY").circle(outer_radius).circle(rim_inner_radius).extrude(rim_height)
    
    # 4. Create the Teeth
    # We will cut the teeth out of the outer cylinder or add them. 
    # A robust way is to create a cutter profile.
    # Let's create a single tooth cutter and pattern it.
    
    # Calculate angular pitch
    angle_per_tooth = 360.0 / num_teeth
    
    # Create a profile for the gap between teeth
    # We work on the XY plane and then extrude and cut
    # The "gap" is roughly a U-shape or trapezoid cut into the outer radius
    
    # Radii for tooth generation
    root_radius = outer_radius - tooth_depth
    
    # Define a custom tooth profile shape (trapezoidal/involute approximation)
    # We will sketch one tooth and extrude it, then union it with a base cylinder.
    # Alternative approach: create a base cylinder of root_radius and add teeth.
    
    # Let's rebuild the rim + teeth as a single extrusion for cleanliness
    def sprocket_profile(num_teeth, outer_r, root_r):
        # A simple parametric profile generator
        pts = []
        for i in range(num_teeth):
            angle = math.radians(i * 360.0 / num_teeth)
            next_angle = math.radians((i + 1) * 360.0 / num_teeth)
            mid_angle = (angle + next_angle) / 2
            
            # Tooth tip width (angular)
            tip_span = (next_angle - angle) * 0.2
            # Tooth root width (angular)
            root_span = (next_angle - angle) * 0.5
            
            # Points for one tooth cycle:
            # 1. Root start
            r_start_angle = angle + root_span/2
            pts.append((root_r * math.cos(r_start_angle), root_r * math.sin(r_start_angle)))
            
            # 2. Tip start
            t_start_angle = mid_angle - tip_span/2
            pts.append((outer_r * math.cos(t_start_angle), outer_r * math.sin(t_start_angle)))
            
            # 3. Tip end
            t_end_angle = mid_angle + tip_span/2
            pts.append((outer_r * math.cos(t_end_angle), outer_r * math.sin(t_end_angle)))
            
            # 4. Root end (start of next valley)
            r_end_angle = next_angle - root_span/2
            pts.append((root_r * math.cos(r_end_angle), root_r * math.sin(r_end_angle)))
            
        pts.append(pts[0]) # Close the loop
        return pts

    # Generate points for the sprocket outer profile
    tooth_pts = sprocket_profile(num_teeth, outer_radius, root_radius)
    
    # Create the toothed ring
    # Inner circle for the ring
    inner_ring_wire = cq.Workplane("XY").circle(rim_inner_radius).val()
    
    # Outer toothed wire
    outer_tooth_wire = cq.Workplane("XY").polyline(tooth_pts).close().val()
    
    # Combine wires into a face and extrude
    # Note: This replaces the simple 'rim' created in step 3
    toothed_rim = cq.Workplane("XY").add(outer_tooth_wire).add(inner_ring_wire).toPending().extrude(rim_height)


    # 5. Create Spokes
    # Create a single spoke and rotate it
    spoke_length = (rim_inner_radius - hub_radius) + 1.0 # Slight overlap for boolean
    
    # Center the spoke rectangle so it connects hub and rim
    # The center of the spoke needs to be at (hub_radius + length/2)
    spoke_center_dist = hub_radius + (spoke_length / 2.0) - 0.5
    
    single_spoke = (cq.Workplane("XY")
                    .center(spoke_center_dist, 0)
                    .box(spoke_length, spoke_width, spoke_height))
    
    # Pattern the spokes
    spokes = (single_spoke.rotate((0,0,0), (0,0,1), 0) # Base object for pattern
              .union(single_spoke.rotate((0,0,0), (0,0,1), 60))
              .union(single_spoke.rotate((0,0,0), (0,0,1), 120))
              .union(single_spoke.rotate((0,0,0), (0,0,1), 180))
              .union(single_spoke.rotate((0,0,0), (0,0,1), 240))
              .union(single_spoke.rotate((0,0,0), (0,0,1), 300))
              )

    # 6. Combine all parts
    result = hub.union(toothed_rim).union(spokes)
    
    # 7. Add Fillets/Chamfers (Optional refinement based on image look)
    # The image shows a small flange or step on the rim, let's add the flange detail.
    # The rim in the image has a wider base (flange) on one side.
    
    # Create the flange on the bottom of the rim
    flange_width = 2.0
    flange_thickness = 2.0
    flange_outer_r = outer_radius # Flange seems to match tooth tip or root radius roughly
    # Actually, looking closely, the teeth sit ON a ring.
    # Let's add a simple ring at the bottom to represent the flange shown in the image.
    
    flange = (cq.Workplane("XY")
              .workplane(offset=0) # Bottom
              .circle(rim_inner_radius + rim_thickness + 1.0) # Slightly wider than root
              .circle(rim_inner_radius)
              .extrude(flange_thickness))
    
    result = result.union(flange)

    # Fillet the junction between spokes and hub/rim for strength/realism
    # result = result.edges("|Z").fillet(1.0) # Can be computationally expensive

    return result

# Generate the model
result = create_sprocket()