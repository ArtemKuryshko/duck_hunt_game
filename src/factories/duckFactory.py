from config import ANIMATIONS_PATH
from os import path, listdir
from typing import Dict, List
from entities.birds import *
import pygame
class DuckFactory:
    _resources: Dict[str, Dict[str, List[pygame.Surface]]] = {} #кешування анімацій для пташок

    @classmethod
    def load_duck_animations(cls, duck_type: str) -> Dict[str, List[pygame.Surface]]:
        if duck_type not in cls._resources: #заванатження в кеш анімацій пташки
            animations = {
                "Side": [],
                "Up": [],
                "Diagonal": [],
                "Death": []
            }
            
            duck_type_animations = sorted(listdir(path.join(ANIMATIONS_PATH, duck_type)))

            for image in duck_type_animations:
                for animation in animations.keys():
                    if image.startswith(animation):
                        animations[animation].append(pygame.transform.smoothscale(pygame.image.load(path.join(ANIMATIONS_PATH, duck_type, image)).convert_alpha(), (150, 150)))
                        break

            cls._resources[duck_type] = animations

        return cls._resources[duck_type]
    
    @classmethod
    def create_duck(cls,duck_type: str, x: int, y: int) -> BaseBird:
        animations = cls.load_duck_animations(duck_type)
        match duck_type:
            case "WhiteDuck":
                return WhiteDuck(x, y, animations)
            case "BadCrow":
                return BadCrow(x, y, animations)
            case "GreenDuck":
                return GreenDuck(x, y, animations)
            

    