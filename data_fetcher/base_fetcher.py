from abc import ABC, abstractmethod

class BaseDataFetcher(ABC):
    @abstractmethod
    def get_options_chain(self, symbol: str):
        pass