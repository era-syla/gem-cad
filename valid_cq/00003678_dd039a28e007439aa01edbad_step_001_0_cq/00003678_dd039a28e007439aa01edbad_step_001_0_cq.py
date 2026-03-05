import cadquery as cq

# Parameters for the profile
# All dimensions in mm, estimated from visual proportions
base_diameter = 12.0
base_length = 5.0

# The bulbous grip section
grip_neck_diameter = 16.0
grip_max_diameter = 18.0
grip_waist_diameter = 14.0
grip_length = 25.0

# The long tapering section
taper_start_diameter = 17.0
taper_end_diameter = 4.0
taper_length = 60.0

# The tip
tip_length = 3.0

def create_profile(base_dia, grip_dia_max, grip_dia_waist, taper_start_dia, taper_end_dia, total_len):
    """
    Creates the 2D profile of the object to be revolved.
    The profile is drawn on the XZ plane, with the axis of revolution along X.
    """
    
    # Calculate radii for easier drawing
    r_base = base_dia / 2.0
    r_grip_max = grip_dia_max / 2.0
    r_grip_waist = grip_dia_waist / 2.0
    r_taper_start = taper_start_dia / 2.0
    r_taper_end = taper_end_dia / 2.0
    
    # Define key X-coordinates
    x0 = 0
    x1 = 4.0  # End of initial cylinder/chamfer
    x2 = 12.0 # First bulge peak
    x3 = 20.0 # Waist
    x4 = 28.0 # Second bulge / start of taper
    x5 = x4 + 50.0 # End of taper shaft
    x6 = x5 + 3.0  # Tip
    
    # Create the sketch
    # We are drawing the upper half of the profile to revolve around X-axis
    result = (
        cq.Workplane("XY")
        .moveTo(x0, 0)
        .lineTo(x0, r_base)
        
        # Initial slight flare/bulge
        .spline([(x1, r_grip_max * 0.9), (x2, r_grip_max)], includeCurrent=True)
        
        # The waist dip
        .spline([(x3, r_grip_waist), (x4, r_taper_start)], includeCurrent=True)
        
        # The long tapering shaft - using a spline for a slight curve instead of linear line
        # This gives it that "organic" flow seen in the image
        .spline([(x4 + 20, r_taper_start * 0.6), (x5, r_taper_end)], includeCurrent=True)
        
        # The conical tip
        .lineTo(x6, 0)
        
        # Close the shape along the axis
        .close()
    )
    
    return result

# Generate the solid by revolving the profile
# We use the X-axis (1, 0, 0) for revolution
profile = create_profile(
    base_diameter, 
    grip_max_diameter, 
    grip_waist_diameter, 
    taper_start_diameter, 
    taper_end_diameter, 
    100
)

result = profile.revolve(360, (0, 0, 0), (1, 0, 0))