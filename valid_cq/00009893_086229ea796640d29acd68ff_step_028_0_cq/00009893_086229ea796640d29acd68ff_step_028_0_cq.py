import cadquery as cq

# Parameters for the pulley/grommet shape
# Adjust these dimensions to resize the model
total_height = 20.0
outer_flange_diameter = 60.0
inner_hub_diameter = 40.0
bore_diameter = 25.0
flange_thickness = 2.0

# Calculate derived dimensions
hub_radius = inner_hub_diameter / 2.0
flange_radius = outer_flange_diameter / 2.0
bore_radius = bore_diameter / 2.0
half_height = total_height / 2.0

# Create the profile to be revolved
# We will draw the cross-section on the XZ plane and revolve around Z
# The profile looks like a 'U' shape on its side if looking at just the solid wall
# Or simply a rectangle for the hub with two rectangles for the flanges.
# Let's create the full solid cylinder first, then add flanges, then cut the bore.

# Method: Construct the cross-section profile and revolve it.
# Points for the right-hand side of the cross section (assuming center is at X=0)
#  (Bore Radius, -Half Height) -> Start
#  (Flange Radius, -Half Height) -> Bottom Flange Outer Edge
#  (Flange Radius, -Half Height + Flange Thickness) -> Bottom Flange Top Edge
#  (Hub Radius, -Half Height + Flange Thickness) -> Hub Bottom Start
#  (Hub Radius, Half Height - Flange Thickness) -> Hub Top End
#  (Flange Radius, Half Height - Flange Thickness) -> Top Flange Bottom Edge
#  (Flange Radius, Half Height) -> Top Flange Outer Edge
#  (Bore Radius, Half Height) -> Top Inner Edge
#  (Bore Radius, -Half Height) -> Close Loop

result = (
    cq.Workplane("XY")
    .circle(outer_flange_diameter / 2.0)
    .extrude(flange_thickness) # Bottom flange
    .faces(">Z").workplane()
    .circle(inner_hub_diameter / 2.0)
    .extrude(total_height - (2 * flange_thickness)) # Central hub
    .faces(">Z").workplane()
    .circle(outer_flange_diameter / 2.0)
    .extrude(flange_thickness) # Top flange
    .faces(">Z").workplane()
    .hole(bore_diameter) # Cut the central hole through everything
)

# Optional: Add fillets to the internal corners where flanges meet the hub for realism
# Select edges based on geometric properties
result = result.edges(
    cq.selectors.RadiusNthSelector(1) # Select the edges corresponding to the hub radius
).fillet(1.0) 

# Ensure the result is exported/visible
if 'show_object' in globals():
    show_object(result)