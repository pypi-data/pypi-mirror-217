"""Module for converting input figure into Econoplots style."""
# %% Imports

# Standard Library Imports

# Third Party Imports
from matplotlib import pyplot as plt  # noqa
from matplotlib.axes import Axes

# Econoplots Imports
from econoplots.params import setRCParams
from econoplots.utils import (
    PutBarsInFront,
    addOuterMinorTicks,
    configDepdendentXAxis,
    configDependentYAxis,
    configIndependentXAxis,
    configIndependentYAxis,
    loadColorMap,
    makePatchSpinesInvisible,
    nudgeBottomSpine,
    plotZeroPt,
    replaceAxesMinusGlyphs,
    setBoxColor,
    setDefaultLineColors,
    setDefaultPatchColors,
    setLegendParams,
    setLineColor,
    setMajorGrids,
    updateLegendEntryColors,
)

# %% Load color map and set parameters
setRCParams()

# with open("econoplots/color_map.json") as json_file:
#     color_map = json.load(json_file)

# %% Functions


def convert2Econo(
    ax: Axes,
    ax_type: str = "line",
    **kwargs,
) -> Axes:
    """Formats a Matplotlib Axes as a pseudo-Economist figure.

    Args:
        ax (Axes): A Matplotlib object.
        ax_type (str, optional): ["line" | "fill" | "bar" | "hbox"] What type of
            plot is contained in ax. Defaults to "line".

    Returns:
        Axes: A Matplotlib object.
    """
    assert isinstance(ax, Axes)
    assert ax_type in [
        "line",
        "fill",
        "bar",
        "hbox",
    ], "ax_type not in recognized list."

    converter_map = {
        "line": convertLine,
        "hbox": convertHBox,
        "bar": convertBar,
        "fill": convertLineFill,
    }

    # color_map = loadColorMap()
    ax = converter_map[ax_type](ax, **kwargs)

    return ax


def convertLine(
    ax: Axes,
    zero_dot: bool = False,
) -> Axes:
    # Set general lie plot defaults
    ax = setLineDefaults(ax)

    # Change line colors
    setDefaultLineColors(ax)

    ax = updateLegendEntryColors(ax)

    if zero_dot is True:
        ax = plotZeroPt(ax, marker_size=10)

    return ax


def setLineDefaults(ax: Axes) -> Axes:
    # Change axis color
    setMajorGrids(ax, axis="y")

    # set axis params
    # y_offset_text = ax.yaxis.get_offset_text().get_text()
    # x_offset_text = ax.xaxis.get_offset_text().get_text()
    replaceAxesMinusGlyphs(ax)
    configDependentYAxis(ax, side="right", label_location="right")

    # Move bottom spine before setting xAxis params to avoid Xticks being regenerated
    nudgeBottomSpine(ax)
    configIndependentXAxis(ax, pad_side="right", minor_ticks_on=True)

    # Add minor tick(s) if outer limits of data are NOT on major ticks. Unlike
    # minor ticks that are in-between major ticks, the outer minor ticks are not
    # optional.
    addOuterMinorTicks(ax)

    # delete top, right, left spines
    makePatchSpinesInvisible(ax, ["top", "right", "left"])

    # Set legend background
    setLegendParams(ax)

    return ax


def convertLineFill(ax: Axes) -> Axes:
    # Set general lie plot defaults
    ax = setLineDefaults(ax)

    ax = setDefaultPatchColors(ax)

    ax = updateLegendEntryColors(ax)

    return ax


def convertBar(ax: Axes, orientation: str = "vertical") -> Axes:
    assert orientation in [
        "vertical",
        "horizontal",
    ], "orientation must be 'vertical' or 'horizontal'."

    if orientation == "vertical":
        grid_axis = "y"
        invisible_spines = ["left", "right", "top"]
    else:
        grid_axis = "x"
        invisible_spines = ["bottom", "right", "top"]

    # Set grid
    setMajorGrids(ax, axis=grid_axis)

    # make all but left spine invisible
    makePatchSpinesInvisible(ax, invisible_spines)

    # Set x and y axes default formats
    if orientation == "vertical":
        configIndependentXAxis(ax, pad_side="right", minor_ticks_on=False)
        configDependentYAxis(ax, side="right", label_location="right")
    else:
        configDepdendentXAxis(ax, side="top")
        configIndependentYAxis(ax)

    # Set bar zorder to be in front of grids
    PutBarsInFront(ax)

    # Reset legend colors
    setLegendParams(ax)

    return ax


def convertHBox(ax: Axes) -> Axes:
    assert (
        len(ax.patches) > 0
    ), "Input Axes does not have filled boxes. Remake plot by setting patch_artist=True."

    color_map = loadColorMap()
    # Set grid on and color
    setMajorGrids(ax, axis="x")

    # make all but left spine invisible
    makePatchSpinesInvisible(ax, ["top", "right", "bottom"])

    # Set axis default params
    configDepdendentXAxis(ax, side="top")
    configIndependentYAxis(ax)
    replaceAxesMinusGlyphs(ax)

    # Set color of data series
    setBoxColor(ax, color=color_map["web_all"]["blue"])
    setLineColor(ax, color=color_map["web_all"]["blue"])

    return ax
