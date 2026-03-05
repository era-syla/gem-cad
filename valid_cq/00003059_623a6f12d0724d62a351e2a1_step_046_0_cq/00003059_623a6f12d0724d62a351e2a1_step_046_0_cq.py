import cadquery as cq
import math

# --- Parameters ---
num_teeth = 13          # Number of teeth
thickness = 5.0         # Thickness of the sprocket plate
bore_diameter = 20.0    # Diameter of the central hole
pitch = 12.7            # Chain pitch (e.g., standard ANSI #40 or ISO 08B is 12.7mm or 1/2")
roller_diameter = 7.95  # Roller diameter (standard for 1/2" pitch)

# Calculated parameters based on standard sprocket geometry approximation
# Pitch Circle Diameter (PCD)
pcd = pitch / math.sin(math.pi / num_teeth)

# Tip Diameter (approximate outer diameter)
# Standard formula often adds about 0.6 to 1.0 times pitch to PCD, or follows specific tooth profiles
# Here we use a simplified geometric construction for the tooth profile.
outer_radius = (pcd / 2) + (pitch * 0.4) 
root_radius = (pcd / 2) - (roller_diameter / 2) - 0.5 # Slightly deeper for clearance

# Tooth profile parameters
tooth_width_angle = 360 / num_teeth
half_tooth_angle = tooth_width_angle / 2

# Create the main sprocket body
# We will define one tooth profile and polar array it.

# Helper function to create a single tooth cutout profile
def create_tooth_cutout():
    # The "gap" between teeth is where the roller sits.
    # We will model the negative space (the gap) and cut it from a solid disk.
    
    # Radius of the gap curvature (approx roller radius + clearance)
    gap_radius = roller_diameter / 2 * 1.05
    
    # Distance from center to the gap center
    gap_center_dist = pcd / 2
    
    # We create a shape representing the space between teeth
    # This is roughly circular at the bottom (root) and flares out
    
    # Using a simple circle for the root gullet
    gullet = (
        cq.Workplane("XY")
        .moveTo(gap_center_dist, 0)
        .circle(gap_radius)
    )
    
    # Creating the angular cutout sides to form the tooth tip shape
    # This is a bit of an approximation to an involute or standard sprocket curve
    # but sufficient for a visual match.
    
    # We cut a wedge shape to separate the teeth
    # Actually, it's easier to make the full disk and cut the "gullets" out.
    return gullet

# 1. Start with the outer disk
disk = cq.Workplane("XY").circle(outer_radius).extrude(thickness)

# 2. Create the cutter for the tooth gaps (gullets)
# The gullet is primarily the roller seating area.
# We also need to trim the tips so they aren't perfectly sharp circular segments.

# Let's try a different approach: Sketch the 2D profile of the entire gear.
def sprocket_profile(num_teeth, pcd, roller_dia):
    # Angle between teeth
    angle_step = 2 * math.pi / num_teeth
    
    points = []
    
    # We will generate points for a spline or polyline
    # A simplified sprocket tooth profile consists of:
    # 1. Root radius arc (where roller sits)
    # 2. Tooth flank
    # 3. Tooth tip
    
    # Roller radius
    rr = roller_dia / 2
    # Pitch radius
    pr = pcd / 2
    
    # Generate the full profile
    # Using a high-level construction: Make a large disk, cut the roller seats
    
    s = cq.Workplane("XY").circle(outer_radius)
    
    for i in range(num_teeth):
        angle = i * 360.0 / num_teeth
        # Position of the roller center
        x = pr * math.cos(math.radians(angle))
        y = pr * math.sin(math.radians(angle))
        
        # Cut the roller seat
        # We need to make the opening slightly wider than just a circle to allow the roller to enter/exit
        # but for a static model, a circular cut at the pitch line is the primary feature.
        # To make it look like a real sprocket, the cut needs to flare out.
        
        # Define a cutting tool for one tooth gap
        # Local coordinates for the cutter
        cutter = (
            cq.Workplane("XY")
            .moveTo(x, y)
            .circle(rr * 1.05) # Roller seat with slight clearance
        )
        s = s.cut(cutter.extrude(thickness))
        
        # To refine the tooth shape (make the sides less "sharp" and more tapered), 
        # we can cut with a shape that represents the path of the roller exiting.
        # However, a simple circular cut at the pitch circle diameter creates a very reasonable sprocket approximation 
        # often used in simplified CAD.
        # The image shows teeth that are rounded at the tips. The "outer_radius" circle defines the tip.
        # The circular cuts define the gullets. The intersection creates the sharp points.
        # To round the tips, we can fillet the resulting edges or reduce the outer diameter relative to the cuts.
        
    return s

# Let's use the Constructive Solid Geometry (CSG) approach which is robust in CadQuery
# 1. Base Cylinder
base = cq.Workplane("XY").circle(outer_radius).extrude(thickness)

# 2. Create the "Negative" roller shape
# The shape that cuts the gap. 
# It's a circle at the root, potentially widening outwards.
# For standard sprockets, the tooth gap is the inverse of the roller path.
# We will use a simple circle at the pitch diameter which creates a basic functional sprocket shape.
gap_cutter = (
    cq.Workplane("XY")
    .workplane(offset=-thickness/2) # Start slightly below to ensure full cut
    .moveTo(pcd/2, 0)
    .circle(roller_diameter/2)
    .extrude(thickness * 2)
)

# 3. Array the cutter
# We rotate this cutter around the Z axis
cutters = gap_cutter
for i in range(1, num_teeth):
    cutters = cutters.union(gap_cutter.rotate((0,0,0), (0,0,1), i * (360.0/num_teeth)))

# 4. Cut the gaps from the base
sprocket = base.cut(cutters)

# 5. Create the central bore
result = sprocket.faces(">Z").workplane().hole(bore_diameter)

# Optional: Add small chamfers to the teeth edges (simulating the image's rounded look)
# This can be computationally expensive on complex curves, so we often skip it for simple generated models,
# or apply it selectively. The image shows a very slight chamfer/fillet on the edges.
try:
    result = result.faces("|Z").edges().fillet(0.5)
except:
    # Fallback if geometry is too complex for simple fillet
    pass

# The variable 'result' contains the final geometry
show_object(result) if 'show_object' in locals() else None