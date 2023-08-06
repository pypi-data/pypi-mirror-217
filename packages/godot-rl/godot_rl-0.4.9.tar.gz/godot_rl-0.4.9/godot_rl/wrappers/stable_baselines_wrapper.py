import gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env.base_vec_env import VecEnv

from godot_rl.core.godot_env import GodotEnv
from godot_rl.core.utils import lod_to_dol


class StableBaselinesGodotEnv(VecEnv):
    def __init__(self, env_path=None, **kwargs):
        self.env = GodotEnv(env_path=env_path, convert_action_space=True, **kwargs)
        self._check_valid_action_space()
        self.results = None

    def _check_valid_action_space(self):
        action_space = self.env.action_space
        if isinstance(action_space, gym.spaces.Tuple):
            assert (
                len(action_space.spaces) == 1
            ), f"sb3 supports a single action space, this env constains multiple spaces {action_space}"

    def step(self, action):
        obs, reward, term, trunc, info = self.env.step(action)
        obs = lod_to_dol(obs)

        return {k: np.array(v) for k, v in obs.items()}, np.array(reward), np.array(term), info

    def reset(self):
        obs, info = self.env.reset()
        obs = lod_to_dol(obs)
        obs = {k: np.array(v) for k, v in obs.items()}
        return obs

    def close(self):
        self.env.close()

    def env_is_wrapped(self, wrapper_class, indices = None):
        return [False] * self.env.num_envs

    @property
    def observation_space(self):
        return self.env.observation_space

    @property
    def action_space(self):
        # sb3 is not compatible with tuple/dict action spaces
        return self.env.action_space

    @property
    def num_envs(self):
        return self.env.num_envs

    def env_method(self):
        raise NotImplementedError()

    def get_attr(self):
        raise NotImplementedError()

    def seed(self):
        raise NotImplementedError()

    def set_attr(self):
        raise NotImplementedError()

    def step_async(self, actions: np.ndarray):
        # raise NotImplementedError()
        # only works for single instances
        self.results = self.step(actions)

    def step_wait(self):
        # raise NotImplementedError()
        # only works for single instances
        return self.results


def stable_baselines_training(args, extras, n_steps=200000):
    # TODO: Add cla etc for sb3
    env = StableBaselinesGodotEnv(env_path=args.env_path, show_window=args.viz, speedup=args.speedup)

    model = PPO(
        "MultiInputPolicy",
        env,
        ent_coef=0.0001,
        verbose=2,
        n_steps=32,
        tensorboard_log="logs/log",
    )
    model.learn(n_steps)

    print("closing env")
    env.close()
