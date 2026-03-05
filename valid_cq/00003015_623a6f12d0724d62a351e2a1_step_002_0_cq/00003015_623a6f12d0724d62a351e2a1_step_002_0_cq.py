import cadquery as cq

# -- Parameters --
outer_diameter = 100.0   # Main diameter of the disk
thickness = 10.0         # Total thickness of the disk
hole_diameter = 10.0     # Diameter of the center hole
groove_depth = 2.0       # Depth of the V-groove on the edge
groove_width = 8.0       # Width of the V-groove at the outer surface

# -- Modeling --

# 1. Create the main disk cylinder
disk = cq.Workplane("XY").circle(outer_diameter / 2).extrude(thickness)

# 2. Cut the center hole
disk = disk.faces(">Z").workplane().hole(hole_diameter)

# 3. Create the groove profile to revolve-cut around the edge
# The profile is a triangle (or similar shape) positioned at the edge
# We will draw this on a plane perpendicular to the disk (e.g., XZ plane)
# Coordinate system: X is radial, Z is axial (thickness direction)

# Calculate points for the groove cutter
# The groove is centered on the thickness (Z-axis in the sketch plane, relative to disk center)
radius = outer_diameter / 2
z_center = thickness / 2

# We need a custom workplane to sketch the groove profile on the side
# We'll use the XZ plane, offset so the sketch is easy to place
groove_cutter = (
    cq.Workplane("XZ")
    .workplane(offset=0) # Working on the default XZ plane
    .moveTo(radius, z_center) # Move to the edge of the disk, middle of thickness
    .polyline([
        (radius, z_center - groove_width / 2),  # Bottom edge of groove opening
        (radius - groove_depth, z_center),      # Tip of the V
        (radius, z_center + groove_width / 2),  # Top edge of groove opening
        (radius, z_center - groove_width / 2)   # Close the loop
    ])
    .close()
    .revolve(360, (0, 0, 0), (0, 0, 1)) # Revolve around Z axis
)

# 4. Subtract the groove from the main disk
# Since revolve creates a solid, we can use cut.
# However, a cleaner way in CadQuery is often to revolve a cut directly if possible,
# but constructing a "cutter" solid and boolean subtracting is very robust.
result = disk.cut(groove_cutter)

# Alternatively, a more direct revolve-cut approach on a cross-section:
# Construct the full cross-section and revolve it.
# Let's try the cross-section revolve method as it's often cleaner for pulleys.

# -- Alternative Method (Revolve Profile) --
# This method defines the cross-section of the pulley wall and revolves it.

# Define points for the cross-section on the XZ plane (X=radius, Y=axial)
# We draw the right half of the cross-section.
pts = [
    (hole_diameter / 2, 0),                       # Bottom-inner corner
    (outer_diameter / 2, 0),                      # Bottom-outer corner
    (outer_diameter / 2, (thickness - groove_width)/2), # Start of groove
    (outer_diameter / 2 - groove_depth, thickness / 2), # Bottom of groove
    (outer_diameter / 2, thickness - (thickness - groove_width)/2), # End of groove
    (outer_diameter / 2, thickness),              # Top-outer corner
    (hole_diameter / 2, thickness),               # Top-inner corner
    (hole_diameter / 2, 0)                        # Close loop
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0)) # Revolve around Z-axis (which is Y in this 2D sketch plane logic)
    # Note: In "XZ" workplane: x_dir is global X, y_dir is global Z.
    # So (0,0) is origin. Revolve axis is the vertical axis of the sketch, which is global Z.
    # The axis start/end arguments for revolve are in local coordinates. 
    # Local (0,0) to (0,1) is the Z axis.
)

# Final Result
# The 'result' variable contains the generated shape
if __name__ == "__main__":
    # If running in an environment that supports show_object (like CQ-Editor), display it
    try:
        show_object(result)
    except NameError:
        pass