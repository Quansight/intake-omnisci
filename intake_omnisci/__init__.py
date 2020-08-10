__version__ = "0.0.1"

import intake
from .catalog import OmniSciCatalog
from .source import OmniSciSource

__all__ = ["OmniSciCatalog", "OmniSciSource"]
