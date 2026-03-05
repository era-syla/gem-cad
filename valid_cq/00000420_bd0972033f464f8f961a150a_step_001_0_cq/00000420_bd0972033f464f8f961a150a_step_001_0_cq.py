import cadquery as cq

def create_intersecting_cylinders():
    # Parameters for the dimensions
    cylinder_radius = 50.0
    cylinder_height = 120.0  # Needs to be large enough to fully intersect

    # Create the first cylinder along the Z axis
    cyl_z = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height, both=True)

    # Create the second cylinder along the X axis
    # Rotate the workplane to YZ so the extrusion is along X
    cyl_x = cq.Workplane("YZ").circle(cylinder_radius).extrude(cylinder_height, both=True)

    # Create the third cylinder along the Y axis
    # Rotate the workplane to XZ so the extrusion is along Y
    cyl_y = cq.Workplane("XZ").circle(cylinder_radius).extrude(cylinder_height, both=True)

    # Calculate the intersection of the three cylinders
    # This shape is known as a Steinmetz solid (specifically a tricylinder)
    result = cyl_z.intersect(cyl_x).intersect(cyl_y)

    return result

# Generate the model
result = create_intersecting_cylinders()