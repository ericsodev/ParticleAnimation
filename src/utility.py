from __future__ import annotations
from models import *


class CollisionDetector:
    """An abstract class for a collision detecting system

    === Attributes ===

    """
    container: Container

    def __init__(self, container: Container) -> None:
        self.container = container

    def _update_positions(self, fps):
        for particle in self.container.particles:
            # update particle positions here
            pass

    def _update_velocity(self, fps):
        pass

    def update(self, fps: int) -> None:
        """Detect collisions and update particle velocity
        Preconditions:
            fps > 0
        """
        raise NotImplementedError


class SweepDetector(CollisionDetector):
    """A collision detector using Sweep and Prune technique

    === Attributes ===
    container: The container of the particles
    sections: Number of sections the container is divided into

    === Representation Invariants ===
    sections >= 1
    """
    container: Container
    sections: int

    def __init__(self, container: Container, sections: int) -> None:
        super().__init__(container)
        self.sections = sections

    def update(self, fps: int) -> None:
        """Detect and update collisions using sweep and prune
        Preconditions:
            fps > 0
        """
        divisions = None


class KDTreeDetector(CollisionDetector):
    """A collision detector using Sweep and Prune technique

    === Attributes ===
    container: The container of the particles

    === Representation Invariants ===
    """
    container: Container

    def __init__(self, container: Container) -> None:
        super().__init__(container)

    def update(self, fps: int) -> None:
        """Detect and update collisions using sweep and prune
        Preconditions:
            fps > 0
        """
        pass
