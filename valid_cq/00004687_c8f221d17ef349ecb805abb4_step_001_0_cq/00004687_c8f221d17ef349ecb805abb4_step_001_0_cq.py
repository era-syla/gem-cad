import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
base_diameter = 40.0       # Diameter of the bottom flange
base_thickness = 5.0       # Height of the bottom flange
body_diameter = 32.0       # Outer diameter of the main cylindrical section
body_height = 20.0         # Height of the straight cylindrical section
taper_top_diameter = 26.0  # Outer diameter at the very top
taper_height = 10.0        # Height of the tapered section
wall_thickness = 3.0       # Thickness of the wall

# --- Calculations ---
total_height = base_thickness + body_height + taper_height
inner_diameter_straight = body_diameter - (2 * wall_thickness)
# Assuming a constant internal bore or a tapered bore following the outside.
# The image suggests a straight bore or slightly tapered. Let's assume a straight bore for the main part
# but often these parts have a consistent wall thickness.
# Let's model it by revolving a profile to maintain consistent wall thickness if desired, 
# or simpler: create the outer shape and shell it or cut a hole.
# Looking at the top rim, the wall thickness looks constant. A revolution is the most robust way.

# --- Modeling Strategy: Revolution ---
# We will draw half the cross-section on the XZ plane and revolve it around the Z axis.

# Points for the outer profile (starting from bottom-right, moving up-left)
p0 = (body_diameter / 2, 0) # Start inside the flange to keep it simple, actually let's do outer profile then inner
p_outer_1 = (base_diameter / 2, 0)
p_outer_2 = (base_diameter / 2, base_thickness)
p_outer_3 = (body_diameter / 2, base_thickness)
p_outer_4 = (body_diameter / 2, base_thickness + body_height)
p_outer_5 = (taper_top_diameter / 2, total_height)

# Points for the inner profile
# We'll subtract wall_thickness from the x-coordinates of the outer profile components
# corresponding to the main body and taper.
p_inner_1 = (taper_top_diameter / 2 - wall_thickness, total_height)
p_inner_2 = (body_diameter / 2 - wall_thickness, base_thickness + body_height)
p_inner_3 = (body_diameter / 2 - wall_thickness, 0) # Straight bore through the bottom

# Create the workplane and draw the sketch
result = (
    cq.Workplane("XZ")
    .polyline([
        p_inner_3,      # Bottom inner point
        p_outer_1,      # Bottom outer flange edge
        p_outer_2,      # Top of flange edge
        p_outer_3,      # Flange to body transition
        p_outer_4,      # Body to taper transition
        p_outer_5,      # Top outside edge
        p_inner_1,      # Top inside edge
        p_inner_2,      # Inner taper transition (to keep uniform wall thickness approximation)
        p_inner_3       # Close the loop
    ])
    .close()
    .revolve()
)

# Optional: Add a small fillet at the flange-to-body transition as seen in the shading (optional but realistic)
result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(1.0)

# If needed to export:
# cq.exporters.export(result, "bushing.step")