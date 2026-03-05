import cadquery as cq

# Parametric dimensions
# Inner diameter of the ring (hole)
inner_diameter = 40.0
# Outer diameter of the main cylindrical body
body_outer_diameter = 44.0
# Outer diameter of the flange at the bottom
flange_outer_diameter = 48.0
# Height of the main body section
body_height = 12.0
# Height/thickness of the flange section
flange_height = 3.0

# Create the main body cylinder
# We start with a solid cylinder representing the upper part
main_body = cq.Workplane("XY").circle(body_outer_diameter / 2).extrude(body_height + flange_height)

# Create the flange
# We create a cylinder for the flange at the bottom
flange = cq.Workplane("XY").circle(flange_outer_diameter / 2).extrude(flange_height)

# Combine the flange and the main body
# Since the main body was extruded to the full height, we need to handle the overlap correctly.
# A simpler approach is to stack them or unite them. 
# Let's recreate it as a union of two cylinders for clarity.

# Re-approach: Construct by revolving a profile or stacking cylinders.
# Stacking cylinders is very straightforward in CadQuery.

result = (
    cq.Workplane("XY")
    # Create the bottom flange solid
    .circle(flange_outer_diameter / 2).extrude(flange_height)
    # Select the top face of the flange
    .faces(">Z").workplane()
    # Create the upper body solid
    .circle(body_outer_diameter / 2).extrude(body_height)
    # Now cut the hole through the entire assembly
    .faces(">Z").workplane()
    .circle(inner_diameter / 2).cutThruAll()
)

# Export the result for verification (optional, usually handled by the environment)
# cq.exporters.export(result, "flanged_bushing.step")