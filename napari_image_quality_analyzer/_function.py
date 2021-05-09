"""
This module is an example of a barebones function plugin for napari

It implements the ``napari_experimental_provide_function`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
import warnings
from typing import TYPE_CHECKING

from enum import Enum
import numpy as np
from napari_plugin_engine import napari_hook_implementation

from napari.types import ImageData, LabelsData, LayerDataTuple


# This is the actual plugin function, where we export our function
# (The functions themselves are defined below)
@napari_hook_implementation
def napari_experimental_provide_function():
    # we can return a single function
    # or a tuple of (function, magicgui_options)
    # or a list of multiple functions with or without options, as shown here:
    return [determine_quality]

def determine_quality(image : ImageData):
    """
    Computes quality of an image as single number.
    """
    quality = np.std(image)
    print("Quality (standard deviation):", quality)
    warnings.warn("Quality (standard deviation): " + str(quality))
    return quality

