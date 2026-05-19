from systems.point_manager import PointManager


def test_creates_points_file_with_defaults(tmp_path):
    points_file = tmp_path / "points.json"

    manager = PointManager(file_path=str(points_file))

    assert manager.points == 0
    assert manager.best_score == 0
    assert points_file.exists()


def test_update_points_persists_total_and_best_score(tmp_path):
    points_file = tmp_path / "points.json"
    manager = PointManager(file_path=str(points_file))

    manager.update_points(12)
    reloaded = PointManager(file_path=str(points_file))

    assert reloaded.points == 12
    assert reloaded.best_score == 12


def test_spend_points_rejects_overspend_and_accepts_valid_purchase(tmp_path):
    points_file = tmp_path / "points.json"
    manager = PointManager(file_path=str(points_file))
    manager.update_points(10)

    assert manager.spend_points(11) is False
    assert manager.spend_points(7) is True
    assert manager.points == 3
