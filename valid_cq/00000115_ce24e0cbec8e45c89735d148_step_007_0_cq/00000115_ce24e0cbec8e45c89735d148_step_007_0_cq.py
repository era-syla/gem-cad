import cadquery as cq
import math

# --- Parameters ---
diameter = 60.0         # Total diameter of the heatsink
total_height = 15.0     # Total height
base_height = 5.0       # Height of the solid base portion
fin_height = 10.0       # Height of the cooling fins
num_fins = 7            # Number of fins on each side (roughly)
fin_thickness = 2.0     # Thickness of each fin
fin_spacing = 2.5       # Gap between fins
center_hole_diam = 10.0 # Diameter of the threaded hole (simplified as smooth hole)
recess_diam = 20.0      # Diameter of the central recessed area
recess_depth = 5.0      # Depth of the central recess (conical/spherical)
bolt_circle_diam = 42.0 # Diameter for the 4 mounting holes
bolt_hole_diam = 3.5    # Diameter of mounting holes
bolt_head_diam = 6.0    # Counterbore diameter for mounting holes

# --- Derived Parameters ---
radius = diameter / 2.0

# --- Construction ---

# 1. Base Cylinder
# Start with the full cylinder block
base = cq.Workplane("XY").circle(radius).extrude(total_height)

# 2. Creating the Fins
# We will create a "cutter" object to remove material between fins.
# Instead of modeling fins, we model the air gaps (slots) and cut them away.
# The slots run parallel to the X-axis.

slot_width = fin_spacing
fin_pitch = fin_thickness + fin_spacing

# Create a sketch for the slots
# We need to cut slots across the top face, reaching down to base_height.
# The cuts go perpendicular to Y axis.

# Calculate how many slots fit
max_offset = radius - (fin_pitch)
offsets = []
current_offset = 0
while current_offset < max_offset:
    offsets.append(current_offset)
    if current_offset != 0:
        offsets.append(-current_offset)
    current_offset += fin_pitch

# Create a cutting tool for the slots
cutter = cq.Workplane("XY").workplane(offset=base_height)

for offset in offsets:
    # We create a rectangle long enough to cut through the whole circle at this offset
    # Length needs to be > diameter
    rect_length = diameter + 10.0
    
    # Calculate position. The center of the slot is 'offset'.
    # But wait, looking at the image, there is a central fin, not a central gap.
    # So the offsets should be shifted. Let's adjust logic.
    # Center is at Y=0. Let's put a fin there. So gaps are at +/- (fin_thickness/2 + gap_width/2)
    pass

# Revised Fin Logic:
# Let's create a single large block and cut slots into it.
# Central Fin is centered on Y=0.
# First gap center is at Y = +/- (fin_thickness/2 + fin_spacing/2)
gap_center_start = (fin_thickness + fin_spacing) / 2.0

# Define a single slot cutter profile
def create_slot_cutters():
    # Start on the top face
    wp = cq.Workplane("XY").workplane(offset=base_height)
    
    slots = []
    
    # Generate Y coordinates for slot centers
    y_positions = []
    y = gap_center_start
    while y < radius:
        y_positions.append(y)
        y_positions.append(-y)
        y += (fin_thickness + fin_spacing)
        
    for y_pos in y_positions:
        # Create a rectangular wire for the slot
        # It needs to be wider than the diameter
        rect = (cq.Workplane("XY")
                .workplane(offset=base_height)
                .center(0, y_pos)
                .rect(diameter * 1.2, fin_spacing)
                .extrude(fin_height + 1.0) # Extrude up to cut
               )
        slots.append(rect)
    
    # Combine all slots into one compound
    if slots:
        compound_slots = slots[0]
        for s in slots[1:]:
            compound_slots = compound_slots.union(s)
        return compound_slots
    return None

slot_tool = create_slot_cutters()

# Cut the fins
if slot_tool:
    result = base.cut(slot_tool)
else:
    result = base

# 3. Central Recess
# The image shows a smooth, bowl-like recess in the center.
# We cut a sphere or revolve a profile. Let's use a revolved cut for control.
recess_profile = (
    cq.Workplane("XZ")
    .workplane(offset=total_height)
    .moveTo(0, 0)
    .lineTo(recess_diam/2, 0)
    # Create a spline or arc down to the center hole
    .threePointArc((recess_diam/4, -recess_depth*0.6), (center_hole_diam/2, -recess_depth))
    .lineTo(0, -recess_depth)
    .close()
)

recess_cut = recess_profile.revolve(360, (0,0,0), (0,1,0)) # Revolve around Z (which is Y in this local XZ plane logic? No, need explicit axis)
# Actually, easier to just do a simple sphere cut or a countersink
# Let's try a simpler countersink approach on the main result
result = result.faces(">Z").workplane().circle(recess_diam/2).cutBlind(-recess_depth, taper=45) # Simplified taper

# Refine Recess: The image shows a curved bowl. Let's do a sphere cut.
sphere_radius = (recess_depth**2 + (recess_diam/2)**2) / (2*recess_depth)
# Center of sphere needs to be at Z = total_height - recess_depth + sphere_radius
sphere_center_z = total_height - recess_depth + sphere_radius

# We need to recreate the sphere cut correctly
sphere_cutter = cq.Workplane("XY").workplane(offset=sphere_center_z - sphere_radius).sphere(sphere_radius)
# We only want to cut the top part
result = result.cut(sphere_cutter)


# 4. Central Hole (Threaded usually, represented as cylinder)
result = result.faces(">Z").workplane().hole(center_hole_diam, depth=total_height)

# 5. Mounting Holes (Counterbored)
# There are 4 holes in a pattern, cutting through the fins.
# The image shows the counterbore cuts through the fins nicely.

# We define the locations
locations = [(bolt_circle_diam/2 * math.cos(math.radians(angle)), 
              bolt_circle_diam/2 * math.sin(math.radians(angle))) 
             for angle in [45, 135, 225, 315]]

# Perform the cuts
# First the through holes
result = (result.faces(">Z").workplane()
          .pushPoints(locations)
          .hole(bolt_hole_diam))

# Now the counterbores (Clearance for tool head)
# These need to go deep enough to clear the fins and slightly into the base
cb_depth = fin_height + 2.0 # Ensure it cuts through fins into the solid part a bit
result = (result.faces(">Z").workplane()
          .pushPoints(locations)
          .hole(bolt_head_diam, depth=cb_depth))


# 6. Fillets and Chamfers
# The image shows the fins have rounded outer edges where they meet the cylinder wall.
# This is naturally handled by the initial cylinder shape.
# However, there is often a chamfer on the top edge of the fins.

# Let's select edges on the top Z plane that are part of the fins and fillet/chamfer them.
# This can be computationally expensive or fragile, so we apply a general fillet to top edges.
# The image shows a distinct chamfer/fillet on the outer circular rim.
result = result.edges(cq.selectors.RadiusNthSelector(0)).fillet(1.0)

# Optional: Fillet the bottom edge
result = result.edges("<Z").fillet(0.5)

# Visual polish: The central recess often has a small chamfer at the rim
# Finding that specific edge selector is tricky, so we omit for robustness.

# Final cleanup to ensure result variable is returned clearly
result = result