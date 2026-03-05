import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
rotor_outer_diameter = 280.0
rotor_thickness = 10.0  # Thickness of the braking surface

# Hub (Hat) dimensions
hub_diameter = 160.0
hub_height = 40.0       # Total height from the back face of the rotor disc
hub_wall_thickness = 6.0
hub_top_thickness = 8.0

# Center bore dimensions
center_bore_diameter = 65.0
center_lip_diameter = 70.0
center_lip_height = 3.0

# Stud/Lug dimensions
bolt_circle_diameter = 114.3  # Standard PCD (e.g., 5x114.3)
num_studs = 5
stud_diameter = 12.0
stud_length = 25.0
stud_head_diameter = 14.0 # For chamfer/visual effect
stud_head_height = 2.0

# --- Geometry Construction ---

# 1. Create the main braking disc
# We start with the large flat cylinder
# Z-axis is the axis of rotation
rotor_disc = cq.Workplane("XY").circle(rotor_outer_diameter / 2.0).extrude(rotor_thickness)

# 2. Create the "Hat" or Hub section
# This sits on top of the rotor disc
hub = (
    cq.Workplane("XY")
    .workplane(offset=rotor_thickness) # Start on top of the rotor disc
    .circle(hub_diameter / 2.0)
    .extrude(hub_height)
)

# 3. Combine initial shapes
result = rotor_disc.union(hub)

# 4. Create the hollow inside the hat (from the back)
# This removes material to make the hat wall thickness correct
# We cut from the bottom (Z=0) upwards
inner_cut_diameter = hub_diameter - (2 * hub_wall_thickness)
cut_depth = rotor_thickness + hub_height - hub_top_thickness

result = (
    result.faces("<Z")
    .workplane()
    .circle(inner_cut_diameter / 2.0)
    .cutBlind(cut_depth)
)

# 5. Create the Center Bore (through hole)
result = (
    result.faces(">Z")
    .workplane()
    .circle(center_bore_diameter / 2.0)
    .cutThruAll()
)

# 6. Create the small locating lip on the front face of the hub
lip = (
    cq.Workplane("XY")
    .workplane(offset=rotor_thickness + hub_height)
    .circle(center_lip_diameter / 2.0)
    .circle(center_bore_diameter / 2.0) # Hollow center
    .extrude(center_lip_height)
)
result = result.union(lip)


# 7. Create the Wheel Studs
# We'll create one stud and then use polar array
# Studs protrude from the top face of the hat

# Define the single stud geometry
stud = (
    cq.Workplane("XY")
    .workplane(offset=rotor_thickness + hub_height)
    .circle(stud_diameter / 2.0)
    .extrude(stud_length)
)

# Add a slight chamfer/fillet to the stud tip for realism
stud = stud.faces(">Z").chamfer(1.0)

# Create the pattern of studs
studs = (
    cq.Workplane("XY")
    .workplane(offset=rotor_thickness + hub_height)
    .polarArray(bolt_circle_diameter / 2.0, 0, 360, num_studs)
    .circle(stud_diameter / 2.0)
    .extrude(stud_length)
)
# Apply chamfer to all studs is tricky after bulk extrude without selecting carefully.
# Instead, let's union the single detailed stud in a loop or use the bulk shape.
# For simplicity and robustness, the bulk shape is usually fine, but let's add the detail.
# Re-doing studs with chamfer:

# Helper to make a stud at a specific angle
def make_stud(angle):
    s = (
        cq.Workplane("XY")
        .workplane(offset=rotor_thickness + hub_height)
        .transformed(rotate=cq.Vector(0, 0, angle))
        .center(bolt_circle_diameter/2.0, 0)
        .circle(stud_diameter/2.0)
        .extrude(stud_length)
    )
    # Add tip chamfer
    s = s.faces(">Z").chamfer(1.0)
    return s

# Create and union all studs
for i in range(num_studs):
    angle = i * (360.0 / num_studs)
    stud_geo = make_stud(angle)
    result = result.union(stud_geo)

# 8. Fillets and Finishing touches
# Add a fillet at the junction of the hat and the disc
try:
    result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(1)).fillet(5.0)
except:
    # Fallback if selector is ambiguous, though for this geometry usually fine
    pass

# Add a small chamfer to the outer edge of the rotor for realism
result = result.faces("<Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(1.0)
result = result.faces(">Z[1]").edges(cq.selectors.RadiusNthSelector(0)).chamfer(1.0)

# Export or display
# show_object(result) # Used in CQ-editor