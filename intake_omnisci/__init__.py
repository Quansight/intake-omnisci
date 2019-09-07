__version__ = "0.1.0"

import intake
from .catalog import OmniSciCatalog
from .source import OmniSciSource

__all__ = ["OmniSciCatalog", "OmniSciSource"]
