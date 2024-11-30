# -*- coding: utf-8 -*-
"""A class that contains two frames:
    1. pad frame that resizes freely and is given all the
       specified format options
    2. content frame that maintains the specified aspect
       ratio inside the pad frame.

When the pad frame is resized _enforced_aspect_ratio
is called. This is called quite frequently during
window creation and resizing.

The caller needs to
    1. pack/grid the pad frame into the parent as it wants
    2. use the content frame for any widgets that should
       be included in the frame. It should also grid
       those elements.
    3. call row_col_config to allow the created frames
       to changes sizes.

This does not seem to work to make the AspectFrame extend
tk.Frame. Trying to create the interior tk frame seems
to configure the base frame.

Created on Thu Nov  7 12:05:00 2024
@author: Ann"""


import tkinter as tk


class AspectFrames:
    """Create a frame within a frame.  The outer frame (pad)
    changes size as the window size changed.
    The inner frame (content_frame), also changes size but
    maintains the specified aspect ratio.

    Let the parent pack/grid/place the pad frame."""

    def __init__(self, parent, *, aratio=1, **kwargs):
        self.aspect_ratio = aratio

        self.pad = tk.Frame(parent, **kwargs)
        self.content = tk.Frame(self.pad)
        self.content.pack(expand=True, fill='both')

        self.pad.bind("<Configure>", self._enforce_aspect_ratio)


    def _enforce_aspect_ratio(self, event):
        """When the pad window resizes, fit the content into it.

        Try to set the width as the controlling dimension, but
        if the height doesn't fit then use the height as the
        controlling dimension.

        Center the content frame in the pad frame."""

        desired_width = event.width
        desired_height = int(event.width / self.aspect_ratio + 0.5)

        if desired_height > event.height:
            desired_height = event.height
            desired_width = int(event.height * self.aspect_ratio + 0.5)

        xloc = (event.width - desired_width) // 2
        yloc = (event.height - desired_height) // 2
        self.content.place(in_=self.pad, x=xloc, y=yloc,
                          width=desired_width, height=desired_height)


    def row_col_config(self):
        """Configure both frames to expand"""

        self.content.grid_rowconfigure('all', weight=1)
        self.content.grid_columnconfigure('all', weight=1)

        self.pad.grid_rowconfigure('all', weight=1)
        self.pad.grid_columnconfigure('all', weight=1)
