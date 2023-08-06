from typing import cast

from pyaedt.hfss import Hfss
from pyaedt.modeler.cad.object3d import Object3d
from pyaedt.modeler.modeler3d import Modeler3D


def delete_model(hfss: Hfss):
    """nuke everything"""
    modeler = cast(Modeler3D, hfss.modeler)

    for obj in modeler.object_list:
        if obj == None:
            break
        obj = cast(Object3d, obj)
        if obj.name != "RadiatingSurface":
            obj.delete()
    modeler.delete(modeler.unclassified_objects)
    modeler.cleanup_objects()
