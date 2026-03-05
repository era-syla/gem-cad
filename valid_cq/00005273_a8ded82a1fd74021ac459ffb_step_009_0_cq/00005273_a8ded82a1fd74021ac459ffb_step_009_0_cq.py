import cadquery as cq

# Parameters
base_diameter = 50.0       # Diameter of the bottom base
top_diameter = 40.0        # Diameter of the top surface
total_height = 30.0        # Total height of the tapered section
chamfer_height = 5.0       # Height of the bottom chamfer/bevel
chamfer_diameter = 45.0    # Diameter where the chamfer starts

# Slot parameters
slot_width = 12.0          # Width of the cuts
slot_depth = 15.0          # Depth of the cuts from the top
cross_bar_width = 12.0     # Width of the center connecting bar (perpendicular to slots)
hole_diameter = 5.0        # Diameter of the side holes

# 1. Create the main body
# We'll create a profile and revolve it, or loft circles. 
# A loft is simple here: Bottom circle -> Middle Circle (for chamfer) -> Top Circle
main_body = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .workplane(offset=chamfer_height)
    .circle(chamfer_diameter / 2)
    .workplane(offset=total_height - chamfer_height)
    .circle(top_diameter / 2)
    .loft(combine=True)
)

# 2. Create the H-shaped cutout (or rather, the two parallel side slots)
# Looking at the image, there are two large rectangular chunks removed from the sides,
# leaving a central bridge. 

# Let's cut the two parallel slots first.
# We need to cut everything EXCEPT the central bridge.
# The cuts go inwards from the perimeter.
cut_volume = (
    cq.Workplane("XY")
    .workplane(offset=total_height)  # Start at top
    .rect(base_diameter * 1.5, slot_width) # Create a rectangle larger than diameter
    .extrude(-slot_depth) # Cut downwards
)

# Actually, looking closer at the image, it's not a single slot.
# It looks like an 'H' shape of *material* is left, or conversely, 
# four corners are cut, or two parallel slots are cut perpendicular to a central slot?
# Let's re-examine the negative space.
# Negative space: Two wide rectangular channels running parallel, leaving a strip in the middle.
# Then there is a cross channel? No.
# It looks like two deep notches on opposite sides.
# Let's assume the "material" forms a bridge.
# The cuts are two parallel slots, removing material on the "left" and "right" of a central bar.
# Wait, looking at the top face, there is a central solid bar, and two solid "ears" on the sides.
# The empty space forms a cross (or a 'plus' sign).
# Let's try cutting a Cross shape.

# Cut 1: The main slot across the diameter
slot1 = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .rect(base_diameter * 1.5, slot_width)
    .extrude(-slot_depth)
)

# Cut 2: The perpendicular slot
slot2 = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .rect(slot_width, base_diameter * 1.5)
    .extrude(-slot_depth)
)

# Combine cuts
# result = main_body.cut(slot1).cut(slot2) 
# This would create 4 isolated pillars if the cuts are deep enough, or a cross-shaped hole.
# The image shows a solid continuous rim, but broken by the cuts? 
# No, the perimeter is interrupted. 
# The image shows a central solid hub is NOT present. The center is empty? No, the center is solid.
# Let's look at the "H". The light gray top surface forms an H shape.
# This means material is REMOVED in the four quadrants? No.
# If the top surface is an H, then there are two rectangular cuts entering from the sides.
# Let's look at the vertical faces inside the cut.
# It creates a channel.
# Let's assume the shape is defined by two wide rectangular cuts entering from opposite sides,
# but not going all the way through, or meeting a perpendicular cut.

# Let's try a different approach based on the resulting solid geometry.
# The solid looks like a cone with two specific rectangular slots cut into it.
# One slot goes all the way across (let's say X-axis).
# The other slot goes across the Y-axis.
# This results in 4 pillars.
# BUT, the image shows two holes going through the material.
# The holes go through the "walls" created by the cuts.

# Let's look really closely at the top face.
# It looks like the letter "H" rotated 90 degrees.
# There is a continuous bar running "vertical" in the image perspective.
# There are two short arms sticking out.
# This implies two rectangular cuts were made from the "left" and "right" (in image perspective),
# leaving a bridge in the middle.
# Then, perpendicular to that, there seems to be another cut or just the curvature?
# Actually, it looks like a single cross-shaped cut.
# Let's assume it's a cross-shaped cut (two slots crossing at 90 deg).
# Width of cut 1 = slot_width.
# Width of cut 2 = slot_width.
# If we do that, we get 4 standing legs.
# But the image shows the legs are connected? No, they look separated at the top.
# Wait, look at the shadow in the near-left quadrant. The top surface is continuous?
# No, the top surface is definitely interrupted.
# It looks exactly like a Phillips head screw drive or a clutch drive.
# A simple Cross Cut (Phillips style) creates 4 independent segments if it cuts the perimeter.
# Let's assume the cuts go all the way to the edge.

# RE-EVALUATION:
# Look at the holes. They go through the faces created by one of the slots.
# The holes are aligned.
# This suggests there is a central solid block? No, the holes go through the "fins".
# Let's look at the near corner. It's a wedge shape.
# There are 4 wedges.
# It creates a "Castellated" appearance.
# Let's assume the standard design for a generic drive dog or clutch.
# It's usually a main body with a cross slot.

# Let's generate a Cross Slot cut and see if it matches the features.
# - Tapered body: Yes.
# - Cross cut from top: Yes.
# - Holes: Through the remaining "teeth".

# Refined Plan:
# 1. Make the tapered cylinder.
# 2. Cut a "Plus" (+) shape from the top.
# 3. Drill holes through the resulting segments.

# Dimension Tuning:
# The cuts look quite wide. Let's say slot_width is about 1/3 of top diameter.
# Top diameter = 40, slot_width = 12.
# Cut depth = 15 (half height).

# Hole placement:
# The holes seem to go through the thickness of the "teeth".
# They appear to be perpendicular to the flat faces of the cut.
# Let's place them on the X and Y axes, going through the center of the wedges?
# No, the image shows the hole on the flat face created by the cut.
# This means the drilling axis is perpendicular to the slot face.
# If we have a slot along Y-axis, the face normal is X. We drill along X.
# If we have a slot along X-axis, the face normal is Y. We drill along Y.
# The image shows two holes visible. One on the left face of the front-right wedge.
# One on the right face of the front-left wedge.
# It looks like a single hole drilled all the way through the slot?
# No, that would mean drilling through empty space.
# It looks like the hole goes into the material.
# Let's assume there is a hole in each "wing" face.

# Let's build the basic body first.
result = main_body

# Create the cross cut
# Slot along Y axis
cut_y = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .rect(slot_width, base_diameter * 1.5)
    .extrude(-slot_depth)
)

# Slot along X axis
cut_x = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .rect(base_diameter * 1.5, slot_width)
    .extrude(-slot_depth)
)

# Apply cuts
result = result.cut(cut_y).cut(cut_x)

# Now the holes.
# The holes appear on the flat vertical faces inside the slots.
# Looking at the image, inside the "front" slot, on the right wall, there is a hole.
# On the left wall, there is a hole.
# These holes seem to go into the quadrants.
# Are they through holes? It's hard to tell. Let's assume they are blind or through the specific quadrant.
# Given typical engineering parts (like a locking cap), these might be for a locking wire or pin.
# Let's drill through the quadrants.
# The easiest way is to drill perpendicular to the slot faces.
# Center of hole Z: offset from top by some amount (e.g., slot_depth / 2).
# Center of hole XY: centered in the slot opening? No, centered on the face width.
# The face width varies because of the conical shape.
# Let's place the holes at a specific radius from the center.

hole_z_pos = total_height - (slot_depth / 2.0)

# Create a workplane on the side of the cut and drill
# We need holes in the faces of the resulting "pillars".
# A simpler way is to construct a cylinder and cut it.
# Let's assume the holes go through the slot walls into the pillars.
# Let's assume 4 holes, one in each direction, or 1 hole passing through the entire assembly?
# If a hole passes through the entire assembly (e.g. along X axis), it would pass through open air in the Y-slot.
# The image shows the hole *start* at the slot face.
# It looks like a hole connecting the two slots? No.
# It looks like a hole going into the solid part.
# Let's create a Workplane on the XZ plane, move it to Y=slot_width/2, and drill into positive Y.
# And mirror/pattern this.

# Defined: 4 holes, located on the flat faces of the slots, pointing into the quadrants.
# Position Z: Mid-depth of slot.
# Position Radial: Some radius to center it on the pillar.
# Actually, looking at the image, the hole is visible on the face perpendicular to the viewing angle.
# Let's put holes on all 8 internal faces? Or just one per pillar?
# The image shows two holes. One on the face of the front-right pillar facing the front-left pillar.
# One on the face of the front-left pillar facing the front-right pillar.
# This suggests a single drilling operation going through the X-axis (if front is Y).
# BUT the center is empty space (the slot).
# So it's two collinear holes.

# Let's execute two "drilling" operations across the whole part, but confined to the solid.
# If we define a cylinder along the X axis and Cut, it will cut the pillars on the left/right of the Y-slot.
# If we define a cylinder along the Y axis and Cut, it will cut the pillars on top/bottom of the X-slot.
# The image shows holes in the faces parallel to the slot.
# This confirms the "Drill Through" hypothesis (interrupted by the slot).

# Let's refine the shape slightly.
# The bottom part has a distinct bevel/chamfer.
# The "base" is actually a smaller chamfer section.
# Base (d=50) -> Height 5 -> Dia 45 (Wait, base is wider? Image: Bottom looks slightly narrower? No, top is narrower.)
# Let's look at the bottom rim. It tapers OUT then goes straight?
# No, standard chamfer: Cylinder -> Chamfer -> Top.
# The image shows: Bottom face -> Taper outwards (chamfer) -> Main body taper inwards.
# Actually, it looks like:
# Bottom Base (Small) -> Chamfer out -> Max Diameter -> Taper in -> Top.
# Let's look at the bottom curve. It curves UP and OUT.
# Then a sharp edge.
# Then Tapers UP and IN.
# Let's adjust dimensions:
# Bottom Face Dia: 45
# Shoulder Dia (at h=5): 50
# Top Face Dia (at h=30): 40

# Code Construction:
# 1. Loft: Circle(45) @ Z0 -> Circle(50) @ Z5 -> Circle(40) @ Z30
# 2. Cut Cross: Rect(100, 12) centered, and Rect(12, 100) centered. Depth 15 from Z30.
# 3. Cut Holes: 
#    - Cylinder along X axis, Z = 30 - 15/2 = 22.5. Radius = 2.5.
#    - Cylinder along Y axis, Z = 22.5. Radius = 2.5.
#    Note: This will cut holes through the "pillars".

result = (
    cq.Workplane("XY")
    .circle(45.0/2) # Bottom
    .workplane(offset=5.0)
    .circle(50.0/2) # Shoulder
    .workplane(offset=25.0) # Total height 30
    .circle(40.0/2) # Top
    .loft(combine=True)
)

# Define the cross cuts
# Create a sketch for the removal? Or just boolean cuts.
# Boolean cuts are robust here.

cut_depth = 12.0 # Looks a bit deeper than width
cw = 14.0 # Cross width

# Slot 1
c1 = (
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .rect(100, cw)
    .extrude(-cut_depth)
)

# Slot 2
c2 = (
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .rect(cw, 100)
    .extrude(-cut_depth)
)

result = result.cut(c1).cut(c2)

# Holes
# Position Z roughly middle of the cut
hz = 30.0 - (cut_depth / 2.0)
hd = 5.0 # Hole diameter

# Drill X axis
h1 = (
    cq.Workplane("YZ")
    .workplane(offset=-50) # Start outside
    .center(0, hz)
    .circle(hd/2)
    .extrude(100)
)

# Drill Y axis
h2 = (
    cq.Workplane("XZ")
    .workplane(offset=-50)
    .center(0, hz)
    .circle(hd/2)
    .extrude(100)
)

result = result.cut(h1).cut(h2)

# Final check of the image
# The chamfer at the bottom looks like a "chamfer", i.e., linear transition.
# The main body is conical.
# The cuts are sharp.
# The holes are clearly visible.

# One small detail: The "H" shape in the prompt thought process vs the "Cross" shape.
# If I look strictly at the top grey pixels, it's 4 distinct islands.
# So a Cross cut is the correct interpretation.

# Adjusting parameters to better match image visual proportions
# Height looks slightly shorter relative to width.
# Base = 50. Height = 30 seems ok.
# Top = 40.
# Cut width looks fairly chunky. 14mm on a 40mm top is substantial (1/3rd). Looks about right.
# Cut depth: Looks like 40% of total height. 12mm on 30mm height. Looks good.
# Bottom chamfer: Looks like bottom face is maybe 38, expanding to 50?
# Let's stick to 45 -> 50.

result = result