from abc import ABC, abstractmethod


class BaseCollector(ABC):

    @abstractmethod
    def fetch_jobs(self):
        pass