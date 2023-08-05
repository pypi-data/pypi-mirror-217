"""The scheduler algorithm"""
import dataclasses
import random
from datetime import datetime, time, timedelta
from typing import Mapping

START_OF_DAY = time(10, 0)
DAY_LENGTH = 14
INITIAL_TEMPERATURE = 0.2
SWEEP_EXPONENT = -1.0


@dataclasses.dataclass
class Task:
    """Slim struct representing a task"""

    uid: str  # unique identifier of the task
    duration: float  # estimated, in hours
    priority: int  # between 1 and 9
    location: int  # number indicating the location, where 0 is "hybrid"


@dataclasses.dataclass
class TimeSlot:
    """Slim struct representing a time slot, so an event consisting of a start and end date."""

    timestamp: datetime
    duration: float  # in hours

    @property
    def timedelta(self) -> timedelta:
        """
        Returns:
            timedelta: the duration as a datetime.timedelta instance
        """
        return timedelta(hours=self.duration)

    @property
    def end(self) -> datetime:
        """
        Returns:
            datetime: the end timestamp of this time slot
        """
        return self.timestamp + self.timedelta


class AbstractScheduler:
    """Abstract Base Class (ABC) for schedulers."""

    def __init__(self, tasks: list[Task]) -> None:
        """Initialises the scheduler, working on a set of pre-defined tasks.

        Args:
            tasks (list[Task]): the tasks to be scheduled
        """
        self.tasks = tasks

    def uidTaskMap(self) -> Mapping[str, Task]:
        """Generates a dictionary for task lookup by UID.

        Returns:
            Mapping[str, Task]: the dictionary keyed by UID of each task.
        """
        return {task.uid: task for task in self.tasks}

    def schedule(self) -> Mapping[str, TimeSlot]:
        """Schedules the tasks using an MCMC procedure.

        Returns:
            Mapping[str, TimeSlot]: the resulting map of Tasks to TimeSlots
        """
        raise NotImplementedError()


def generateDemoTasks() -> list[Task]:
    """Generates a fixed set of demo tasks."""
    return [
        Task("1", 3.5, 1, 1),
        Task("2", 2.0, 7, 2),
        Task("3", 11.0, 3, 1),
        Task("4", 2.0, 9, 0),
        Task("5", 4.0, 5, 1),
    ]


def generateManyDemoTasks(N: int) -> list[Task]:
    """Generates a larger set of randomly generated demo tasks."""
    return [Task(str(i), random.randint(1, 20) / 2, random.randint(1, 9), random.randint(0, 2)) for i in range(N)]
