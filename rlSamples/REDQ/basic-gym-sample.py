import gym
from gym import Space

if __name__ == "__main__":
    ENV_NAME: str = "MountainCarContinuous-v0"

    env = gym.make(ENV_NAME, render_mode="human")
    observationSpace: Space = env.observation_space
    actionSpace: Space = env.action_space

    print(f"observationSpace: {observationSpace}")
    print(f"actionSpace: {actionSpace}")

    env.reset()

    for _ in range(1000000):
        env.render()
        newObs, reward, terminated, info, _ = env.step(env.action_space.sample())
        print(f"reward: {reward}")

        if terminated:
            print("Terminated")
            break

    env.close()
