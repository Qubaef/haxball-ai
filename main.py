import multiprocessing
import random
from datetime import datetime
from math import ceil
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from typing import List
import pickle
from torch.utils.tensorboard import SummaryWriter
import os
import trainingConfig
from GameController import GameController
from AgentInput import AgentInput
from HaxballEngine import GameEngine
from HaxballEngine.GameEngine import GameState
from HaxballEngine.Properties import InternalProperties
from InputManager import InputManager
from Utils.Plots.HeatmapPlot import HeatmapPlot
from Utils.Plots.LinePlot import LinePlot
import rlSamples.PPO.PPO as PPO


def train_subprocess(
    lastFrame: int,
    previousLastFrame: int,
    reward_queue: Queue,
    proc: int,
    action_std: float,
) -> None:
    gameController: GameController = GameController(1)
    phase = 0
    agentsInputs: List[AgentInput] = [AgentInput() for _ in range(2)]
    frameId: int = 0
    ppo = []
    state0 = gameController.getState(0)
    avg_reward = [0.0 for _ in range(2)]
    config = trainingConfig.TrainingConfig(state0.size, 5, False)
    for i in range(2):
        ppo.append(
            PPO.PPO(
                config.state_dim,
                config.action_dim,
                config.lr_actor,
                config.lr_critic,
                config.gamma,
                config.K_epochs,
                config.eps_clip,
                action_std,
            )
        )
    if lastFrame > 0:
        ppo[0].load(f"models/ppo{lastFrame}.pth")
    if previousLastFrame > 0:
        ppo[1].load(f"models/ppo{previousLastFrame}.pth")
    while frameId < config.update_timestep:
        for t in range(1, config.max_ep_len + 1):
            for i in range(len(agentsInputs)):
                state = gameController.getState(i)
                if (
                    config.use_random_action
                    and random.random() < config.use_random_action_freq
                ):
                    action = ppo[i].select_action(state, True)
                else:
                    action = ppo[i].select_action(state)
                agentsInputs[i].movementDir.x = action[0]
                agentsInputs[i].movementDir.y = action[1]
                agentsInputs[i].kickPos.x = action[2]
                agentsInputs[i].kickPos.y = action[3]
                agentsInputs[i].kick = True if action[4] > 0.5 else False

            frameId += 1
            gameController.nextFrame(agentsInputs)
            for i in range(len(agentsInputs)):
                reward = gameController.generateCurrentReward(i, phase)
                avg_reward[i] += reward
                ppo[i].buffer.rewards.append(reward)
                ppo[i].buffer.is_terminals.append(
                    any(
                        gameController.engine.gameState == state
                        for state in [GameState.GOAL_SCORED or GameState.FINISHED]
                    )
                    or frameId % config.max_ep_len == 0
                )
        gameController.reset()
    buffer = [
        ppo[0].buffer.states,
        ppo[0].buffer.actions,
        ppo[0].buffer.rewards,
        ppo[0].buffer.is_terminals,
        ppo[0].buffer.logprobs,
    ]
    # save buffer to file
    pickle.dump(buffer, open(f"{proc}.bin", "wb"))
    reward_queue.put(avg_reward)


def startUserGameplay():
    # Check if models dir exists
    if not os.path.exists("models"):
        os.makedirs("models")

    class MyManager(BaseManager):
        pass

    MyManager.register("PPO", PPO.PPO)
    agentsInTeam: int = 1
    # Initialize game
    gameController: GameController = GameController(agentsInTeam)

    # Plots data
    frameId: int = 0
    state0 = gameController.getState(0)
    config = trainingConfig.TrainingConfig(state0.size, 5)
    ballPosPlot: LinePlot = LinePlot(
        "Ball-pos", "Frame", ["X", "Y"], config.writer, frameId
    )

    heatmapTileSize: int = 100
    ballPosHeatmap: HeatmapPlot = HeatmapPlot(
        "Ball-pos-heatmap",
        ceil(InternalProperties.SCREEN_WIDTH / heatmapTileSize),
        ceil(InternalProperties.SCREEN_HEIGHT / heatmapTileSize),
        config.writer,
        frameId,
    )

    player1PosHeatmap: HeatmapPlot = HeatmapPlot(
        "Player1-pos-heatmap",
        ceil(InternalProperties.SCREEN_WIDTH / heatmapTileSize),
        ceil(InternalProperties.SCREEN_HEIGHT / heatmapTileSize),
        config.writer,
        frameId,
    )

    ppo = PPO.PPO(
        config.state_dim,
        config.action_dim,
        config.lr_actor,
        config.lr_critic,
        config.gamma,
        config.K_epochs,
        config.eps_clip,
        config.action_std,
        device=config.learningDevice,
    )
    # Main loop of the game
    avg_reward = [0 for _ in range(agentsInTeam * 2)]
    startTime = datetime.now()
    action_std_moment = 1
    last_frame = 0
    prev_last_frame = 0
    while frameId < config.max_training_timesteps:
        reward_queues = [Queue() for _ in range(config.cores)]
        processes = []
        for i in range(config.cores):
            p = multiprocessing.Process(
                target=train_subprocess,
                args=(last_frame, prev_last_frame, reward_queues[i], i, ppo.action_std),
            )
            p.start()
            processes.append(p)
        for i, p in enumerate(processes):
            p.join()
            p.close()
        for i in range(config.cores):
            # load buffer from file
            with open(f"{i}.bin", "rb") as fp:
                buffer = pickle.load(fp)
            ppo.buffer.states.extend(buffer[0])
            ppo.buffer.actions.extend(buffer[1])
            ppo.buffer.rewards.extend(buffer[2])
            ppo.buffer.is_terminals.extend(buffer[3])
            ppo.buffer.logprobs.extend(buffer[4])
            process_avg_reward = reward_queues[i].get()
            for i in range(len(avg_reward)):
                avg_reward[i] += process_avg_reward[i]
        print("Making update")
        ppo.update()
        frameId += config.cores * config.update_timestep
        for i in range(len(avg_reward)):
            avg_reward[i] /= config.cores * config.update_timestep

        delta = datetime.now() - startTime

        for i in range(len(avg_reward)):
            config.writer.add_scalar(f"agent {i} avg reward", avg_reward[i], frameId)
            print(f"{delta}: agent {i} avg reward: {avg_reward[i]}")
        ppo.save(f"models/ppo{frameId}.pth")

        prev_last_frame = last_frame
        last_frame = frameId

        if frameId / config.action_std_decay_freq > action_std_moment:
            ppo.decay_action_std(config.action_std_decay_freq, config.min_action_std)
            action_std_moment += 1

    ballPosPlot.show()
    ballPosHeatmap.show()
    player1PosHeatmap.show()


if __name__ == "__main__":
    startUserGameplay()
