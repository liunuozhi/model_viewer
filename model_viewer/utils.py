import bpy
from mathutils import Vector


def scale_to_unit_cube(obj):
    # Get the object's bounding box corners in world space
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    # Calculate the bounding box dimensions
    min_x = min(corner.x for corner in bbox_corners)
    max_x = max(corner.x for corner in bbox_corners)
    min_y = min(corner.y for corner in bbox_corners)
    max_y = max(corner.y for corner in bbox_corners)
    min_z = min(corner.z for corner in bbox_corners)
    max_z = max(corner.z for corner in bbox_corners)
    
    width = max_x - min_x
    height = max_y - min_y
    depth = max_z - min_z
    
    # Calculate scale factors to make the object a unit cube
    scale_x = 1.0 / width if width != 0 else 1.0
    scale_y = 1.0 / height if height != 0 else 1.0
    scale_z = 1.0 / depth if depth != 0 else 1.0
    
    scale_factor = min(scale_x, scale_y, scale_z)
    
    # Apply scaling to the object
    obj.scale *= scale_factor
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.location = (0, 0, 0)
    

def move_object_to_center(obj):
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    bbox_center = sum((Vector(corner) for corner in bbox_corners), Vector()) / 8
    translation_vector = -bbox_center
    obj.location += translation_vector
