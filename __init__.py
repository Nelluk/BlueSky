"""
BlueSky plugin: Monitors IRC channels for BlueSky links and provides post previews
"""

import supybot
import supybot.world as world

__version__ = "1.0.0"
__author__ = "Cline"
__maintainer__ = "Cline"

__contributors__ = {}

from . import config
from . import plugin
from importlib import reload
reload(plugin) # In case we're being reloaded.

Class = plugin.Class
configure = config.configure
