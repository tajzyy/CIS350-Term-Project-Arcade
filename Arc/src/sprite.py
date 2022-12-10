import os
import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, img, color=None):
        super().__init__()
        self.image = img
        self.ORIGINAL_IMAGE = self.image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.IMAGE_RATIO = self.image.get_width() / self.image.get_height()
        self.f_top = float(self.rect.top)
        self.f_left = float(self.rect.left)
        self.rotation_degrees = 0

        if color is not None:
            self.color = color
            color_image = pygame.Surface(
                self.ORIGINAL_IMAGE.get_size()
            ).convert_alpha()
            color_image.fill(color)
            self.image.blit(
                color_image,
                (0, 0),
                special_flags=pygame.BLEND_RGBA_MULT
            )

    def resize(self, new_width, new_height):
        # height = self.ORIGINAL_IMAGE.get_height() * multiplier
        # width = height * self.IMAGE_RATIO
        # self.image = pygame.transform.scale(
        #     self.ORIGINAL_IMAGE,
        #     (width, height)
        # )
        # self.rect = self.image.get_rect(topleft=self.rect.topleft)
        # scales image
        self.image = pygame.transform.scale(
            self.ORIGINAL_IMAGE,
            (new_width, new_height)
        )
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        return self

    # rounding errors if not rotating by 90 degree increments
    # I think
    def rotate(self, degrees):
        self.image = pygame.transform.rotate(self.image, degrees)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.rotation_degrees = degrees
        return self

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect.topleft)

        # circle = pygame.font.SysFont('Ariel', 35).render('.', True, (255, 255, 255))
        # screen.blit(circle, self.rect.topleft)
        # screen.blit(circle, self.rect.topright)
        # screen.blit(circle, self.rect.bottomleft)
        # screen.blit(circle, self.rect.bottomright)


class AnimatedSprite(Sprite):
    def __init__(self, x, y, path, animation_speed, name='base', color=None):
        self.images = self.get_images(path)
        super().__init__(x, y, self.images[0], color)
        self.animation_speed = animation_speed
        self.NUM_IMAGES = len(self.images)

        self.animations = {name: self.images}
        self.animation_speeds = {name: animation_speed}
        self.original_animations = {name: self.images}

        self.animation_time_prev = pygame.time.get_ticks()
        self.animation_trigger = False
        self.pause_animation = False

        self.current_sprite = 0
        self.current_animation = name

    def update(self):
        self.check_animation_speed()
        self.animate()

    def animate(self):
        if not self.animation_trigger or self.pause_animation:
            return

        self.current_sprite = (self.current_sprite + 1) % self.NUM_IMAGES

        # Sets image to the contents off the sprites array
        self.image = self.images[self.current_sprite]

    def check_animation_speed(self):
        if self.pause_animation:
            return
        self.animation_trigger = False
        time_now = pygame.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_speed:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    @staticmethod
    def get_images(path: str):
        images = []
        files = {}
        # finds all files in path (ignores folders)
        # also ignores any files not named a digit
        for file in os.listdir(path):
            if not os.path.isfile(os.path.join(path, file)):
                continue

            # splits file_name from extension
            file_name, file_extension = os.path.splitext(file)
            if not file_name.isnumeric():
                continue

            # adds file_extension to a dict at key file_name
            # this way, we can sort later and still
            # know what the file name is
            files[file_name] = file_extension

        for file_name in sorted(files, key=int):
            img = pygame.image.load(
                f'{path}/{file_name}{files[file_name]}').convert_alpha()
            images.append(img)

        return images

    # from https://predictivehacks.com/?all-tips=how-to-split-a-list-into-equal-elements-in-python
    # don't really know how it works but it does
    @staticmethod
    def split_list(user_input: list, num_elem):
        output = []
        for i in range(0, len(user_input), num_elem):
            output.append(user_input[i:i + num_elem])

        return output

    def split_animations(self, name, num_animations):
        all_images = self.animations[name]

        # split into right=0, down=1, left=2, up=3
        split_images = self.split_list(
            list(all_images), len(all_images)//num_animations)

        return split_images

    def resize(self, new_width, new_height):
        for animation_name, images in self.animations.items():
            for i, _ in enumerate(images):
                self.animations[animation_name][i] = pygame.transform.scale(
                    self.original_animations[animation_name][i], (new_width, new_height)
                )
        self.set_animation(self.current_animation)
        self.image = self.images[int(self.current_sprite)]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        return self

    def rotate(self, degrees):
        self.images = [pygame.transform.rotate(i, degrees)
                       for i in self.animations[self.current_animation]]
        self.image = self.images[self.current_sprite]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        return self

    def add_animation(self, name: str, folder_path: str, animation_speed: float = None):
        if animation_speed is None:
            animation_speed = self.animation_speed
        self.original_animations[name] = self.get_images(folder_path)
        self.animations[name] = self.original_animations[name]
        self.animation_speeds[name] = animation_speed

    def add_animation_w_images(self, name: str, images: list, animation_speed: float = None):
        if animation_speed is None:
            animation_speed = self.animation_speed
        self.original_animations[name] = images
        self.animations[name] = images
        self.animation_speeds[name] = animation_speed

    def set_animation(self, name):
        if name not in self.animations:
            print(f'{name} not in animations')
            return
        # ignore if it's already at that animation
        if name == self.current_animation:
            return
        self.current_sprite = 0
        self.current_animation = name
        self.images = self.animations[name]
        self.animation_speed = self.animation_speeds[name]
        self.NUM_IMAGES = len(self.images)
