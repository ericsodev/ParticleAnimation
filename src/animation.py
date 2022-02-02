from __future__ import annotations

from PIL import Image, ImageDraw, ImageColor
import cv2
import numpy as np

from models import Container, Particle


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
        self.container.add_random_particle(5)
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
