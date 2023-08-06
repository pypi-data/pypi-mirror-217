# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
guidata.widgets.objecteditor
============================

This package provides a generic object editor widget.

.. autofunction:: oedit

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import PIL.Image
from guidata.qthelpers import exec_dialog
from guidata.widgets.arrayeditor import ArrayEditor
from guidata.widgets.collectionseditor import CollectionsEditor
from guidata.widgets.nsview import DataFrame, FakeObject, Series, is_known_type
from guidata.widgets.texteditor import TextEditor
from numpy.core.multiarray import ndarray

try:
    from guidata.widgets.dataframeeditor import DataFrameEditor
except ImportError:
    DataFrameEditor = FakeObject()


if TYPE_CHECKING:
    import numpy as np
    from qtpy import QtWidgets as QW


def create_dialog(obj, title, parent=None):
    """Creates the editor dialog and returns a tuple (dialog, func) where func
    is the function to be called with the dialog instance as argument, after
    quitting the dialog box

    The role of this intermediate function is to allow easy monkey-patching.
    (uschmitt suggested this indirection here so that he can monkey patch
    oedit to show eMZed related data)
    """

    conv_func = lambda data: data
    readonly = not is_known_type(obj)
    if isinstance(obj, ndarray):
        dialog = ArrayEditor(parent)
        if not dialog.setup_and_check(obj, title=title, readonly=readonly):
            return
    elif isinstance(obj, PIL.Image.Image):
        dialog = ArrayEditor(parent)
        import numpy as np

        data = np.array(obj)
        if not dialog.setup_and_check(data, title=title, readonly=readonly):
            return
        conv_func = lambda data: PIL.Image.fromarray(data, mode=obj.mode)
    elif isinstance(obj, (DataFrame, Series)) and DataFrame is not FakeObject:
        dialog = DataFrameEditor(parent)
        if not dialog.setup_and_check(obj):
            return
    elif isinstance(obj, str):
        dialog = TextEditor(obj, title=title, readonly=readonly, parent=parent)
    else:
        dialog = CollectionsEditor(parent)
        dialog.setup(obj, title=title, readonly=readonly)

    def end_func(dialog):
        """

        :param dialog:
        :return:
        """
        return conv_func(dialog.get_value())

    return dialog, end_func


def oedit(
    obj: dict | list | tuple | str | np.ndarray,
    title: str = None,
    parent: QW.QWidget = None,
) -> dict | list | tuple | str | np.ndarray:
    """Edit the object 'obj' in a GUI-based editor and return the edited copy
    (if Cancel is pressed, return None)

    Args:
        obj (dict | list | tuple | str | np.ndarray): object to edit
        title (str, optional): dialog title
        parent (QW.QWidget, optional): parent widget

    Returns:
        dict | list | tuple | str | np.ndarray: edited object
    """
    title = "" if title is None else title
    result = create_dialog(obj, title, parent)
    if result is None:
        return
    dialog, end_func = result
    if exec_dialog(dialog):
        return end_func(dialog)
    return None
