import cadquery as cq
import math

# Parameters for the circular sector geometry
radius = 20.0
height = 15.0
angle_degrees = 90.0

# Helper calculations for the arc
# Convert angle to radians
angle_rad = math.radians(angle_degrees)
mid_angle_rad = angle_rad / 2.0

# Calculate the end point of the arc
end_x = radius * math.cos(angle_rad)
end_y = radius * math.sin(angle_rad)

# Calculate a mid-point for the arc (required for threePointArc)
mid_x = radius * math.cos(mid_angle_rad)
mid_y = radius * math.sin(mid_angle_rad)

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .lineTo(radius, 0)                              # Draw straight line for the first radius
    .threePointArc((mid_x, mid_y), (end_x, end_y))  # Draw the outer curved edge
    .close()                                        # Close the profile back to origin (0,0)
    .extrude(height)                                # Extrude the 2D profile to create the solid
)