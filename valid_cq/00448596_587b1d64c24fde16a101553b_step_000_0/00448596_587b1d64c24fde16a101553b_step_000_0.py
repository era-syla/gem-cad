import cadquery as cq
import math

# --- Parameters ---
band_width = 24.0
band_thickness = 4.5
outer_radius = 65.0
inner_radius = outer_radius - band_thickness
angle_start = 180.0     # Hinge end (horizontal left)
angle_end = 80.0        # Top end
hinge_length = 20.0     # Length of the thinned hinge section
hinge_thickness = 2.5   # Thickness of the forked section
fork_gap = 10.0         # Width of the slot
eyelet_radius = 3.5     # Outer radius of hinge boss
pin_radius = 1.6        # Inner hole radius

# --- Helper Function ---
def make_arc_profile(workplane, r_in, r_out, start_deg, end_deg):
    """
    Creates a closed 2D profile of an arc segment defined by 
    inner/outer radii and start/end angles.
    """
    # Convert angles to radians
    rad_start = math.radians(start_deg)
    rad_end = math.radians(end_deg)
    
    # Calculate endpoints
    p_start_in = (r_in * math.cos(rad_start), r_in * math.sin(rad_start))
    p_start_out = (r_out * math.cos(rad_start), r_out * math.sin(rad_start))
    p_end_in = (r_in * math.cos(rad_end), r_in * math.sin(rad_end))
    p_end_out = (r_out * math.cos(rad_end), r_out * math.sin(rad_end))
    
    # Calculate midpoints for 3-point arc construction
    rad_mid = (rad_start + rad_end) / 2
    p_mid_in = (r_in * math.cos(rad_mid), r_in * math.sin(rad_mid))
    p_mid_out = (r_out * math.cos(rad_mid), r_out * math.sin(rad_mid))
    
    # Draw the profile
    return (workplane
            .moveTo(*p_start_in)
            .lineTo(*p_start_out)
            .threePointArc(p_mid_out, p_end_out)
            .lineTo(*p_end_in)
            .threePointArc(p_mid_in, p_start_in)
            .close())

# --- Model Construction ---

# 1. Create the Main Band Body
# Extrude the full arc profile symmetrically
base_band = (make_arc_profile(cq.Workplane("XZ"), inner_radius, outer_radius, angle_start, angle_end)
             .extrude(band_width / 2.0, both=True))

# 2. Hinge Step-Down Feature
# Calculate the angle span for the hinge length
hinge_angle_span = math.degrees(hinge_length / outer_radius)
step_start_angle = angle_start + 2.0  # Overshoot slightly for a clean end cut
step_end_angle = angle_start - hinge_angle_span

# Define dimensions for the cutter to thin the band
cut_radius_inner = inner_radius + hinge_thickness
cut_radius_outer = outer_radius + 5.0 # Ensure it clears the outside

# Create the cutter solid
step_cutter = (make_arc_profile(cq.Workplane("XZ"), cut_radius_inner, cut_radius_outer, step_start_angle, step_end_angle)
               .extrude(band_width, both=True))

# Apply the cut to create the thinned section
result = base_band.cut(step_cutter)

# 3. Add Hinge Eyelets
# Position: At the tip of the band (angle_start = 180 deg)
# Coordinate calculation: Tip is at (-R, 0). 
# Center the cylinder on the thinned profile tip.
eyelet_x = -(inner_radius + hinge_thickness/2.0)
eyelet_z = 0.0

eyelet_solid = (cq.Workplane("XZ")
                .center(eyelet_x, eyelet_z)
                .circle(eyelet_radius)
                .extrude(band_width / 2.0, both=True))

result = result.union(eyelet_solid)

# 4. Create the Fork Slot
# Cut a rectangular slot from the tip inwards
# Using a Box centered roughly at the tip to cut through band and eyelet
slot_cutter = (cq.Workplane("XY")
               .center(-outer_radius, 0)
               .box(outer_radius, fork_gap, 50.0)) # (Length, Width, Height)

result = result.cut(slot_cutter)

# 5. Drill Pin Holes
pin_hole_cutter = (cq.Workplane("XZ")
                   .center(eyelet_x, eyelet_z)
                   .circle(pin_radius)
                   .extrude(band_width, both=True))

result = result.cut(pin_hole_cutter)

# 6. Final Fillets
# Add fillets to the long outer edges of the band for smoothness
try:
    # Select edges on the outer circumference (largest radius)
    result = result.edges(cq.selectors.RadiusNthSelector(0)).fillet(1.0)
    
    # Add a small fillet to the transition step edge
    # The step edge is along Y, located roughly at x = -60 (calculated via angle)
    # Using a geometric selector to find the transition edge
    result = result.edges("|Y").filter_by(lambda e: e.Center().x < -40 and e.Center().x > -64 and e.Center().z > 0).fillet(1.5)
except Exception:
    pass # Skip fillets if selection fails due to version differences