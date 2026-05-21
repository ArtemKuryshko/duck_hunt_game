import pytest
from entities.birds.whiteDuck import WhiteDuck


@pytest.mark.unit
class TestBird:
    def test_initialization(self, mock_animations, mock_trajectory_class):
        duck = WhiteDuck(100, 100, mock_animations)

        assert duck.health == 1
        assert duck.isAlive is True
        assert duck.x == 100
        assert duck.y == 100
        assert duck.kill_points == 10

    def test_get_damage(self, mock_animations, mock_trajectory_class):
        duck = WhiteDuck(100, 100, mock_animations)
        duck.get_damage(1)

        assert duck.health == 0
        assert duck.isAlive is False
        assert duck.was_shot is True

    def test_move(self, mock_animations, mock_trajectory_class):
        mock_trajectory_class.get_position.side_effect = [(100, 100), (105, 105)]

        duck = WhiteDuck(100, 100, mock_animations)
        duck.move()

        assert duck.x == 105
        assert duck.y == 105
        mock_trajectory_class.update.assert_called_once()

    def test_update_falling(self, mock_animations, mock_trajectory_class):
        duck = WhiteDuck(100, 100, mock_animations)
        duck.isAlive = False
        duck.was_shot = True
        duck.damage = 0

        initial_y = duck.y
        duck.update(16)

        assert duck.y > initial_y
