import jax
import jax.numpy as jnp

import navix as nx
from navix.entities import Player, Goal, Key, Door


def test_rgb():
    height = 10
    width = 10
    grid = jnp.zeros((height - 2, width - 2), dtype=jnp.int32)
    grid = jnp.pad(grid, 1, mode="constant", constant_values=-1)

    state = nx.entities.State(
        key=jax.random.PRNGKey(0),
        grid=grid,
        players=Player.create(position=jnp.asarray((1, 1)), direction=jnp.asarray(0)),
        goals=Goal.create(position=jnp.asarray((4, 4)), probability=jnp.asarray(1.0)),
        keys=Key.create(position=jnp.asarray((2, 2)), id=jnp.asarray(0)),
        doors=Door.create(position=jnp.asarray([(1, 5), (1, 6)]), direction=jnp.asarray((0, 2)), requires=jnp.asarray((0, 0))),
        cache=nx.graphics.RenderingCache.init(grid),
    )
    sprites_registry = nx.graphics.SPRITES_REGISTRY

    doors = state.doors.replace(open=jnp.asarray((False, True)))
    state = state.replace(doors=doors)

    obs = nx.observations.rgb(state, sprites_registry=sprites_registry)
    expected_obs_shape = (height * nx.graphics.TILE_SIZE, width * nx.graphics.TILE_SIZE, 3)
    assert obs.shape == expected_obs_shape, (
        f"Expected observation {expected_obs_shape}, got {obs.shape} instead"
    )

    def get_tile(position):
        x = position[0] * nx.graphics.TILE_SIZE
        y = position[1] * nx.graphics.TILE_SIZE
        return obs[x:x + nx.graphics.TILE_SIZE, y:y + nx.graphics.TILE_SIZE, :]

    player_tile = get_tile(state.players.position)
    assert jnp.array_equal(player_tile, sprites_registry[2][0][0]), player_tile

    goal_tile = get_tile(state.goals.position[0])
    assert jnp.array_equal(goal_tile, sprites_registry[3][0][0]), goal_tile

    key_tile = get_tile(state.keys.position[0])
    assert jnp.array_equal(key_tile, sprites_registry[4][0][0]), key_tile

    door_tile = get_tile(state.doors.position[0])
    assert jnp.array_equal(door_tile, sprites_registry[5][0][0]), door_tile

    door_tile = get_tile(state.doors.position[1])
    assert jnp.array_equal(door_tile, sprites_registry[5][2][1]), door_tile

    return


def test_categorical_first_person():
    height = 10
    width = 10
    grid = jnp.zeros((height - 2, width - 2), dtype=jnp.int32)
    grid = jnp.pad(grid, 1, mode="constant", constant_values=-1)

    state = nx.entities.State(
        key=jax.random.PRNGKey(0),
        grid=grid,
        players=Player.create(position=jnp.asarray((1, 1)), direction=jnp.asarray(0)),
        goals=Goal.create(position=jnp.asarray((4, 4)), probability=jnp.asarray(1.0)),
        keys=Key.create(position=jnp.asarray((2, 2)), id=jnp.asarray(0)),
        doors=Door.create(position=jnp.asarray([(1, 5), (1, 6)]), direction=jnp.asarray((0, 2)), requires=jnp.asarray((0, 0))),
        cache=nx.graphics.RenderingCache.init(grid),
    )

    obs = nx.observations.categorical_first_person(state)
    print(obs)

if __name__ == "__main__":
    # test_rgb()
    test_categorical_first_person()
    jax.jit(test_categorical_first_person)()
