import logging
import sys

import traceback
from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    # @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def prompt(self, processed_input):
        pass

