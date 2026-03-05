import cadquery as cq

# --- Parametric Dimensions for 608RS Bearing ---
# Standard ISO dimensions for a 608 bearing:
# Inner Diameter (ID): 8mm
# Outer Diameter (OD): 22mm
# Width (W): 7mm
inner_diameter = 8.0
outer_diameter = 22.0
width = 7.0

# Derivations and cosmetic details
inner_radius = inner_diameter / 2.0
outer_radius = outer_diameter / 2.0
seal_recess_depth = 0.5  # Depth of the rubber seal recess
seal_recess_width = 1.0  # approximate width of the gap between races
inner_race_wall = 2.0    # Thickness of inner race ring
outer_race_wall = 2.0    # Thickness of outer race ring

# Chamfer sizes
chamfer_size = 0.3

# --- Modeling Strategy ---
# 1. Create the main outer cylinder.
# 2. Cut the center hole.
# 3. Create recesses for the seals on top and bottom faces to simulate the race separation.
# 4. Add chamfers to the edges for a realistic look.
# Note: Since the prompt asks for the geometry shown (which looks like a simplified solid representation
# with the seal flush or slightly recessed), we will model it as a solid assembly representation.

# 1. Create the base cylinder (Outer Race boundary)
base = cq.Workplane("XY").circle(outer_radius).extrude(width)

# 2. Create the through hole (Inner Race boundary)
# We subtract the inner diameter cylinder
result = base.faces(">Z").workplane().hole(inner_diameter)

# 3. Create the Seal Recesses (The groove separating inner and outer races)
# We need a groove on the top and bottom faces.
# The groove sits between the inner race and outer race.
# Let's calculate the center radius of the groove.
groove_outer_r = outer_radius - outer_race_wall
groove_inner_r = inner_radius + inner_race_wall

# We'll cut a ring on the top face
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(0, 0)
    .circle(groove_outer_r)
    .circle(groove_inner_r)
    .cutBlind(-seal_recess_depth)
)

# We'll cut a ring on the bottom face
result = (
    result.faces("<Z")
    .workplane()
    .moveTo(0, 0)
    .circle(groove_outer_r)
    .circle(groove_inner_r)
    .cutBlind(-seal_recess_depth)
)

# 4. Adding Chamfers
# Standard bearings have chamfers on the inner bore edges and outer edges.
# Select outer edges
result = result.edges(cq.selectors.RadiusNthSelector(0)).chamfer(chamfer_size) # Inner hole edges
result = result.edges(cq.selectors.RadiusNthSelector(-1)).chamfer(chamfer_size) # Outer cylinder edges

# Optional: Add the "608RS" text. 
# While 3D text can be computationally heavy or font-dependent, 
# adding a simple emboss adds significant realism matching the image.
text_string = "608RS"
text_size = 2.5
text_depth = 0.1
text_radius = (groove_inner_r + groove_outer_r) / 2.0 

# To place text in a circular pattern or simply on the seal face:
# We will place it on the seal surface (the face resulting from the cut in step 3).
# We need to select the annular face created by the cut.
# A simple way is to select faces parallel to XY, at the recess depth.

try:
    # Attempt to find the recessed face to emboss text
    seal_face = result.faces(cq.selectors.ParallelDirSelector((0,0,1))).faces(
        cq.selectors.NearestToPointSelector((text_radius, 0, width - seal_recess_depth))
    )
    
    # We will create the text on a separate workplane and cut it
    # Rotating text around a circle is complex in basic CQ without plugins,
    # so we will place the text straight or along an arc if possible.
    # For simplicity and robustness in this snippet, we place it centered.
    
    # Creating a text object
    result = (
        seal_face.workplane()
        .text(text_string, fontsize=text_size, distance=-text_depth, font="Arial", kind="regular", halign="center", valign="center")
    )
except Exception:
    # Fallback if text generation fails (e.g. font missing) or face selection is ambiguous
    pass

# Ensure the final object is named 'result'
result = result