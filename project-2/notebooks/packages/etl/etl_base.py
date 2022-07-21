from __future__ import annotations

from abc import ABC
from packages.utils.logger import Logger
import os


class ETLBase(ABC):

    filesystem_path = os.path.join(os.getcwd(), "layers")

    def __init__(self):
        self._logger = Logger()
