"""Generating report."""

# %% Import
import numpy as np
import pandas as pd
from pyaedt.modules.AdvancedPostProcessing import PostProcessor
from typing import cast

from pyaedt.modules.solutions import SolutionData
from antcal.application.hfss import SOLUTIONS


# %% Functions
def get_s_params(
    post: PostProcessor, row: int, col: int, setup_name: str, sweep_name: str
):
    """Fetch S parameters as an array.

    :param pyaedt.modules.AdvancedPostProcessing.PostProcessor post: Advanced post processor
    :param int row: Which row of the S matrix
    :param int col: Which column of the S matrix
    :return pd.DataFrame: S parameters in dB
    """

    match post.post_solution_type:
        case SOLUTIONS.Hfss.DrivenModal:
            category = "Modal Solution Data"
        case SOLUTIONS.Hfss.DrivenTerminal:
            category = "Terminal Solution Data"
        case _:
            category = "Modal Solution Data"

    solution_data = post.get_solution_data(
        expressions=f"S({row},{col})",
        setup_sweep_name=f"{setup_name} : {sweep_name}",
        domain="Sweep",
        variations={"Freq": ["All"]},
        primary_sweep_variable="Freq",
        report_category=category,
        context=None,
        math_formula="dB",
    )
    solution_data = cast(SolutionData, solution_data)

    return pd.DataFrame(
        {
            "Freq": solution_data.primary_sweep_values,
            f"S{row}{col}": solution_data.data_real(f"dB(S({row},{col}))"),
        }
    )


def get_pattern(
    post: PostProcessor, phi: int, freq: float, setup_name: str, sweep_name: str
):
    """Fetch radiation pattern."""

    solution_data = post.get_solution_data(
        expressions=["GainTheta", "GainPhi"],
        setup_sweep_name=f"{setup_name} : {sweep_name}",
        domain="Sweep",
        variations={"Theta": ["All"], "Phi": [f"{phi}deg"], "Freq": [f"{freq}GHz"]},
        primary_sweep_variable="Theta",
        report_category="Far Fields",
        context="Elevation",
        math_formula="dB",
    )
    solution_data = cast(SolutionData, solution_data)

    return pd.DataFrame(
        {
            "Theta": solution_data.primary_sweep_values,
            "dB(GainTheta)": solution_data.data_real("dB(GainTheta)"),
            "dB(GainPhi)": solution_data.data_real("dB(GainPhi)"),
        }
    )
