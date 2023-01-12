from datetime import datetime

from torch.utils.tensorboard import SummaryWriter


class TrainingConfig:
    def __init__(self, args, state_dim, action_dim):

        self.max_ep_len = 60 * 30  # game take 3 minutes, each second is 15 frames
        self.max_training_timesteps = int(
            54e6
        )  # break training loop if timeteps > max_training_timesteps

        self.action_std = (
            0.6  # starting std for action distribution (Multivariate Normal)
        )
        self.action_std_decay_rate = 0.05  # linearly decay action_std (action_std = action_std-action_std_decay_rate)
        self.min_action_std = (
            0.1  # minimum action_std (stop decay after action_std <= min_action_std)
        )
        self.action_std_decay_freq = int(
            self.max_training_timesteps
            / ((self.action_std - self.min_action_std) / self.action_std_decay_rate + 1)
        )  # action_std decay frequency (in num timesteps)

        # PPO hyperparameters
        self.update_timestep = self.max_ep_len * 20  # update policy every n timesteps
        self.K_epochs = 80  # update policy for K epochs in one PPO update

        self.eps_clip = 0.2  # clip parameter for PPO
        self.gamma = 0.99  # discount factor

        self.lr_actor = 0.0003  # learning rate for actor network
        self.lr_critic = 0.001  # learning rate for critic network

        self.training_timestamp = datetime.now().strftime("%b%d_%H-%M-%S")
        self.training_name = f"{args.name}_{self.training_timestamp}"
        self.writer = SummaryWriter(f"runs/{self.training_timestamp}")

        # state space dimension
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.save_model_freq = 10 * self.update_timestep
        self.use_random_action = True
        self.use_random_action_freq = 0.5
        self.use_random_action_decay_rate = 0.05
