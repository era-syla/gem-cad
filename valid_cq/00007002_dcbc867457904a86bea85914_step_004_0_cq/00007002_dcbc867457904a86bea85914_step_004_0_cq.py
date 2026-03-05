import cadquery as cq
import math

# --- Parametric Dimensions ---
track_radius = 50.0       # Radius of the inner surface of the belt
track_width = 25.0        # Width of the track
track_thickness = 2.0     # Thickness of the base belt
num_segments = 36         # Number of tread segments around the circumference

# Outer Tread (Chevron Pattern) parameters
tread_height = 2.0        # Height of the outer lugs
tread_gap = 2.0           # Gap between chevrons
chevron_angle = 45.0      # Angle of the chevron "V" shape
lug_width_ratio = 0.7     # How much of the segment width the lug occupies

# Inner Drive Lug parameters
inner_lug_height = 4.0    # Height of the inner drive teeth
inner_lug_thickness = 3.0 # Thickness of the inner drive teeth along the circumference
inner_lug_width = 8.0     # Width of the inner drive teeth (transverse)
inner_lug_inset = 4.0     # Distance from edge (though typically centered or dual-row)
                          # Looking at image, it looks like a single row of lugs in the middle-ish, 
                          # but actually the image shows a central gap and lugs on the sides? 
                          # Let's look closer. 
                          # The image shows inner lugs that are extensions of the outer pattern 
                          # wrapping around, or distinct blocks. 
                          # Actually, looking at the inner surface, there are two rows of teeth 
                          # at the edges, and a smooth center. 
                          # Let's model them as side guide teeth.

side_lug_width = 4.0      # Width of the inner side lugs
side_lug_length = 4.0     # Length along the belt
side_lug_height = 4.0     # Height sticking inwards

# Derived calculations
circumference = 2 * math.pi * track_radius
segment_arc_length = circumference / num_segments
segment_angle = 360.0 / num_segments

# --- Geometry Construction ---

# 1. Create the base belt ring
base_belt = (
    cq.Workplane("XY")
    .circle(track_radius + track_thickness)
    .circle(track_radius)
    .extrude(track_width)
)

# 2. Define the Tread Lug (Chevron Shape)
# We will create one flat segment and then project/wrap it or create a polar array.
# In CadQuery, creating a custom shape and doing a polar array is efficient.

# Calculate the dimensions of one chevron "V" on a flat plane
# Width of the V-shape arms
arm_thickness = (segment_arc_length - tread_gap) 

def create_chevron_lug():
    # Construct a V-shape sketch
    # Center of the V is at (0,0)
    
    # Calculate points for a V-shape
    # We want the V to point along the direction of travel (tangential) or sideways?
    # In the image, the V points along the circumference.
    
    # Let's build a single lug solid in isolation, oriented correctly, then move it.
    
    # Create a V-shape profile on the surface of the belt
    # We'll make a sketch on the XZ plane (where Y is up/radial)
    
    s = cq.Sketch()
    
    # Outer bound of the segment
    half_w = track_width / 2.0
    half_l = segment_arc_length / 2.0 * 0.85 # Slight gap between segments
    
    # Points for a simple V-chevron
    # We'll use a polygon
    
    # The chevron spans the full width
    p1 = (-half_l, -half_w)
    p2 = (0, -half_w)
    p3 = (half_l, 0) # Tip
    p4 = (0, half_w)
    p5 = (-half_l, half_w)
    p6 = (half_l - arm_thickness, half_w)
    p7 = (half_l, 0 + arm_thickness/2) # Inner tip
    p8 = (half_l - arm_thickness, -half_w) # Back to start-ish area logic
    
    # Let's simplify: Just a rectangle rotated 45 degrees, mirrored?
    # Or just draw the polygon explicitly based on the image style.
    # The image shows a chevron made of two angled bars meeting.
    
    bar_w = segment_arc_length * 0.6
    
    # Left Arm
    r1 = cq.Workplane("XY").rect(bar_w, track_width/2 + 2, centered=True).extrude(tread_height)
    r1 = r1.rotate((0,0,0), (0,0,1), 30) # Angled
    r1 = r1.translate((-bar_w/4, -track_width/4, 0))
    
    # Right Arm (Mirror)
    r2 = cq.Workplane("XY").rect(bar_w, track_width/2 + 2, centered=True).extrude(tread_height)
    r2 = r2.rotate((0,0,0), (0,0,1), -30)
    r2 = r2.translate((-bar_w/4, track_width/4, 0))
    
    lug = r1.union(r2)
    
    # Cut off the excess sticking out the sides
    cutter = cq.Workplane("XY").rect(segment_arc_length*3, track_width).extrude(tread_height + 10).translate((0,0,-5))
    lug = lug.intersect(cutter)
    
    return lug

# Create one master lug
master_lug = create_chevron_lug()

# Position the lug on the outer surface
# Current lug is at Z=0. Needs to be at Radius + Thickness
outer_radius_center = track_radius + track_thickness
master_lug = master_lug.translate((0, 0, outer_radius_center))

# 3. Define the Inner Guide Teeth
# The image shows teeth on the inner rim, near the edges, aligned with the tread segments.
def create_inner_teeth():
    # A simple block
    tooth = (
        cq.Workplane("XY")
        .rect(side_lug_length, side_lug_width)
        .extrude(side_lug_height)
    )
    
    # Position two teeth: Left and Right
    # Distance from center
    offset_y = track_width/2.0 - side_lug_width/2.0
    
    t1 = tooth.translate((0, -offset_y, track_radius - side_lug_height))
    t2 = tooth.translate((0, offset_y, track_radius - side_lug_height))
    
    return t1.union(t2)

master_inner = create_inner_teeth()

# 4. Patterning around the Cylinder
# CadQuery doesn't have a "wrap" function for complex solids, 
# so we rotate and place instances.

def polar_array_solid(solid_to_pattern, count, axis_vector):
    # This function creates a union of rotated copies
    accumulated = cq.Workplane()
    angle_step = 360.0 / count
    
    # Since unioning 36 separate solids can be slow or brittle if they touch perfectly,
    # we usually iterate.
    
    # For speed in this script, we'll build a list of objects and union them efficiently if possible,
    # or just loop.
    
    # Note: solid_to_pattern is a Workplane object.
    base_solid = solid_to_pattern.val()
    
    rotated_solids = []
    for i in range(count):
        # Rotation around X axis (since our cylinder runs along Z in standard extrude, 
        # but here we extruded in Z, so the cylinder axis is Z. Wait.
        # "base_belt" was circle extruded.
        # circle plane "XY" -> extrude direction Z.
        # So the belt is a tube along the Z axis.
        # We need to rotate around Z.
        
        # However, our lug was built on XY plane.
        # To sit on the side of a Z-axis cylinder, we need to rotate it so it faces outward radially.
        # Currently master_lug is flat on XY, translated up Z. This puts it on the "Cap" of a cylinder, not the side.
        pass

    return

# RE-ORIENTATION STRATEGY
# Let's orient the base belt differently to match standard "Wheel" orientation usually expected (Axle along Y or X).
# Or stick to Z axis axle.
# If Axle is Z:
# The belt is a tube centered on (0,0,0) with length along Z.
# The tread needs to be on the cylindrical face.
# Our `create_chevron_lug` made a shape flat on XY.
# To put this on the side of a cylinder along Z, we need to:
# 1. Rotate the lug 90 deg around X (so it stands up).
# 2. Translate it along Y to the radius.
# 3. Rotate around Z for the array.

# Re-building geometry with Cylinder Axis = Z

# Base Belt (Tube along Z)
# Shifted so Z goes from -width/2 to +width/2
base_belt = (
    cq.Workplane("XY")
    .circle(track_radius + track_thickness)
    .circle(track_radius)
    .extrude(track_width)
    .translate((0, 0, -track_width/2))
)

# Re-define Lug for Side Surface
# We build it flat on XZ plane, then project out Y.
def create_side_lug():
    # Width is along Z now. Length along X.
    
    bar_w = segment_arc_length * 0.7
    bar_th = segment_arc_length * 0.25
    
    # Draw V shape on XZ plane
    s = cq.Workplane("XZ")
    
    # Create the V-shape using two rectangles
    # Leg 1
    r1 = s.rect(bar_w, bar_th).extrude(tread_height)
    # Rotate 45 deg around Y axis? No, around the normal (Y)
    r1 = r1.rotate((0,0,0), (0,1,0), -35)
    r1 = r1.translate((-bar_w/5, 0, track_width/4))
    
    # Leg 2
    r2 = s.rect(bar_w, bar_th).extrude(tread_height)
    r2 = r2.rotate((0,0,0), (0,1,0), 35)
    r2 = r2.translate((-bar_w/5, 0, -track_width/4))
    
    lug = r1.union(r2)
    
    # Trim to width
    box = cq.Workplane("XZ").rect(segment_arc_length*2, track_width).extrude(tread_height*2).translate((0,0,-tread_height))
    lug = lug.intersect(box)
    
    return lug

lug_unit = create_side_lug()
# Move to radius
# Currently centered at (0,0,0), extruded in Y (positive).
# Move Y to outer surface.
lug_unit = lug_unit.translate((0, track_radius + track_thickness, 0))

# Inner Teeth
# Build on XZ plane, extrude Y (negative/inwards)
def create_side_inner_teeth():
    s = cq.Workplane("XZ")
    
    # Left Tooth
    t1 = s.rect(side_lug_length, side_lug_width).extrude(side_lug_height) # Extrudes in +Y
    t1 = t1.translate((0, 0, track_width/2 - side_lug_width/2))
    
    # Right Tooth
    t2 = s.rect(side_lug_length, side_lug_width).extrude(side_lug_height)
    t2 = t2.translate((0, 0, -track_width/2 + side_lug_width/2))
    
    teeth = t1.union(t2)
    
    # Since extrude was +Y, and we want it inside the ring pointing inward:
    # We need to move it to inner radius, then rotate 180 or extrude negative?
    # Let's rotate 180 around X to point -Y
    teeth = teeth.rotate((0,0,0), (1,0,0), 180)
    # Move to inner radius
    teeth = teeth.translate((0, track_radius, 0))
    
    return teeth

inner_unit = create_side_inner_teeth()

# Combine one full segment
segment_unit = lug_unit.union(inner_unit)

# --- Perform Polar Array ---
# We manually loop and unite because we are dealing with complex solids
# not just simple features on a single workplane.

final_tracks = cq.Workplane("XY") # Empty container

# Efficient way: Place all, then union all at once
segments = []
for i in range(num_segments):
    angle = i * (360.0 / num_segments)
    # Rotate around Z axis
    rot_segment = segment_unit.rotate((0,0,0), (0,0,1), angle)
    segments.append(rot_segment)

# Union everything
# Start with base belt
result = base_belt
for seg in segments:
    result = result.union(seg)

# Optional: Fillets can be expensive on this many edges, skipping for robustness/speed unless requested.