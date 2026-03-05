import cadquery as cq
import math

# ==========================================
# Parameters
# ==========================================
hub_diameter = 12.0
hub_height = 9.0
shaft_diameter = 3.0
prop_diameter = 130.0
prop_radius = prop_diameter / 2.0

# Define blade stations: radius (x-dist), chord (width), thickness, twist angle
# Radius starts small to bury the root inside the hub for a clean union
stations = [
    # Inside Hub
    {"r": 3.0,  "c": 8.0,  "t": 4.5, "ang": 45.0}, 
    # Root Transition
    {"r": 12.0, "c": 14.0, "t": 3.0, "ang": 30.0},
    # Mid-Span (Widest)
    {"r": 30.0, "c": 16.0, "t": 2.2, "ang": 22.0},
    # Outer Span
    {"r": 45.0, "c": 13.0, "t": 1.6, "ang": 16.0},
    # Tapering
    {"r": 60.0, "c": 8.0,  "t": 1.0, "ang": 12.0},
    # Tip
    {"r": prop_radius, "c": 0.5, "t": 0.2, "ang": 10.0}
]

# ==========================================
# Helper Function: Generate Airfoil Wire
# ==========================================
def make_airfoil(radius, chord, thickness, angle):
    """
    Creates a closed spline wire on the YZ plane at a specific X offset (radius).
    The shape is rotated by 'angle' to simulate pitch.
    """
    # Create a workplane located at x=radius
    wp = cq.Workplane("YZ").workplane(offset=radius)
    
    # Define localized points for the airfoil cross-section (before rotation)
    # We center the Leading Edge/Aerodynamic center roughly at (0,0)
    # y coordinates correspond to chordwise position, z to thickness
    
    y_le = -chord * 0.3  # Leading edge Y
    y_te = chord * 0.7   # Trailing edge Y
    
    # Points: Leading Edge, Top Curve, Trailing Edge, Bottom Curve
    # Using 5 points to define the loop for the spline
    pts_raw = [
        (y_le, 0.0),                            # LE
        (y_le + chord*0.35, thickness/2.0),     # Top Max
        (y_te, 0.0),                            # TE
        (y_le + chord*0.35, -thickness*0.3)     # Bottom Max (flatter bottom)
    ]
    
    # Rotate points around (0,0) by the pitch angle
    rad = math.radians(angle)
    c = math.cos(rad)
    s = math.sin(rad)
    
    pts_rotated = []
    for y, z in pts_raw:
        # Standard 2D rotation formula
        yr = y * c - z * s
        zr = y * s + z * c
        pts_rotated.append((yr, zr))
        
    # Create the closed spline wire
    return wp.spline(pts_rotated, includeCurrent=False).close()

# ==========================================
# Main Geometry Construction
# ==========================================

# 1. Create the Hub
hub = (cq.Workplane("XY")
       .circle(hub_diameter / 2.0)
       .extrude(hub_height)
       .translate((0, 0, -hub_height / 2.0))) # Center vertically on Z=0

# 2. Create the first blade
# Generate wires for each station
blade_wires = []
for s in stations:
    w = make_airfoil(s["r"], s["c"], s["t"], s["ang"])
    blade_wires.append(w)

# Loft the wires to create the solid blade
# We start a new stack, add all wires, and loft
blade1 = cq.Workplane("YZ")
for w in blade_wires:
    blade1 = blade1.add(w)

blade1 = blade1.toPending().loft()

# 3. Create the second blade
# Rotate the first blade 180 degrees around Z axis
blade2 = blade1.rotate((0, 0, 0), (0, 0, 1), 180)

# 4. Union Hub and Blades
propeller = hub.union(blade1).union(blade2)

# 5. Cut the Shaft Hole
result = (propeller
          .faces(">Z")
          .workplane()
          .circle(shaft_diameter / 2.0)
          .cutThruAll())

# 6. Add a small fillet to the hub top edge for clean look (optional but good)
try:
    result = result.edges(cq.selectors.RadiusNthSelector(0)).fillet(0.5)
except:
    pass # Skip if fillet fails due to geometry complexity