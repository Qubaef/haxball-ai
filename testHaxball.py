import os
from typing import List

import pygame

from InputManager import InputManager
import trainingConfig
from GameController import GameController
from AgentInput import AgentInput
from HaxballEngine import GameEngine
import rlSamples.PPO.PPO as PPO


def startUserGameplay():
    # Check if models dir exists
    agentsInTeam: int = 1
    total_test_episodes = 5
    # Initialize game
    gameController: GameController = GameController(agentsInTeam, screen=True)
    phase = 0
    # Initialize inputs
    agentsInputs: List[AgentInput] = [AgentInput() for _ in range(agentsInTeam * 2)]

    # Plots data
    frameId: int = 0

    state0 = gameController.getState(0)
    config = trainingConfig.TrainingConfig(state0.size, 5)
    config.action_std = 0.1
    ppo = []
    for i in range(agentsInTeam * 2):
        ppo.append(
            PPO.PPO(
                config.state_dim,
                config.action_dim,
                config.lr_actor,
                config.lr_critic,
                config.gamma,
                config.K_epochs,
                config.eps_clip,
            )
        )
        # find latest model by datetime recurential waights ending with i.pth
        all_models = os.listdir("models")
        latest_model = None
        for model in all_models:
            if model.endswith(f"{i}.pth"):
                if latest_model is None:
                    latest_model = model
                else:
                    if model > latest_model:
                        latest_model = model
        ppo[i].load(f"models/{latest_model}")
        print(f"Loaded model {latest_model}")
    # Main loop of the game
    avg_reward = [0 for _ in range(agentsInTeam * 2)]
    for _ in range(total_test_episodes):
        for t in range(1, config.max_ep_len + 1):
            for i in range(len(agentsInputs)):
                state = gameController.getState(i)
                action = ppo[i].select_action(state)
                agentsInputs[i].movementDir.x = action[0]
                agentsInputs[i].movementDir.y = action[1]
                # agentsInputs[i].kickPos.x = action[2]
                # agentsInputs[i].kickPos.y = action[3]
                # agentsInputs[i].kick = True if action[4] > 0.5 else False

            frameId += 1
            # Update game state
            # shouldClose = InputManager.parseUserInputs(gameController, agentsInputs[0])

            gameController.nextFrame(agentsInputs)
            for i in range(len(agentsInputs)):
                reward = gameController.generateCurrentReward(i, phase)
                avg_reward[i] += reward
                # Log reward
                if frameId % 1000 == 0:
                    print(f"Frame {frameId} - Agent {i} reward: {avg_reward[i] / 1000}")
                    config.writer.add_scalar(
                        f"Agent {i} reward", avg_reward[i] / 1000, frameId
                    )
                    avg_reward[i] = 0

        gameController.reset()


if __name__ == "__main__":
    startUserGameplay()
