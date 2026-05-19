from systems.trajectory_creator import BirdTrajectory


def test_spawn_point_from_left_ends_offscreen_right(monkeypatch):
    monkeypatch.setattr("systems.trajectory_creator.random.randint", lambda start, end: start)

    trajectory = BirdTrajectory(speed=0.1, spawn_point=(-50, 120))

    assert trajectory.p3[0] > trajectory.sw


def test_rotation_angle_is_zero_for_horizontal_path():
    trajectory = BirdTrajectory(speed=0.1, spawn_point=(0, 0))
    trajectory.p0 = (0, 0)
    trajectory.p1 = (10, 0)
    trajectory.p2 = (20, 0)
    trajectory.p3 = (30, 0)

    assert trajectory.get_rotation_angle() == 0.0


def test_update_marks_trajectory_as_finished():
    trajectory = BirdTrajectory(speed=0.6, spawn_point=(0, 0))

    trajectory.update()
    trajectory.update()

    assert trajectory.t == 1.0
    assert trajectory.is_finished is True
