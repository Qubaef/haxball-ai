import random
from datetime import datetime
from math import ceil
from typing import List

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


def startUserGameplay():
    # Check if models dir exists
    if not os.path.exists("models"):
        os.makedirs("models")
    agentsInTeam: int = 1
    # Initialize game
    gameController: GameController = GameController(agentsInTeam)
    phase = 0
    # Initialize inputs
    agentsInputs: List[AgentInput] = [AgentInput() for _ in range(agentsInTeam * 2)]

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
    # Main loop of the game
    avg_reward = [0 for _ in range(agentsInTeam * 2)]
    startTime = datetime.now()
    last_frame = 0
    while frameId < config.max_training_timesteps:
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
                # agentsInputs[i].kickPos.x = action[2]
                # agentsInputs[i].kickPos.y = action[3]
                # agentsInputs[i].kick = True if action[4] > 0.5 else False

            ballPos = gameController.engine.balls[0].p
            ballPosPlot.storeVal(frameId, [ballPos[0], ballPos[1]])
            ballPosHeatmap.storeVal(
                int(ballPos[0] / heatmapTileSize), int(ballPos[1] / heatmapTileSize), 1
            )
            player1PosHeatmap.storeVal(
                int(gameController.engine.agents[0].p[0] / heatmapTileSize),
                int(gameController.engine.agents[0].p[1] / heatmapTileSize),
                1,
            )
            frameId += 1
            # Update game state
            # shouldClose = InputManager.parseUserInputs(gameController, agentsInputs[0])
            # gameController.engine.balls[0].set_move((0, 0), pygame.mouse.get_pos())

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
                if frameId % config.update_timestep == 0:
                    print(
                        f"Frame {frameId} - Training time {(datetime.now() - startTime)} - "
                        f"Agent {i} reward: {avg_reward[i] / config.update_timestep}"
                    )
                    config.writer.add_scalar(
                        f"Agent {i} avg reward",
                        avg_reward[i] / config.update_timestep,
                        frameId,
                    )
                    avg_reward[i] = 0
                    if i == 0:
                        ppo[i].update()
                if frameId % config.action_std_decay_freq == 0:
                    ppo[i].decay_action_std(
                        config.action_std_decay_rate, config.min_action_std
                    )
                    if i == 0:
                        config.use_random_action_freq -= (
                            config.use_random_action_decay_rate
                        )
                if frameId % config.save_model_freq == 0:
                    if i == 0:
                        ppo[0].save(
                            f"models/{config.training_timestamp}_ppo_{frameId}.pth"
                        )
                        if last_frame > 0:
                            ppo[1].load(
                                f"models/{config.training_timestamp}_ppo_{frameId}.pth"
                            )
                        last_frame = frameId

        gameController.reset()

    ballPosPlot.show()
    ballPosHeatmap.show()
    player1PosHeatmap.show()


if __name__ == "__main__":
    startUserGameplay()
