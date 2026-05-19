from dataclasses import dataclass

from systems.level_manager import LevelManager
from systems.score_system import ScoreSystem


@dataclass
class StubBird:
    x: int = 0
    y: int = 0
    isAlive: bool = True
    was_shot: bool = False
    points_handled: bool = False
    damage: int = 0
    kill_points: int = 0
    update_result: object = None

    def update(self, dt):
        return self.update_result


def create_manager(on_bird_escape=None, difficulty="easy"):
    score_system = ScoreSystem()
    manager = LevelManager(
        score_system=score_system,
        on_bird_escape=on_bird_escape or (lambda: None),
        difficulty=difficulty,
    )
    return manager, score_system


def test_spawn_timer_calls_spawn_bird_when_interval_is_reached(monkeypatch):
    manager, _ = create_manager()
    calls = []

    monkeypatch.setattr(manager, "spawn_bird", lambda: calls.append("spawned"))

    manager.update(manager.spawn_interval)

    assert calls == ["spawned"]
    assert manager.spawn_timer == 0


def test_shot_bird_awards_score_once_and_is_removed_after_fall():
    manager, score_system = create_manager()
    bird = StubBird(isAlive=False, was_shot=True, damage=0, kill_points=25, y=500)
    manager.birds.append(bird)

    manager.update(16)

    assert score_system.score == 25
    assert bird.points_handled is True
    assert manager.birds == []


def test_damaging_bird_removes_health_and_bird():
    manager, score_system = create_manager()
    bird = StubBird(isAlive=False, was_shot=True, damage=2, y=100)
    manager.birds.append(bird)

    manager.update(16)

    assert score_system.health == 1
    assert bird.points_handled is True
    assert manager.birds == []


def test_offscreen_regular_bird_triggers_escape_penalty():
    escapes = []
    manager, _ = create_manager(on_bird_escape=lambda: escapes.append("escaped"))
    bird = StubBird(x=-100, y=10, damage=0)
    manager.birds.append(bird)

    manager.update(16)

    assert escapes == ["escaped"]
    assert manager.birds == []
