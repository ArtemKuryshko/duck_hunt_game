from systems.score_system import ScoreSystem


def test_add_score_increases_total():
    score_system = ScoreSystem()

    score_system.add_score(15)

    assert score_system.score == 15


def test_deduct_health_triggers_game_over_callback_once_health_is_depleted():
    calls = []
    score_system = ScoreSystem(on_game_over=lambda: calls.append("game-over"))

    score_system.deduct_health(3)

    assert score_system.health == 0
    assert calls == ["game-over"]


def test_reset_restores_default_values():
    score_system = ScoreSystem()
    score_system.add_score(12)
    score_system.deduct_health(2)

    score_system.reset()

    assert score_system.score == 0
    assert score_system.health == 3
