import cadquery as cq
import math

# --- Parameters ---
# Base dimensions
base_width = 50.0
base_length = 50.0
base_thickness = 5.0

# Tube dimensions
tube_outer_radius = 12.0
tube_inner_radius = 10.0
tube_height = 50.0

# Coil (Helix) dimensions
coil_wire_radius = 2.0
coil_pitch = 8.0  # Distance between turns
coil_turns = (tube_height / coil_pitch)  # Calculate turns to cover height
coil_radius = tube_outer_radius + (coil_wire_radius * 0.8) # Slight overlap for robust union

# --- Modeling ---

# 1. Create the base plate
base = cq.Workplane("XY").box(base_width, base_length, base_thickness)

# 2. Create the central hollow tube
# We start the tube from the top of the base
tube = (cq.Workplane("XY")
        .workplane(offset=base_thickness / 2) # Start on top of the base
        .circle(tube_outer_radius)
        .circle(tube_inner_radius)
        .extrude(tube_height)
        )

# 3. Create the Helix (Coil)
# We need to define a path for the sweep.
# CadQuery's helix creation often involves parametric curves or the helper function.

def helix(r, h, p):
    """
    Creates a helical wire.
    r: radius
    h: height
    p: pitch
    """
    # Calculate number of turns
    turns = h / p
    
    # Create the helix path
    path = cq.Workplane("XY").parametricCurve(
        lambda t: (
            r * math.cos(t * turns * 2 * math.pi),
            r * math.sin(t * turns * 2 * math.pi),
            t * h
        )
    )
    return path

# Generate the helical path starting just above the base
helix_path = (helix(coil_radius, tube_height, coil_pitch)
              .translate((0, 0, base_thickness / 2)) # Move to start on top of base
             )

# Create the profile for the sweep (circular wire cross-section)
# We need to orient a plane perpendicular to the start of the helix path.
# The parametric curve starts at angle 0 (X-axis) at Z=0 (relative to the path start).
# So the normal to the path at start is the Y-axis (tangent).
# The profile should be on the XZ plane relative to the path start.

coil = (cq.Workplane("XZ") # Plane perpendicular to the start of the helix
        .workplane(offset=coil_radius) # Offset to the radius of the helix
        .circle(coil_wire_radius) # Draw the wire cross-section
        .sweep(helix_path, isFrenet=True) # Sweep along the path
       )

# 4. Combine all parts
# Union the base, the tube, and the coil.
result = base.union(tube).union(coil)

# If running in an environment that visualizes 'result' automatically (like CQ-editor)
# show_object(result)