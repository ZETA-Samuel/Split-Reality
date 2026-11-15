import pygame

from pathlib import Path

class Player:
    def __init__(self,x,y):
        self.frame_width = 32
        self.frame_height = 96

        
        self.rect = pygame.Rect(x + 10,y + 65,12,25)
        self.draw_position = pygame.Vector2(x,y)
        self.position = pygame.Vector2(self.rect.x,self.rect.y)
        # physics
        self.gravity = 1200
        self.jump_strength = -500
        self.move_speed = 350

        self.velocity = pygame.Vector2(0,0)
        self.on_ground = False
        self.facing_right = True

        self.animation_counts = {
            "idle": 2,
            "jump": 11,
            "fall": 8,
            "teleport": 14,
            "teleport_2": 13,
            "teleport_3": 19,
            "hit_top":2
        }

        self.animation_speeds = {
            "idle": 5,
            "jump": 12,
            "fall": 10,
            "teleport": 15,
            "teleport_2": 15,
            "teleport_3": 15,
            "hit_top": 8
        }

        self.animations = self.load_animations()

        self.current_animation = "idle" 
        self.frame_index = 0
        self.animation_timer = 0

        self.animation_loop = True
        self.animation_finished = False

    def load_animations(self):
        animations = {}

        asset_dir = Path(__file__).resolve().parent / "assets" / "player"

        for name,frame_count in self.animation_counts.items():

            image_path = asset_dir / f"{name}.png"

            sheet = pygame.image.load(str(image_path)).convert_alpha()

            frames = []

            for i in range(frame_count):
                frame = pygame.Rect(i * self.frame_width,0,self.frame_width,self.frame_height)

                image = sheet.subsurface(frame).copy()
                frames.append(image)

            animations[name] = frames

        return animations

    def collides_with_map(self,walls):

        player_mask = pygame.mask.Mask(self.rect.size, fill=True)

        for wall in walls:
            offset = (
                self.rect.x - wall["rect"].x,
                self.rect.y - wall["rect"].y
            )

            if wall["mask"].overlap(player_mask,offset):
                return True

        return False

    def resolve_collision(self,walls,axis):

        if not self.collides_with_map(walls):
            return

        if axis == "x":
            direction = 1 if self.velocity.x > 0 else -1

            while self.collides_with_map(walls):
                self.rect.x -= direction

            self.position.x = self.rect.x
            self.velocity.x = 0

        elif axis == "y":
            direction = 1 if self.velocity.y > 0 else -1

            while self.collides_with_map(walls):
                self.rect.y -= direction

            if direction == 1:
                self.on_ground = True

            self.position.y = self.rect.y
            self.velocity.y = 0

    def set_animation(self,name, loop=True, force=False):

        if name == self.current_animation and not force:
            return 

        self.current_animation = name
        self.frame_index = 0
        self.animation_timer = 0

        self.animation_loop = loop
        self.animation_finished = False

    def play_animation(self,name):
        self.set_animation(name, loop=False,force=True)

    def update_animation(self,dt):
        if self.animation_finished:
            return

        self.animation_timer += dt

        frame_duration = (1/self.animation_speeds[self.current_animation])

        if self.animation_timer >= frame_duration:

            self.animation_timer -= frame_duration
            self.frame_index += 1

            frames = self.animations[self.current_animation]

            if self.frame_index >= len(frames):

                if self.animation_loop:
                    self.frame_index = 0

                else:
                    self.frame_index = len(frames) - 1
                    self.animation_finished = True

    def jump(self):

        if self.on_ground:
            self.velocity.y = self.jump_strength
            self.on_ground = False

    def update(self,dt,walls):
        keys = pygame.key.get_pressed()

        self.velocity.x = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity.x = -self.move_speed 
            self.facing_right = False

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity.x = self.move_speed
            self.facing_right = True

        self.position.x += self.velocity.x * dt
        self.rect.x = round(self.position.x)

        self.resolve_collision(walls, "x")

        self.velocity.y += self.gravity * dt

        self.position.y += self.velocity.y * dt 
        self.rect.y = round(self.position.y)

        self.on_ground = False

        self.resolve_collision(walls, "y")

        if self.velocity.y >= 0:

            self.rect.y += 1

            if self.collides_with_map(walls):
                self.on_ground = True
                self.velocity.y = 0

            self.rect.y -= 1

        self.draw_position.x = self.rect.x - 10
        self.draw_position.y = self.rect.y - 70

        # screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = self.rect.x

        #if self.rect.right > 800:
        #    self.rect.right = 800
        #    self.position.x = self.rect.right


        if self.rect.top < 0:
            self.rect.y = 0
            self.velocity.y = 0
            self.position.y = self.rect.y

        

        if self.velocity.y < 0:
            self.set_animation("jump")
        elif not self.on_ground:
            self.set_animation("fall")
        else:
            self.set_animation("idle")

        self.update_animation(dt)

    def draw(self,surface, camera,zoom):

        image = self.animations[self.current_animation][self.frame_index]

        if not self.facing_right:
            image = pygame.transform.flip(image,True,False)

        draw_x = self.draw_position.x * zoom - camera.x 
        draw_y = self.draw_position.y * zoom - camera.y

        image = pygame.transform.scale(image,(int(image.get_width() * zoom), int(image.get_height() * zoom)))

        surface.blit(image,(round(draw_x),round(draw_y)) )

        hitbox = pygame.Rect(
            round(self.rect.x * zoom - camera.x),
            round(self.rect.y * zoom - camera.y),
            round(self.rect.width * zoom),
            round(self.rect.height * zoom)
        )

        pygame.draw.rect(surface, "red", hitbox ,1)