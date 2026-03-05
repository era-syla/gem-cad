import cadquery as cq

# Parametric dimensions
spool_outer_radius = 40.0
spool_inner_radius = 20.0  # Where the wire would wind
spool_width = 30.0         # Width between the two flanges
flange_thickness = 2.0

hub_radius_1 = 15.0        # The wider part of the hub extension
hub_width_1 = 10.0         # Length of wider hub part
hub_radius_2 = 10.0        # The narrower part of the hub extension
hub_width_2 = 8.0          # Length of narrower hub part
hub_radius_3 = 6.0         # The small boss at the end
hub_width_3 = 3.0          # Length of small boss

shaft_radius = 2.0         # The central shaft sticking out
shaft_length_total = 80.0  # Total length of the shaft

# Create the main spool body
# We'll create the profile and revolve it

# Define the spool drum (center cylinder)
drum = cq.Workplane("XY").circle(spool_inner_radius).extrude(spool_width)

# Define the flanges
flange_left = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness)
    .circle(spool_outer_radius)
    .extrude(flange_thickness)
)

flange_right = (
    cq.Workplane("XY")
    .workplane(offset=spool_width)
    .circle(spool_outer_radius)
    .extrude(flange_thickness)
)

# Create the stepped hub on the front (left side relative to extrusion direction)
# Looking at the image, there's a stepped structure protruding from one flange
# The image shows the stepped hub on the "front" face. Let's align it with negative Z.

hub_step_1 = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness)
    .circle(hub_radius_1)
    .extrude(-hub_width_1)
)

hub_step_2 = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness - hub_width_1)
    .circle(hub_radius_2)
    .extrude(-hub_width_2)
)

# Chamfer between step 1 and step 2 creates the conical transition visible in the image
# To do this cleanly, let's select the edge of hub_step_1 closest to hub_step_2
# However, simple extrusion stacking is easier. To get the cone shape, we can use a loft or chamfer.
# The image shows a conical transition. Let's rebuild the hub steps with a loft for the transition.

# Re-approach for the Hub to match the conical transition better:
# Hub cylinder 1
hub_part_1 = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness)
    .circle(hub_radius_1)
    .extrude(-hub_width_1 + 2) # Leave space for chamfer
)

# Conical transition
transition_start = -flange_thickness - hub_width_1 + 2
transition_end = -flange_thickness - hub_width_1
hub_transition = (
    cq.Workplane("XY")
    .workplane(offset=transition_start)
    .circle(hub_radius_1)
    .workplane(offset=transition_end - transition_start)
    .circle(hub_radius_2)
    .loft(combine=True)
)

# Hub cylinder 2
hub_part_2 = (
    cq.Workplane("XY")
    .workplane(offset=transition_end)
    .circle(hub_radius_2)
    .extrude(-hub_width_2)
)

# Small boss at the very end
boss_z_start = transition_end - hub_width_2
hub_part_3 = (
    cq.Workplane("XY")
    .workplane(offset=boss_z_start)
    .circle(hub_radius_3)
    .extrude(-hub_width_3)
)

# Central Shaft
# The shaft goes through the whole assembly
shaft_start_z = boss_z_start - hub_width_3 - 10 # sticking out a bit
shaft = (
    cq.Workplane("XY")
    .workplane(offset=shaft_start_z)
    .circle(shaft_radius)
    .extrude(shaft_length_total)
)

# Combine everything
result = (
    drum
    .union(flange_left)
    .union(flange_right)
    .union(hub_part_1)
    .union(hub_transition)
    .union(hub_part_2)
    .union(hub_part_3)
    .union(shaft)
)

# Add fillets to smooth transitions as seen in the render
# Fillet the junction between drum and inner flange faces
result = result.faces("|Z").edges(cq.selectors.RadiusNthSelector(1)).fillet(1.0)

# Optional: Fillet the transition from the large flange to the first hub stage
# result = result.edges(cq.selectors.NearestToPointSelector((0, 0, -flange_thickness))).fillet(0.5)