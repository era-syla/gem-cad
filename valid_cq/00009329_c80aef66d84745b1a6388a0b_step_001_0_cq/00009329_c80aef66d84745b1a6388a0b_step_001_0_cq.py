import cadquery as cq

# Parametric dimensions
main_diameter = 20.0
main_length = 100.0

# End section dimensions
taper_length = 5.0
end_shaft_diameter = 8.0
end_shaft_length = 10.0
groove_width = 2.0
groove_depth = 1.0  # Reduction in radius
groove_offset = 3.0 # Distance from the very end to the start of the groove

# Derived calculations
total_length = main_length + 2 * (taper_length + end_shaft_length)

def create_roller():
    # 1. Create the main central cylinder
    roller = cq.Workplane("XY").circle(main_diameter / 2).extrude(main_length)

    # Function to create one end of the shaft
    def add_shaft_end(part, direction):
        # Determine the workplane based on direction (positive or negative Z)
        if direction > 0:
            face_selector = ">Z"
            extrusion_dir = 1
        else:
            face_selector = "<Z"
            extrusion_dir = -1
        
        # 2. Add the tapered section (frustum)
        # We start from the end face of the current part
        # loft is a good way to make a taper, but simple extrusion with a separate sketch is easier to control
        # or just simple cylinder stacking.
        # Let's use a loft for the taper to be robust.
        
        # Get the center of the face
        end_face = part.faces(face_selector)
        
        # Create the taper
        # We need to create a new sketch plane offset by taper_length
        # But CadQuery's stack-based approach is easier.
        
        # Let's try a different approach: Revolve a profile.
        # A profile is much easier for this axially symmetric part.
        return part

    # RE-STRATEGY: Using a Revolve operation is cleaner for this type of turned part.
    # We will draw the half-profile on the XZ plane and revolve it around the Z axis.
    
    # Calculate half dimensions
    r_main = main_diameter / 2.0
    r_shaft = end_shaft_diameter / 2.0
    r_groove = r_shaft - groove_depth
    
    # Z-coordinates relative to center
    z_center_half = main_length / 2.0
    z_taper_end = z_center_half + taper_length
    z_shaft_end = z_taper_end + end_shaft_length
    
    # Groove coordinates
    # Groove is near the end. Let's place it 'groove_offset' from the tip.
    z_groove_start = z_shaft_end - groove_offset - groove_width
    z_groove_end = z_shaft_end - groove_offset

    # Define points for the profile (positive X, variable Z)
    # We'll draw the right half and mirror it, or draw the whole profile if simpler.
    # Let's draw the full profile from bottom to top on the right side of the axis (X > 0)
    
    pts = []
    
    # Bottom End (Negative Z)
    pts.append((0, -z_shaft_end)) # Start on axis
    pts.append((r_shaft, -z_shaft_end))
    pts.append((r_shaft, -(z_shaft_end - groove_offset)))
    pts.append((r_groove, -(z_shaft_end - groove_offset))) # Groove start
    pts.append((r_groove, -(z_shaft_end - groove_offset - groove_width))) # Groove end
    pts.append((r_shaft, -(z_shaft_end - groove_offset - groove_width)))
    pts.append((r_shaft, -z_taper_end))
    pts.append((r_main, -z_center_half))
    
    # Main Body
    pts.append((r_main, z_center_half))
    
    # Top End (Positive Z)
    pts.append((r_shaft, z_taper_end))
    pts.append((r_shaft, z_groove_start))
    pts.append((r_groove, z_groove_start)) # Groove start
    pts.append((r_groove, z_groove_end)) # Groove end
    pts.append((r_shaft, z_groove_end))
    pts.append((r_shaft, z_shaft_end))
    pts.append((0, z_shaft_end)) # End on axis
    
    # Close the profile
    pts.append((0, -z_shaft_end))

    # Create the revolve
    result_obj = cq.Workplane("XZ").polyline(pts).close().revolve()
    
    return result_obj

# Generate the model
result = create_roller()