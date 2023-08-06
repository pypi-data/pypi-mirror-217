#!/usr/bin/env python3
from textual.widgets import Static

from lolcatt.casting.caster import Caster


class CasterStatic(Static):
    """Base class for a Static widget containing a Caster."""

    def __init__(self, caster: Caster, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._caster = caster
