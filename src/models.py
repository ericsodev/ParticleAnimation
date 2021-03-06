from __future__ import annotations
from typing import List

from PIL import Image, ImageDraw, ImageColor
import cv2
import numpy as np
import random
import math


class Particle:
    """A class representing an animated particle

    === Class variables ===
    default_colours: The colours used when choosing random particle colours

    === Instance variables ===
    radius: Radius of the particle
    mass: Mass of the particle
    center: A list containing of the center (x,y) of the particle
    velocity: A list containing the (x,y) velocity
    colour: Particle colour
    constraints: The dimensions of the container
    acceleration: A list containing (x,y) acceleration (px per s^2)
    """
    default_colors = ["#e67e22", "#2ecc71", "#8e44ad", "#1abc9c"]
    radius: float
    mass: float
    center: list[int]
    velocity: list[float]
    colour: str
    constraints: tuple[int, int]
    acceleration: list[float]

    def __init__(self, radius: int, mass: int,
                 center: list[int], v: list[float],
                 constraints: tuple[int, int],
                 acceleration: list[float],
                 colour="") -> None:
        self.radius = radius
        self.mass = mass
        self.center = center
        self.velocity = v
        self.constraints = constraints
        self.acceleration = acceleration

        # Assign random colour if colour was not provided
        if colour == "":
            self.colour = Particle.default_colors[
                random.randint(0, len(Particle.default_colors) - 1)]

    def collide(self, di: int) -> bool:
        """Check if the particle collides the container's bounds
        :param di: 0 for "x" dimension, 1 for "y" dimension

        Precondition:
            di in [0, 1]
        """
        return not (self.center[di] + self.radius < self.constraints[di] and
                    self.center[di] - self.radius > 0)

    def update(self, dt: float) -> None:
        """Update the particle's position, velocity into the next frame
        """

        for i in [0, 1]:
            # Update particle position
            self.center[i] += math.floor(self.velocity[i] * dt)
            # Check collision with container
            if self.collide(i):
                self.velocity[i] *= -1
            # Apply acceleration to velocity
            self.velocity[i] = self.acceleration[i] + self.velocity[i]


class Container:
    """A class representing the box containing all particles

    === Instance Attributes ===
    height: Height of the box
    width: Width of the box
    acceleration: The constant acceleration each particle experiences
    particles: List of particles contained in this box

    === Representation Invariants ===
    height >= 100
    width >= 100
    """
    height: int
    width: int
    acceleration: list[float]
    particles: List[Particle]

    def __init__(self, w: int, h: int, particles: list[Particle] = None,
                 acceleration: list[int, int] = (0, 0)) -> None:
        """Initialize an empty box
        Preconditions:
        width >= 100
        height >= 100
        """
        self.width = w
        self.height = h
        self.acceleration = acceleration
        self.particles = []

        if particles:
            for particle in particles:
                if self.check_in_bounds(particle):
                    self.particles.append(particle)
                else:
                    print(
                        "A particle did not conform to container's dimensions: "
                        "Omitted!")

    def update(self, fps: int) -> None:
        """Update all particles in this box"""
        for particle in self.particles:
            particle.update(60 / fps)

    def check_in_bounds(self, particle: Particle) -> bool:
        """Check if a given particle is within this container's bound s"""
        return particle.center[0] + particle.radius <= self.width and \
               particle.center[0] - particle.radius >= 0 and \
               particle.center[1] + particle.radius <= self.height and \
               particle.center[1] - particle.radius >= 0

    def add_random_particle(self, quantity: int = 1) -> None:
        """Add a random particle conforming to the container's bounds"""
        for _ in range(quantity):
            max_square_len = min(self.width, self.height)
            r = random.randint(math.floor(0.05 * max_square_len),
                               math.floor(0.1 * max_square_len))

            cx = random.randint(0 + r, self.width - r)
            cy = random.randint(0 + r, self.height - r)
            v = [random.randint(-math.floor(0.05 * max_square_len),
                                math.floor(0.05 * max_square_len))
                 for _ in [0, 1]]

            particle = Particle(r, random.randint(1, 10), [cx, cy], v,
                     (self.width, self.height), self.acceleration)
            self.particles.append(particle)


class Animation:
    """A class of an animation
    === Instance Attributes ===
    fps: frame-rate of the animation
    duration: length of the animation in seconds
    resolution: dimensions of the animation
    title: output file name
    """
    fps: int
    duration: int
    resolution: tuple[int, int]
    container: Container
    frames: list[Image]
    title: str

    def __init__(self, fps: int, duration: int, res: tuple[int, int],
                 title: str = "animation") -> None:
        """Initialize an animation with randomly generated particles"""
        self.fps = fps
        self.duration = duration
        self.resolution = res
        self.frames = []
        self.container = Container(res[0], res[1], acceleration=[0, 0])
        self.container.add_random_particle(1)
        self.title = title

    def start(self) -> None:
        """Start rendering animation"""
        output = cv2.VideoWriter(f'./output/{self.title}.avi',
                                 cv2.VideoWriter_fourcc(*"DIVX"),
                                 self.fps, self.resolution)
        for i in range(self.fps * self.duration):
            if i % 20:
                self.composite_frames(output)
            self.record_frame()
            self.container.update(self.fps)

        self.composite_frames(output)
        output.release()

    def record_frame(self) -> None:
        """Record the current frame"""
        frame = Image.new(mode="RGB", size=self.resolution,
                          color=ImageColor.getrgb("#141414"))
        draw = ImageDraw.Draw(frame)
        for p in self.container.particles:
            cx, cy = p.center
            r = p.radius
            col = ImageColor.getrgb(p.colour)
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        self.frames.append(frame)

    def composite_frames(self, output: cv2.VideoWriter) -> None:
        """Composite current frames into an animation"""
        while len(self.frames) > 0:
            output.write(np.array(self.frames.pop(0)))
