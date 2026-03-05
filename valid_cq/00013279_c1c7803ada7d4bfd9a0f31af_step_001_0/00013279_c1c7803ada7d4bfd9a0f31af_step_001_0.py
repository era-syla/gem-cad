import cadquery as cq

# -- Parametric Dimensions --
length = 90.0           # Total length of the enclosure
width = 45.0            # Total width
height = 35.0           # Total height
nose_height = 15.0      # Vertical height of the front nose face
slant_run = 30.0        # Horizontal distance covered by the slanted face
back_fillet_r = 12.0    # Radius for rounding the back corners
foot_diam = 6.0         # Diameter of the feet
foot_height = 5.0       # Height of the feet
foot_inset = 8.0        # Distance from the edge to the foot center

# -- Model Generation --

# 1. Create the main body shape using a side profile sketch and extrusion
# The profile is drawn on the XZ plane.
# (0,0) corresponds to the bottom-front corner.
profile_points = [
    (0, 0),                     # Bottom Front
    (length, 0),                # Bottom Back
    (length, height),           # Top Back
    (slant_run, height),        # Transition point between top and slant
    (0, nose_height)            # Top of the vertical nose
]

# Create the base solid by extruding the profile along the Y axis
# both=True centers the extrusion on the plane, making symmetry operations easier
main_body = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .extrude(width / 2.0, both=True)
)

# 2. Round the back corners
# Select vertical edges (|Z) that are at the maximum X position (>X)
main_body = main_body.edges("|Z and >X").fillet(back_fillet_r)

# 3. Add the feet
# Select the bottom face (<Z), create a workplane, and draw the feet
# We use a construction rectangle to easily place points at the 4 corners with an offset
foot_spacing_x = length - 2 * foot_inset
foot_spacing_y = width - 2 * foot_inset

result = (
    main_body.faces("<Z")
    .workplane()
    .rect(foot_spacing_x, foot_spacing_y, forConstruction=True)
    .vertices()
    .circle(foot_diam / 2.0)
    .extrude(foot_height)
)