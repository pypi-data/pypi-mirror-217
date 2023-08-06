from tablib.formats import registry

from .format import FastXLSXFormat

registry.register("fast_xlsx", FastXLSXFormat())
