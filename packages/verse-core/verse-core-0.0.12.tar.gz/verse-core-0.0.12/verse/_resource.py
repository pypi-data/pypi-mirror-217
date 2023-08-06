from abc import ABC, abstractmethod


class Resource(ABC):
    @abstractmethod
    def set_provider(self, **config) -> None:
        pass
