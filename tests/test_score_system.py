from unittest.mock import Mock

import pytest
from systems.score_system import ScoreSystem


pytestmark = [pytest.mark.systems, pytest.mark.unit]


@pytest.mark.parametrize(("start_score", "amount", "expected"), [(0, 15, 15), (10, 5, 15)])
def test_add_score_increases_total(start_score, amount, expected):
    score_system = ScoreSystem()
    score_system.score = start_score

    score_system.add_score(amount)

    assert score_system.score == expected


def test_deduct_health_triggers_game_over_callback_once_health_is_depleted():
    on_game_over = Mock()
    score_system = ScoreSystem(on_game_over=on_game_over)

    score_system.deduct_health(3)

    assert score_system.health == 0
    on_game_over.assert_called_once_with()


def test_deduct_health_without_callback_only_changes_health():
    score_system = ScoreSystem()

    score_system.deduct_health(1)

    assert score_system.health == 2


def test_reset_restores_default_values():
    score_system = ScoreSystem()
    score_system.add_score(12)
    score_system.deduct_health(2)

    score_system.reset()

    assert score_system.score == 0
    assert score_system.health == 3
