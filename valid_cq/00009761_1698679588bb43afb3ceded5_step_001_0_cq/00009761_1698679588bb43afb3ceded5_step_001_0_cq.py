import cadquery as cq

# Parameters
# Bottom section
bottom_od = 20.0  # Outer diameter of the bottom section
bottom_h = 10.0   # Height of the bottom section

# Middle section
middle_od = 26.0  # Outer diameter of the middle section
middle_h = 18.0   # Height of the middle section

# Top section (Head)
top_od = 32.0     # Outer diameter of the top section
top_h = 10.0      # Height of the top cylindrical section (before top bevel)

# Internal features
inner_bore_d = 16.0 # Through-hole diameter
countersink_angle = 45.0 # Angle of the top conical opening
countersink_depth = 5.0 # Depth of the conical part

# External features
top_chamfer_size = 2.0 # Chamfer on the top outer edge

# Create the solid geometry
# We will build this stack-up from bottom to top
result = (
    cq.Workplane("XY")
    # 1. Bottom Cylinder
    .circle(bottom_od / 2.0)
    .extrude(bottom_h)
    
    # 2. Middle Cylinder
    .faces(">Z")
    .workplane()
    .circle(middle_od / 2.0)
    .extrude(middle_h)
    
    # 3. Top Cylinder (Head)
    .faces(">Z")
    .workplane()
    .circle(top_od / 2.0)
    .extrude(top_h)
    
    # 4. Top outer chamfer
    .faces(">Z").edges()
    .chamfer(top_chamfer_size)
    
    # 5. Through-hole
    .faces(">Z")
    .workplane()
    .hole(inner_bore_d)
)

# 6. Create the countersink / conical entrance at the top
# We select the top face's inner edge (created by the hole) and chamfer it
# Alternatively, we can cut a cone. Given the smooth look, a chamfer or loft is good.
# Let's use a specific chamfer on the inner edge to create that funnel shape.
# We need to find the inner edge on the top face.

# Finding the top face
top_face = result.faces(">Z")

# Finding the inner circle edge on that face. 
# The outer edge has been chamfered, so the top face is an annulus.
# The inner edge corresponds to the bore.
result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(countersink_depth)

# Export or display the result (optional, standard practice for CQ scripts)
# show_object(result)