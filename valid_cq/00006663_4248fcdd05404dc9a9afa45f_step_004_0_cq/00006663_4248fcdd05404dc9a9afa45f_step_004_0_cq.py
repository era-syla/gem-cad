import cadquery as cq

# Parametric dimensions
lower_diameter = 10.0
lower_height = 25.0
upper_diameter = 5.0
upper_height = 30.0
tip_angle_degrees = 45.0  # Angle of the chamfer/cone at the top
tip_height = 2.0 # Height of the conical tip section
transition_chamfer = 1.0 # The chamfer between the two main cylinders

# 1. Create the lower cylinder base
lower_cylinder = cq.Workplane("XY").circle(lower_diameter / 2).extrude(lower_height)

# 2. Create the upper cylinder
# We select the top face of the lower cylinder to start the next extrusion
upper_cylinder = (
    lower_cylinder.faces(">Z")
    .workplane()
    .circle(upper_diameter / 2)
    .extrude(upper_height)
)

# 3. Create the transition between the two cylinders
# A standard approach for this visual "step" is often a chamfer or fillet
# looking at the image, there is a distinct angled transition.
# We will select the edge at the bottom of the upper cylinder where it meets the lower one.
# Since we just extruded, the "bottom" of the new extrusion is at z=lower_height.
result_with_transition = upper_cylinder.faces(f"<Z[1]").edges().chamfer(transition_chamfer)

# 4. Create the conical tip
# We select the very top face of the model
# The image shows a small conical taper at the very tip, ending in a flat or smaller point.
# A chamfer on the top edge is the most efficient way to achieve this.
result = result_with_transition.faces(">Z").edges().chamfer(tip_height)

# Alternatively, if a specific point or flat top dimension is required, a loft or revolution could be used,
# but a chamfer on the cylinder end creates exactly the geometry shown (a frustum).

if __name__ == "__main__":
    try:
        from cadquery import exporters
        # Optional: export to STL for verification
        # exporters.export(result, "pin_model.stl")
        pass
    except ImportError:
        pass