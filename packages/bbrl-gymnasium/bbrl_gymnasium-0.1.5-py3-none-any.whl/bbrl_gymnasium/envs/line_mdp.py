"""
Simple MDP with 5 states and 2 actions
"""

import logging
from typing import Any, Dict, Optional

import gymnasium as gym
from gymnasium import spaces
from gymnasium.utils import seeding

logger = logging.getLogger(__name__)


class LineMDPEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(2)
        self.nb_states = 5
        self.observation_space = spaces.Discrete(self.nb_states)

        self.seed()
        self.viewer = None
        self.state = None
        self.np_random = None

        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        done = False
        reward = 0.0
        if action == 0:
            self.state += 1
            if self.state >= self.nb_states:
                done = True
                reward = 10.0
        else:
            self.state -= 1
            if self.state < 0:
                done = True
                reward = 1.0

        if not done:
            pass
        elif self.steps_beyond_done is None:
            self.steps_beyond_done = 0
        else:
            if self.steps_beyond_done == 0:
                logger.warning(
                    "You are calling 'step()' even though this environment has already returned done = True. "
                    "You should always call 'reset()' once you receive 'done = True' -- "
                    "any further steps are undefined behavior."
                )
                self.steps_beyond_done += 1
        next_state = self.state
        return next_state, reward, done, False, {}

    def reset(self, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None):

        self.state = min(2, self.nb_states - 1)
        self.steps_beyond_done = None
        return self.state, {}

    def render(self, mode="human", close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        screen_width = 600
        screen_height = 400

        if self.viewer is None:
            from gymnasium.envs.classic_control import rendering

            self.viewer = rendering.Viewer(screen_width, screen_height)
        print("Nothing to show")
        return self.viewer.render(return_rgb_array=mode == "rgb_array")
