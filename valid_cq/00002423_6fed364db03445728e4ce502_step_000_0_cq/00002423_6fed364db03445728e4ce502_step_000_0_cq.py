import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions
base_diameter = 40.0
base_height = 20.0
total_height = 45.0

# Central Shaft/Hub dimensions
shaft_outer_diameter = 12.0
shaft_inner_diameter = 9.0
shaft_height = total_height

# Rib/Key dimensions
rib_thickness = 3.0
rib_protrusion = 2.0  # How much the ribs stick out from the shaft
num_ribs = 4

# Base Dome features
dome_wall_thickness = 4.0
rim_height = 5.0 # Height of the straight cylindrical part of the base before the dome starts
rim_thickness = 2.0

# Fillets
fillet_radius = 0.5
inner_fillet_radius = 1.0

# --- Modeling ---

# 1. Create the Domed Base
# We'll create a semi-sphere or truncated sphere.
# Let's use a revolution of a profile.
sphere_radius = base_diameter / 2.0

# Create the outer shell profile
base_outer = (
    cq.Workplane("XY")
    .sphere(sphere_radius)
    # Cut off the top to make it the right height if needed, 
    # but the image looks like a flattened hemisphere or just a section of a sphere.
    # Let's stick with a half-sphere but truncated at the bottom to flat? 
    # No, looking at the image, it's a hemisphere that transitions into a cylinder.
    # Actually, it looks like a revolution of an arc.
)

# Let's construct the base using a more precise revolution approach to get the rim and hollow center.
def base_profile(r_outer, h_straight, r_dome, wall_thk):
    # Determine points for the outer profile
    # Start at bottom center (0, -h_dome) ... wait, let's keep bottom at Z=0?
    # No, usually easier to build up. Let's make the bottom of the dome Z=0.
    
    # Let's model the base as a solid revolution first.
    # Outer radius is r_outer.
    # The bottom is rounded. Let's assume a semi-circle profile for the bottom section.
    
    sk = (
        cq.Sketch()
        .segment((0, 0), (r_outer, 0)) # Top flat face of base (at rim)
        .segment((0, -h_straight)) # Vertical down (rim)
        # Create an arc for the bottom bowl shape. 
        # For simplicity, let's use a 3-point arc or fillet, but a large fillet on a rectangle is easier.
        .close()
    )
    return sk

# Alternative approach: Construct solids boolean-wise.

# Step 1: The Base "Bowl"
# A solid cylinder with a massive fillet on the bottom edge to create the bowl shape.
base_cyl_height = base_height
base_solid = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_cyl_height)
    .edges("<Z")
    .fillet(base_diameter / 2.0 - 0.1) # Almost a full hemisphere
)

# Step 2: Hollow out the base to make it a shell
# We shell the solid, keeping the top face open.
base_shell = base_solid.faces(">Z").shell(-dome_wall_thickness)

# Step 3: Create the Central Shaft (Hollow Cylinder)
shaft = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start from bottom? No, shaft goes through.
    .circle(shaft_outer_diameter / 2.0)
    .circle(shaft_inner_diameter / 2.0) # Hollow it out immediately
    .extrude(total_height)
)

# Move base shell to align with shaft. The shaft starts at Z=0.
# The base solid was extruded up. Let's move the base so its top is somewhere up the shaft?
# Looking at the image, the base is at the bottom.
# Let's re-orient. The base "rim" is the top of the bowl.
# The shaft extends significantly above the rim.

# Let's shift the Z of the shaft so it starts slightly below the base inside,
# or just union them properly.
# The base currently sits from Z=0 to Z=20.
# The shaft sits from Z=0 to Z=45.
# This looks correct for alignment.

# Step 4: Add the ribs (Cruciform shape on the shaft)
# The ribs extend from the shaft outwards and connect to the inside of the bowl?
# In the image, the ribs connect the central shaft to the "floor" of the bowl,
# but they also run up the side of the shaft.
# Crucially, the ribs form a '+' shape at the top of the shaft.

rib_profile = (
    cq.Workplane("XY")
    .rect(rib_thickness, (shaft_outer_diameter + 2*rib_protrusion))
    .rect((shaft_outer_diameter + 2*rib_protrusion), rib_thickness)
)

# Extrude the ribs up to the top of the shaft
ribs = rib_profile.extrude(total_height)

# Now we need to connect the ribs to the inside of the bowl.
# The ribs in the image seem to flare out or connect to the bottom curvature.
# However, simpler is to union them. The provided image shows the ribs
# are 'cut' or contained within the shaft diameter mostly, but stick out slightly (splines/keys).
# Looking closer at the TOP of the shaft:
# There are 4 protrusions. They look like keys.
# Let's refining the rib geometry. They run the full length.

# Let's combine Shaft + Ribs first.
shaft_assembly = shaft.union(ribs)

# Step 5: Connecting structure inside the bowl.
# There are stiffeners inside the bowl connecting the shaft to the bowl wall?
# Looking at the image: The "Ribs" *flare out* at the bottom to merge with the bowl floor.
# It looks like a web.
# To achieve this simple sweeping shape, we can create a lower structural reinforcement.

# Create a cross shape that is wider at the bottom (inside the bowl) and tapers or is cut by the bowl.
lower_support_height = base_height - 2.0 # Slightly below rim
lower_support_width = base_diameter - 2*dome_wall_thickness # Inside width

support_cross = (
    cq.Workplane("XY")
    .rect(rib_thickness, lower_support_width)
    .rect(lower_support_width, rib_thickness)
    .extrude(lower_support_height)
    .intersect(base_solid) # Intersect with a solid version of the base to conform to curvature
)
# Note: intersect(base_solid) works if base_solid is full.
# Our base_shell is hollow.
# Let's recreate a dummy solid for intersection.
dummy_solid = (
    cq.Workplane("XY")
    .circle((base_diameter / 2.0) - dome_wall_thickness) # Inner radius
    .extrude(base_height)
    .edges("<Z")
    .fillet((base_diameter / 2.0) - dome_wall_thickness - 0.1)
)

# The support ribs need to be cut by this dummy inner shape, but they exist *inside* it?
# No, they connect the shaft to the inner wall.
# So we need a union of the shaft and the inner wall?
# Actually, the image shows the ribs getting *wider* (radially) as they go down into the bowl?
# No, looking closely, the ribs on the shaft are constant width.
# There is a separate, lower set of ribs connecting the shaft to the outer shell.
# Let's assume the support cross is simply the union of the shaft ribs and the shell,
# but likely there is a web.

# Let's try a simpler approach for the specific geometry visible:
# 1. Shaft with key-ribs (constant profile).
# 2. Bowl (shell).
# 3. Four webs connecting shaft to bowl.

# Redefine Ribs/Keys on Shaft
shaft_keys_sk = (
    cq.Sketch()
    .rect(rib_thickness, shaft_outer_diameter + 2.0*rib_protrusion)
    .rect(shaft_outer_diameter + 2.0*rib_protrusion, rib_thickness)
)
shaft_keys = cq.Workplane("XY").placeSketch(shaft_keys_sk).extrude(total_height)

# Redefine Base
# Let's make the base slightly more complex to match the rim.
base_sk = (
    cq.Sketch()
    .segment((0, 0), (base_diameter/2, 0)) # Top
    .segment((0, -rim_height)) # Rim vertical
    .arc((0.1, -base_height), (base_diameter/4, -base_height + 5)) # Bottom curve approximation
    .close()
    .assemble()
)
# Actually, standard primitives are safer and robust.
base_main = (
    cq.Workplane("XY")
    .circle(base_diameter/2)
    .extrude(rim_height) # The vertical rim
)
base_bottom = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start at bottom of rim, extruding down? 
    # Let's build up.
    # Bowl bottom (hemisphere-ish)
    .sphere(base_diameter/2)
    # Cut top to make it a bowl
    .cut(cq.Workplane("XY").rect(base_diameter*2, base_diameter*2).extrude(base_diameter))
)
# Re-orient base_bottom to be the bottom half
base_bottom = base_bottom.mirror("XY") 

# This is getting messy with primitives. Let's use a revolve for the main cup shape.
# Profile for the cup:
#   |
#   |___
#  /    \
p_outer_r = base_diameter / 2.0
p_inner_r = p_outer_r - dome_wall_thickness
p_rim_h = 5.0
p_bowl_depth = 15.0 # Total height approx 20

def cup_profile(h_rim, depth, r_out, r_in):
    # Points defined in XZ plane, revolution around Z
    pts = [
        (r_out, 0), # Top outer rim
        (r_out, -h_rim), # Bottom of straight rim
        (0, -depth), # Bottom center (approx, will control with tangent)
        (0, -depth + (r_out-r_in)), # Inner bottom center
        (r_in, -h_rim), # Inner bottom of rim
        (r_in, 0), # Top inner rim
    ]
    
    # We need a nice curve for the bowl.
    # Using spline or 3-point arcs.
    # Outer arc: from (r_out, -h_rim) to (0, -depth)
    # Inner arc: from (0, -depth+thk) to (r_in, -h_rim)
    
    res = (
        cq.Workplane("XZ")
        .moveTo(r_out, 0)
        .lineTo(r_out, -h_rim)
        .threePointArc((r_out*0.7, -depth*0.85), (0, -depth)) # Outer curve
        .lineTo(0, -depth + (r_out - r_in)) # Thickness at bottom
        .threePointArc((r_in*0.7, -depth*0.85 + (r_out-r_in)), (r_in, -h_rim)) # Inner curve
        .lineTo(r_in, 0)
        .close()
    )
    return res

cup = cup_profile(p_rim_h, base_height, p_outer_r, p_inner_r).revolve()

# Center Shaft
shaft_complete = (
    cq.Workplane("XY")
    .circle(shaft_outer_diameter/2.0)
    .circle(shaft_inner_diameter/2.0)
    .extrude(total_height)
    .translate((0,0,-base_height)) # Move down to align with cup bottom
)

# Keys on shaft
keys = (
    cq.Workplane("XY")
    .rect(rib_thickness, shaft_outer_diameter + 2*rib_protrusion)
    .rect(shaft_outer_diameter + 2*rib_protrusion, rib_thickness)
    .extrude(total_height)
    .translate((0,0,-base_height))
)

# Internal Webs (Connecting shaft to cup)
# They fit inside the cup height.
web_height = base_height - 5.0 # Keep them inside the cup
web_thk = rib_thickness

webs = (
    cq.Workplane("XY")
    .rect(web_thk, base_diameter) # Span full width
    .rect(base_diameter, web_thk)
    .extrude(web_height)
    .translate((0,0,-base_height))
    .intersect(cup) # Trim to fit inside the cup geometry
)

# Combine everything
part = cup.union(shaft_complete).union(keys).union(webs)

# Post-processing: Cuts and details
# The shaft is hollow, ensure keys don't block it
part = part.cut(
    cq.Workplane("XY")
    .circle(shaft_inner_diameter/2.0)
    .extrude(total_height*2)
    .translate((0,0,-total_height))
)

# Add chamfer/fillets
# Top of shaft keys looks chamfered or just plain.
# Fillet the junction between shaft and cup floor?
# The image shows a smooth transition (fillet) where the shaft meets the internal webs/cup.

try:
    part = part.edges("(>Z[-25] and <Z[-10]) and %CIRCLE").fillet(1.0) # Internal bottom fillets
except:
    pass # Fillets can be fragile

# Move to Z=0 for final result
result = part.translate((0, 0, base_height))

# Final check of the image:
# There is a small groove/lip on the rim of the base.
# Let's add that groove.
groove = (
    cq.Workplane("XY")
    .circle(p_outer_r - 1.0)
    .circle(p_outer_r - 1.5)
    .extrude(0.5)
    .translate((0,0, base_height))
)
# Actually, the image shows a step on the outer diameter.
# We can cut a small groove.
result = result.cut(
    cq.Workplane("XZ")
    .moveTo(p_outer_r, base_height - 2.0)
    .circle(0.5)
    .revolve()
)

# Rotate to match image orientation roughly (not strictly required but nice)
# Image shows isometric view.

# Re-verify the shaft top. The keys are flush with the top face.
# The hole goes all the way through.

# One detail: The ribs inside the bowl are likely just extensions of the shaft keys.
# My "webs" logic covers this.

# Refine fillets: The junction between the vertical ribs and the horizontal "floor" of the cup has a large fillet.
# This suggests the web shape logic was correct.

# Cleanup
result = result