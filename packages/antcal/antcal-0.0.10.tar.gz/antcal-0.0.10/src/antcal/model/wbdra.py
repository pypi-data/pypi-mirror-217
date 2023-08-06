"""Widebeam DRA"""

from typing import cast

import numpy as np
from pyaedt.application.Variables import VariableManager
from pyaedt.desktop import Desktop
from pyaedt.generic.constants import AXIS, PLANE, SOLUTIONS
from pyaedt.generic.general_methods import remove_project_lock
from pyaedt.hfss import Hfss
from pyaedt.modeler.cad.elements3d import Point
from pyaedt.modeler.cad.object3d import Object3d
from pyaedt.modeler.modeler3d import Modeler3D
from pyaedt.modules.AdvancedPostProcessing import PostProcessor
from pyaedt.modules.Material import Material
from pyaedt.modules.MaterialLib import Materials
from pyaedt.modules.solutions import SolutionData
from pyaedt.modules.SolveSetup import SetupHFSS, SetupHFSSAuto


def update_variables(hfss: Hfss, variables: np.ndarray, mapping: list[str]):
    # var_dict: {

    # }
    ...


def update_materials(materials: Materials, CONSTANTS: dict[str, str]):
    if not materials.checkifmaterialexists(CONSTANTS["sub1_mat_name"]):
        materials.add_material(
            CONSTANTS["sub1_mat_name"],
        )
    sub1_mat = materials[CONSTANTS["sub1_mat_name"]]
    sub1_mat = cast(Material, sub1_mat)
    sub1_mat.permittivity = CONSTANTS["sub1_eps_r"]
    sub1_mat.dielectric_loss_tangent = CONSTANTS["sub1_tan_d"]
    sub1_mat.material_appearance = [244, 244, 244]
    sub1_mat.update()

    if not materials.checkifmaterialexists(CONSTANTS["sub2_mat_name"]):
        materials.add_material(CONSTANTS["sub2_mat_name"])
    sub2_mat = materials[CONSTANTS["sub2_mat_name"]]
    sub2_mat = cast(Material, sub2_mat)
    sub2_mat.permittivity = [
        CONSTANTS["sub2_eps_r_xy"],
        CONSTANTS["sub2_eps_r_xy"],
        CONSTANTS["sub2_eps_r_z"],
    ]
    sub2_mat.dielectric_loss_tangent = CONSTANTS["sub2_tan_d"]
    sub2_mat.material_appearance = [210, 233, 255]
    sub2_mat.update()


def remove_all(modeler: Modeler3D):
    for obj in modeler.object_list:
        if obj == None:
            break
        obj = cast(Object3d, obj)
        if obj.name != "RadiatingSurface":
            obj.delete()
    modeler.cleanup_objects()
    modeler.delete(modeler.unclassified_objects)


def build_model(hfss: Hfss, variables: np.ndarray):
    # preparation

    hfss.logger.enable_log_on_file()
    hfss.autosave_enable()
    modeler = cast(Modeler3D, hfss.modeler)
    materials = cast(Materials, hfss.materials)
    post = cast(PostProcessor, hfss.post)
    variables = cast(VariableManager, hfss.variable_manager)
    hfss.set_auto_open()

    # Design variables: Widebeam DRA

    CONSTANTS = {
        "sub1_mat_name": "Rogers RO4350 (tm) 10 mil",
        "sub1_eps_r": "3.88",
        "sub1_tan_d": "0.0037",
        "sub2_mat_name": "Rogers RT/duroid 6010/6010LM (tm) Anisotropic",
        "sub2_eps_r_xy": "13.3",
        "sub2_eps_r_z": "10.6",
        "sub2_tan_d": "0.0023",
    }

    MATERIALS = [CONSTANTS["sub1_mat_name"], CONSTANTS["sub2_mat_name"], "copper"]

    # wavelength in sub 1 is around 7.3 mm
    # wavelength in sub 2 is around 3.8 mm
    CONSTANT_VARIABLES = {
        "f_c": "24.1 GHz",
        "lambda_0": "12.45 mm",
        "lambda_sub1": "7.31mm",
        "lambda_sub2": "3.8 mm",
        "zl_sub1": "0.254 mm",
        "zl_sub2": "1.27 mm",
        "zl_cu": "0.035 mm",
    }

    DEFAULT_VARIABLES = {
        "xl_gnd": "14 mm",
        "yl_gnd": "xl_gnd",
        "xl_dr": "3.9 mm",
        "yl_dr": "xl_dr",
        "w_slot": "0.3 mm",
        "l_slot": "3 mm",
        "l_stub": "0.8 mm",
        "w_feed": "0.5 mm",
    }

    for k, v in (CONSTANT_VARIABLES | DEFAULT_VARIABLES).items():
        variables.set_variable(k, v, overwrite=True)

    for mat_name in MATERIALS:
        materials.checkifmaterialexists(mat_name)

    setup_name = "Auto1"
    sweep_name = "Sweep1"
    freq_start = 20
    freq_end = 28
    step_size = 0.05

    update_materials(materials, CONSTANTS)

    # ground layer
    gnd_name = "gnd"
    gnd = modeler.create_rectangle(
        PLANE.XY,
        ["- xl_gnd / 2", "- yl_gnd / 2", 0],
        ["xl_gnd", "yl_gnd"],
        gnd_name,
        "copper",
    )
    gnd = cast(Object3d, gnd)

    # slot
    slot_name = "slot"
    slot = modeler.create_rectangle(
        PLANE.XY,
        ["- w_slot / 2", "- l_slot / 2", 0],
        ["w_slot", "l_slot"],
        slot_name,
    )
    slot = cast(Object3d, slot)
    gnd.subtract([slot], keep_originals=False)
    modeler.cleanup_objects()

    hfss.assign_perfecte_to_sheets(gnd, f"{gnd_name}")

    # sub1
    sub1_name = "sub1"
    sub1 = modeler.create_box(
        ["- xl_gnd / 2", "- yl_gnd / 2", 0],
        ["xl_gnd", "yl_gnd", "- zl_sub1"],
        f"{sub1_name}",
        CONSTANTS["sub1_mat_name"],
    )
    sub1 = cast(Object3d, sub1)

    dr_name = "dr1"
    dr = (
        modeler.create_box(
            ["- xl_dr / 2", "- yl_dr / 2", 0],
            ["xl_dr", "yl_dr", "zl_sub2"],
            f"{dr_name}",
            CONSTANTS["sub2_mat_name"],
        ),
    )

    feedline_name = "feedline1"
    feedline = modeler.create_rectangle(
        PLANE.XY,
        ["- xl_gnd / 2", "- w_feed / 2", "-zl_sub1"],
        ["xl_gnd / 2 + l_stub", "w_feed"],
        feedline_name,
        "copper",
    )
    feedline = cast(Object3d, feedline)

    hfss.assign_perfecte_to_sheets(feedline, feedline_name)

    hfss.lumped_port(
        feedline,
        gnd,
        True,
        integration_line=hfss.AxisDir.XNeg,
        name="1",
        renormalize=False,
    )

    setup_auto1 = hfss.get_setup(setup_name)
    setup_auto1 = cast(SetupHFSS, setup_auto1)
    setup_auto1.enable_adaptive_setup_single(CONSTANT_VARIABLES["f_c"], 15, 0.05)
    setup_auto1.update(
        {
            "MinimumConvergedPasses": 2,
            "PercentRefinement": 50,
            "BasisOrder": -1,
            "DrivenSolverType": "Auto Select Direct/Iterative",
        }
    )
    if not sweep_name in hfss.get_sweeps(setup_name):
        setup_auto1.create_linear_step_sweep(
            "GHz", freq_start, freq_end, step_size, sweep_name, sweep_type="Fast"
        )

    assert hfss.validate_full_design()[1]
