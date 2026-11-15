import pytest
from systems.level_manager import LevelManager
from systems.score_system import ScoreSystem


def create_manager(on_bird_escape=None, difficulty="easy"):
    score_system = ScoreSystem()
    manager = LevelManager(
        score_system=score_system,
        on_bird_escape=on_bird_escape or (lambda: None),
        difficulty=difficulty,
    )
    return manager, score_system


pytestmark = [pytest.mark.systems, pytest.mark.unit]


def test_spawn_timer_calls_spawn_bird_when_interval_is_reached(level_manager, monkeypatch):
    calls = []

    monkeypatch.setattr(level_manager, "spawn_bird", lambda: calls.append("spawned"))

    level_manager.update(level_manager.spawn_interval)

    assert calls == ["spawned"]
    assert level_manager.spawn_timer == 0


def test_shot_bird_awards_score_once_and_is_removed_after_fall(stub_bird_factory):
    manager, score_system = create_manager()
    bird = stub_bird_factory(isAlive=False, was_shot=True, damage=0, kill_points=25, y=500)
    manager.birds.append(bird)

    manager.update(16)

    assert score_system.score == 25
    assert bird.points_handled is True
    assert manager.birds == []


def test_damaging_bird_removes_health_and_bird(stub_bird_factory):
    manager, score_system = create_manager()
    bird = stub_bird_factory(isAlive=False, was_shot=True, damage=2, y=100)
    manager.birds.append(bird)

    manager.update(16)

    assert score_system.health == 1
    assert bird.points_handled is True
    assert manager.birds == []


def test_offscreen_regular_bird_triggers_escape_penalty(stub_bird_factory):
    escapes = []
    manager, _ = create_manager(on_bird_escape=lambda: escapes.append("escaped"))
    bird = stub_bird_factory(x=-100, y=10, damage=0)
    manager.birds.append(bird)

    manager.update(16)

    assert escapes == ["escaped"]
    assert manager.birds == []


@pytest.mark.parametrize(
    ("difficulty", "expected_interval"),
    [("easy", 2000), ("medium", 1500), ("hard", 1000)],
)
def test_difficulty_controls_spawn_interval(difficulty, expected_interval):
    manager, _ = create_manager(difficulty=difficulty)

    assert manager.spawn_interval == expected_interval


def test_settings_manager_difficulty_is_used_when_not_passed(mock_settings_manager):
    score_system = ScoreSystem()

    manager = LevelManager(
        score_system=score_system,
        on_bird_escape=lambda: None,
        settings_manager=mock_settings_manager,
    )

    assert manager.difficulty == "medium"
    assert manager.spawn_interval == 1500


def test_update_collects_effects_from_birds(level_manager, stub_bird_factory):
    effect = object()
    bird = stub_bird_factory(update_result=effect)
    level_manager.birds.append(bird)

    new_effects = level_manager.update(16)

    assert new_effects == [effect]


@pytest.mark.parametrize(
    ("x", "y"),
    [(-100, 10), (900, 10), (10, -100), (10, 700)],
)
def test_offscreen_regular_bird_is_removed_for_any_boundary(level_manager, stub_bird_factory, x, y):
    bird = stub_bird_factory(x=x, y=y, damage=0)
    level_manager.birds.append(bird)

    level_manager.update(16)

    assert level_manager.birds == []


def test_offscreen_damaging_bird_is_removed_without_escape_penalty(stub_bird_factory):
    escapes = []
    manager, _ = create_manager(on_bird_escape=lambda: escapes.append("escaped"))
    bird = stub_bird_factory(x=-100, y=10, damage=1)
    manager.birds.append(bird)

    manager.update(16)

    assert escapes == []
    assert manager.birds == []
