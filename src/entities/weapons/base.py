import pygame

class BaseWeapon:
    def __init__(self, name, ammo_capacity, reload_time, fire_rate):
        self.name = name
        self.ammo_capacity = ammo_capacity
        self.current_ammo = ammo_capacity
        self.reload_time = reload_time * 1000
        self.fire_rate = fire_rate * 1000
        self.reload_timer = 0
        self.is_reloading = False
        self.last_shot_time = 0

    def can_shoot(self):
        now = pygame.time.get_ticks()
        return self.current_ammo > 0 and not self.is_reloading and (now - self.last_shot_time) > self.fire_rate

    def start_reload(self):
        if self.current_ammo < self.ammo_capacity and not self.is_reloading:
            self.is_reloading = True
            self.reload_timer = self.reload_time

    def update(self, dt):
        if self.is_reloading:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.current_ammo = self.ammo_capacity
                self.is_reloading = False

    def shoot(self, mouse_pos, birds):
        if self.can_shoot():
            self.current_ammo -= 1
            self.last_shot_time = pygame.time.get_ticks()
            return True
        return False