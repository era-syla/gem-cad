import cadquery as cq

# Parameters for the pin/rivet geometry
d_head = 28.0      # Diameter of the flat top of the head
d_shaft = 12.0     # Diameter of the main cylindrical shaft
d_tip = 6.0        # Diameter of the flat end of the tip
l_head = 12.0      # Length of the conical head section
l_shaft = 30.0     # Length of the straight cylindrical shaft
l_tip = 6.0        # Length of the chamfered tip section

# Define the 2D profile points for revolution
# The profile is drawn in the XY plane, to be revolved around the X axis
profile_points = [
    (0, 0),                                      # Center of the top head face
    (0, d_head / 2.0),                           # Outer edge of the top head face
    (l_head, d_shaft / 2.0),                     # Base of the head / start of the shaft
    (l_head + l_shaft, d_shaft / 2.0),           # End of the shaft / start of the tip chamfer
    (l_head + l_shaft + l_tip, d_tip / 2.0),     # Outer edge of the flat tip
    (l_head + l_shaft + l_tip, 0)                # Center of the flat tip
]

# Create the 3D solid by revolving the profile 360 degrees around the X axis
result = (
    cq.Workplane("XY")
    .polyline(profile_points)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)