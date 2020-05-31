import _collections as col
import matplotlib.pyplot as plt
import numpy as np

class Stats( object ):
    def __init__(self, results_foldername, plots_foldername, frames_per_game, batch_size, games_per_epoch, save_model_func):
        self.results_foldername = results_foldername
        self.plots_foldername = plots_foldername
        self.filepath = results_foldername + '/' + plots_foldername + '/'

        self.epoch_number = 0
        self.save_model_func = save_model_func
        self.frames_per_game = frames_per_game
        self.games_per_epoch = games_per_epoch
        self.batch_size = batch_size

        self.avg_reward_story_1 = col.deque(maxlen = games_per_epoch)
        self.avg_reward_story_2 = col.deque(maxlen = games_per_epoch)
        self.loss_story = col.deque(maxlen = frames_per_game * games_per_epoch)

        self.kicks_accuracy = 1000
        self.kicks_story = [0] * self.kicks_accuracy


    # plot and save all data; clear data and set new epoch number
    def new_epoch(self):

        # save avg reward
        plt.title("Średnia nagroda od numeru gry")
        plt.plot(range(1, self.games_per_epoch + 1), self.avg_reward_story_1, 'b')
        plt.plot(range(1, self.games_per_epoch + 1), self.avg_reward_story_2, 'r')
        plt.plot([1, self.games_per_epoch + 1], [0, 0], 'y')
        plt.savefig(self.filepath + 'average_reward_' + str(self.epoch_number) + '.png')
        plt.clf()

        # save loss
        plt.title("Strata od numeru uczenia")
        plt.plot(range(1, len(self.loss_story) + 1), self.loss_story, 'b')
        plt.savefig(self.filepath + 'loss_' + str(self.epoch_number) + '.png')
        plt.clf()

        # save kicks to distance
        plt.title("Kopnięcia piłki od odległości gracza od piłki")
        plt.bar(np.arange(0, 1, 1 / self.kicks_accuracy), self.kicks_story, width = 1 / self.kicks_accuracy, color = 'b')
        plt.savefig(self.filepath + 'kicks_' + str(self.epoch_number) + '.png')
        plt.clf()

        # save model as txt file
        self.save_model_func(40, self.results_foldername + '/', self.epoch_number, self.frames_per_game, self.games_per_epoch, self.batch_size)

        # clear all stored data
        self.avg_reward_story_1.clear()
        self.avg_reward_story_2.clear()
        self.loss_story.clear()
        self.kicks_story = [0] * self.kicks_accuracy

        self.epoch_number += 1


    def memorize_avg_reward(self, avg_rew_1, avg_rew_2):
        self.avg_reward_story_1.append(avg_rew_1)
        self.avg_reward_story_2.append(avg_rew_2)


    def memorize_loss(self, loss):
        if loss is not None:
            self.loss_story.append(loss)


    def memorize_kicks(self, distance):
        if distance is not None:
            self.kicks_story[int(distance * self.kicks_accuracy)] += 1