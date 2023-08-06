from pathlib import Path

from pygame import Surface

from robingame.image.utils import (
    load_spritesheet,
    load_image_sequence,
    flip_images,
    recolor_images,
    scale_images,
)


class SpriteAnimation:
    """
    Animates a sequence of images.
    Can scale, flip, and recolor itself.
    """

    images: list[Surface] | None

    def __init__(
        self,
        images: list[Surface] = None,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict = None,
    ):
        self.images = images
        if scale:
            self.scale(scale)
        if flip_x or flip_y:
            self.flip(flip_x, flip_y)
        if colormap:
            self.recolor(colormap)

    @classmethod
    def from_image(
        cls,
        filename: Path | str,
        colorkey=None,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict = None,
    ) -> "SpriteAnimation":
        return cls.from_spritesheet(
            filename=filename,
            image_size=None,
            colorkey=colorkey,
            flip_x=flip_x,
            flip_y=flip_y,
            colormap=colormap,
            scale=scale,
        )

    @classmethod
    def from_spritesheet(
        cls,
        filename: Path | str,
        image_size: (int, int),
        colorkey=None,
        num_images: int = 0,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict = None,
    ) -> "SpriteAnimation":
        images = load_spritesheet(
            filename=filename, image_size=image_size, colorkey=colorkey, num_images=num_images
        )
        return cls(images=images, scale=scale, flip_x=flip_x, flip_y=flip_y, colormap=colormap)

    @classmethod
    def from_image_sequence(
        cls,
        filename: Path | str,
        colorkey=None,
        num_images: int = 0,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict = None,
    ) -> "SpriteAnimation":
        images = load_image_sequence(filename=filename, colorkey=colorkey, num_images=num_images)
        return cls(images=images, scale=scale, flip_x=flip_x, flip_y=flip_y, colormap=colormap)

    ############## playback ###############
    def play(self, n: int):
        """
        Fetch frame with index n. This is used in the game loop (where n is the iteration
        counter) to animate the sprite. Return False when we've run out of frames.
        """
        try:
            return self.images[n]
        except IndexError:
            return False

    def loop(self, n: int):
        """If n is greater than the number of frames, start again at the beginning."""
        return self.play(n % len(self.images))

    def play_once(self, n: int, repeat_frame=-1):
        """Run the animation once and then continue returning the specified frame (default=last
        frame)."""
        try:
            return self.images[n]
        except IndexError:
            return self.images[repeat_frame]

    ############## edit in place ###############
    def flip(self, flip_x: bool, flip_y: bool):
        self.images = flip_images(self.images, flip_x, flip_y)

    def recolor(self, colormap: dict):
        self.images = recolor_images(self.images, colormap)

    def scale(self, scale: float):
        self.images = scale_images(self.images, scale)

    ############## edit and copy ###############
    def flipped_copy(self, flip_x=False, flip_y=False):
        return self.__class__(images=flip_images(self.images, flip_x, flip_y))

    def recolored_copy(self, colormap: dict):
        return self.__class__(images=recolor_images(self.images, colormap))

    def scaled_copy(self, scale: float):
        return self.__class__(images=scale_images(self.images, scale))

    def __len__(self):
        return len(self.images)
