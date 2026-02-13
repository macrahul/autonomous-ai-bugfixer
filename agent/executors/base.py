from abc import ABC, abstractmethod

class BaseExecutor(ABC):
    """
    Base class for all executors.
    Each executor must:
    - Decide if it applies to a given error log
    - Apply a fix to a given file
    """

    @abstractmethod
    def applies_to(self, error_log: str) -> bool:
        pass

    @abstractmethod
    def apply_fix(self, file_path: str) -> bool:
        """
        Returns:
            True  -> fix applied
            False -> no change or not applicable
        """
        pass

    @abstractmethod
    def name(self) -> str:
        pass