import cadquery as cq

# Parametric dimensions for the handle
total_height = 135.0
nub_radius = 6.0
nub_height = 10.0
base_radius = 14.5
base_height = 25.0
neck_radius = 11.5
neck_height = 55.0
bulb_radius = 19.0
bulb_height = 95.0

# Define the profile points for the organic shape
# These points define the curve after the initial nub
profile_points = [
    (base_radius, base_height),
    (neck_radius, neck_height),
    (bulb_radius, bulb_height),
    (0, total_height)  # Ends at the top center
]

# Define tangents at each point to ensure smooth transitions and a rounded top
# 5 Tangents corresponding to: [Start(Nub Top), Base, Neck, Bulb, Top]
profile_tangents = [
    (0.15, 1.0),   # Start: Slight outward flare from the nub
    (0.3, 1.0),    # Base: Continuing to curve up
    (0.0, 1.0),    # Neck: Vertical tangent at the inflection point
    (-0.25, 1.0),  # Bulb: Begin curving inwards
    (-1.0, 0.0)    # Top: Horizontal tangent to form a smooth dome
]

# Create the model by revolving the profile around the Z-axis
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(nub_radius, 0)          # Bottom of nub
    .lineTo(nub_radius, nub_height) # Side of nub
    .spline(
        profile_points,
        includeCurrent=True,
        tangents=profile_tangents
    )
    .close() # Close the profile back to (0,0)
    .revolve()
)