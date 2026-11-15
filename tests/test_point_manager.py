import json

import pytest
from systems.point_manager import PointManager


pytestmark = [pytest.mark.systems]


@pytest.mark.io
def test_creates_points_file_with_defaults(points_file):
    manager = PointManager(file_path=str(points_file))
    assert manager.points == 0
    assert manager.best_score == 0
    assert points_file.exists()


@pytest.mark.io
def test_update_points_persists_total_and_best_score(points_file):
    manager = PointManager(file_path=str(points_file))

    manager.update_points(12)
    reloaded = PointManager(file_path=str(points_file))

    assert reloaded.points == 12
    assert reloaded.best_score == 12


@pytest.mark.unit
def test_spend_points_rejects_overspend_and_accepts_valid_purchase(points_file):
    manager = PointManager(file_path=str(points_file))
    manager.update_points(10)

    assert manager.spend_points(11) is False
    assert manager.spend_points(7) is True
    assert manager.points == 3


@pytest.mark.io
@pytest.mark.parametrize(
    ("contents", "expected_points", "expected_best"),
    [
        ("{", 0, 0),
        ('{"points": 7}', 7, 0),
        ('{"best_score": 21}', 0, 21),
        ("null", 0, 0),
    ],
)
def test_load_from_file_recovers_or_uses_defaults(points_file, contents, expected_points, expected_best):
    points_file.write_text(contents, encoding="utf-8")

    manager = PointManager(file_path=str(points_file))

    assert manager.points == expected_points
    assert manager.best_score == expected_best
    assert json.loads(points_file.read_text(encoding="utf-8")) == {
        "points": expected_points,
        "best_score": expected_best,
    }


@pytest.mark.unit
@pytest.mark.parametrize(
    ("balance", "amount", "expected_result", "expected_balance"),
    [(0, 1, False, 0), (5, 5, True, 0), (9, 4, True, 5)],
)
def test_spend_points_cases(point_manager, balance, amount, expected_result, expected_balance):
    point_manager.points = balance
    point_manager.best_score = max(point_manager.best_score, balance)
    point_manager.update_file()

    result = point_manager.spend_points(amount)

    assert result is expected_result
    assert point_manager.points == expected_balance
