import pygame
import pygame.gfxdraw
from math import ceil
import random
from CirclePhysical import CirclePhysical
from Goal import Goal
from Team import Team

from Collision import Collision


class GameEngine( object ):
    # object containing Game's data

    screen_w = 1100
    screen_h = int(screen_w / 1.57)

    pitch_w = int(screen_w * 0.8)
    pitch_h = int(pitch_w / 1.57)

    back_color = (164, 143, 91)
    pitch_color_1 = (113, 152, 63)
    pitch_color_2 = (134, 185, 80)

    border_width = 2
    border_color = (174, 202, 137)

    sector_size = 50

    fps = 60
    test_mode = False
    wall_bounce = 1.0

    goal_delay = 0      # in miliseconds
    start_delay = 0     # in miliseconds
    delay_counter = 0

    play_mode = 0
    # play_mode flags states:
    # play_mode = 0 => game running
    # play_mode = -2 => game freezed, players and ball not set on the right positions, waiting time not initialized (set after goal score)
    # play_mode = -1 => game freezed, players and ball not set on the right positions, waiting time initialized (set after goal score and -2 state)
    # play_mode = 1 => game freezed, players and ball set on the right positions, waiting time not initialized (set at the beginning of the game and after -1 state (after goal score cooldown))
    # play_mode = 2 => game freezed, players and ball set on the right positions, waiting time initialized (set after 1 state; after time counter drops to 0, game starts)

    team1_color = (0, 0, 255)
    team2_color = (255, 0, 0)


    def __init__(self, display_mode):
        self.display_mode = display_mode

        if(self.display_mode != 0):
            pygame.init()

            self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
            self.fps_clock = pygame.time.Clock()

        self.done = 0

        self.balls = []      # list containing balls
        self.players = []    # list containing players

        # 2D array containing arrays, to store object in the secotrs and optimise collisions
        self.sectors = [[[] for j in range(ceil(self.screen_h / self.sector_size))] for i in
                        range(ceil(self.screen_w / self.sector_size))]

        # create goals
        screen_margin = (self.screen_h - self.pitch_h) / 2
        self.goal_left = Goal(self, self.pitch_color_1, (self.screen_w - self.pitch_w) / 2,
                              screen_margin + self.pitch_h * 6 / 16, screen_margin + self.pitch_h * 10 / 16, 50, -1)
        self.goal_right = Goal(self, self.pitch_color_2, self.pitch_w + (self.screen_w - self.pitch_w) / 2,
                               screen_margin + self.pitch_h * 6 / 16, screen_margin + self.pitch_h * 10 / 16, 50, 0)

        self.team_right = Team(self, self.team1_color, self.goal_right, 1)
        self.team_left = Team(self, self.team2_color, self.goal_left, -1)


    def draw_background(self):
        # draw backgroud
        self.screen.fill(self.back_color)

        # draw score
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        score_left = font.render(str(self.team_left.score), False, self.team_left.color)
        score_right = font.render(str(self.team_right.score), False, self.team_right.color)

        self.screen.blit(score_left, (self.screen_w / 10, self.screen_h / 20))
        self.screen.blit(score_right, (self.screen_w * 9 / 10, self.screen_h / 20))

        if self.play_mode == -1:
            status_message = font.render('GOAL!', False, (0, 0, 0))
            self.screen.blit(status_message, (self.screen_w * 3 / 10, self.screen_h / 20))
        elif self.play_mode == 2 and self.delay_counter < 500:
            status_message = font.render('PLAY!', False, (0, 0, 0))
            self.screen.blit(status_message, (self.screen_w * 3 / 10, self.screen_h / 20))

        # draw pitch border
        pygame.draw.rect(self.screen, self.border_color, \
                         ((self.screen_w - self.pitch_w) / 2 - self.border_width, \
                          (self.screen_h - self.pitch_h) / 2 - self.border_width, \
                          self.pitch_w + self.border_width * 2 - 1, \
                          self.pitch_h + self.border_width * 2 - 1), \
                         self.border_width)

        # draw pitch stripes
        for i in range(0, 10):
            if i % 2:
                pygame.draw.rect(self.screen, self.pitch_color_1, \
                                 ((self.screen_w - self.pitch_w) / 2 + i * self.pitch_w / 10, \
                                  (self.screen_h - self.pitch_h) / 2, self.pitch_w / 10, \
                                  self.pitch_h))
            else:
                pygame.draw.rect(self.screen, self.pitch_color_2, \
                                 ((self.screen_w - self.pitch_w) / 2 + i * self.pitch_w / 10, \
                                  (self.screen_h - self.pitch_h) / 2, self.pitch_w / 10, \
                                  self.pitch_h))

        ### draw pitch lines

        # middle line
        pygame.draw.rect(self.screen, self.border_color, \
                         ((self.screen_w / 2) - self.border_width + 1, \
                          (self.screen_h - self.pitch_h) / 2, \
                          self.border_width * 2, self.pitch_h))

        # circle
        pygame.gfxdraw.aacircle(self.screen, \
                                int(self.screen_w / 2), \
                                int(self.screen_h / 2), \
                                int(self.pitch_w / 8), self.border_color)

        pygame.gfxdraw.aacircle(self.screen, \
                                int(self.screen_w / 2), \
                                int(self.screen_h / 2), \
                                int(self.pitch_w / 8 - 1), self.border_color)

        pygame.gfxdraw.aacircle(self.screen, \
                                int(self.screen_w / 2), \
                                int(self.screen_h / 2), \
                                int(self.pitch_w / 8 - 2), self.border_color)

        # dot
        pygame.gfxdraw.filled_circle(self.screen, \
                                     int(self.screen_w / 2), \
                                     int(self.screen_h / 2), \
                                     self.border_width * 3, self.border_color)

        # draw goals and borders
        pygame.draw.rect(self.screen, self.border_color, (self.goal_left.get_px() - self.border_width, self.goal_left.get_py() - self.border_width,
        self.goal_left.get_width() + self.border_width - 1, self.goal_left.get_height() + self.border_width * 2 - 1),
                         self.border_width)
        pygame.draw.rect(self.screen, self.goal_left.color, (self.goal_left.get_px(), self.goal_left.get_py(), self.goal_left.get_width(), self.goal_left.get_height()))

        pygame.draw.rect(self.screen, self.border_color, (self.goal_right.get_px(), self.goal_right.get_py() - self.border_width,
        self.goal_right.get_width() + self.border_width - 1, self.goal_right.get_height() + self.border_width * 2 - 1),
                         self.border_width)
        pygame.draw.rect(self.screen, self.goal_right.color, (self.goal_right.get_px(), self.goal_right.get_py(), self.goal_right.get_width(), self.goal_right.get_height()))

        # draw posts
        pygame.gfxdraw.filled_circle(self.screen, int(self.goal_left.post_up.p.x), int(self.goal_left.post_up.p.y),
                                     self.goal_left.post_up.size, self.goal_left.post_up.color)
        pygame.gfxdraw.aacircle(self.screen, int(self.goal_left.post_up.p.x), int(self.goal_left.post_up.p.y),
                                self.goal_left.post_up.size, self.goal_left.post_up.color)
        pygame.gfxdraw.filled_circle(self.screen, int(self.goal_left.post_down.p.x), int(self.goal_left.post_down.p.y),
                                     self.goal_left.post_down.size, self.goal_left.post_down.color)
        pygame.gfxdraw.aacircle(self.screen, int(self.goal_left.post_down.p.x), int(self.goal_left.post_down.p.y),
                                self.goal_left.post_down.size, self.goal_left.post_down.color)

        pygame.gfxdraw.filled_circle(self.screen, int(self.goal_right.post_up.p.x), int(self.goal_right.post_up.p.y),
                                     self.goal_right.post_up.size, self.goal_right.post_up.color)
        pygame.gfxdraw.aacircle(self.screen, int(self.goal_right.post_up.p.x), int(self.goal_right.post_up.p.y),
                                self.goal_right.post_up.size, self.goal_right.post_up.color)
        pygame.gfxdraw.filled_circle(self.screen, int(self.goal_right.post_down.p.x),
                                     int(self.goal_right.post_down.p.y), self.goal_right.post_down.size,
                                     self.goal_right.post_down.color)
        pygame.gfxdraw.aacircle(self.screen, int(self.goal_right.post_down.p.x), int(self.goal_right.post_down.p.y),
                                self.goal_right.post_down.size, self.goal_right.post_down.color)


    def clock_tick(self):
        return self.fps_clock.tick(self.fps)


    def new_player(self, player, team_number=None):
        # add new player to the game and team
        self.players.append(player)

        if team_number == None:
            if self.team_left.size() >= self.team_right.size():
                self.team_right.add_player(player)
            else:
                self.team_left.add_player(player)
        else:
            if team_number == 1:
                self.team_left.add_player(player)
            else:
                self.team_right.add_player(player)
                
        self.team_left.reset_positions()
        self.team_right.reset_positions()


    def new_ball(self, ball):
        self.balls.append(ball)


    def redraw(self):

        # control game states
        self.game_state_manager()

        # dt is time since last tick
        if(self.display_mode != 0):
            dt = self.clock_tick()

            if self.delay_counter != 0:
                self.delay_counter -= dt
            if self.delay_counter < 0:
                self.delay_counter = 0

        if self.play_mode == 0:
            # update objects positions and redraw players
            self.update()

        if(self.display_mode != 0):
        # redraw whole board
            self.display_redraw()

        # update the screen
            pygame.display.update()


    def update(self):
        # update object's positions
        for obj in self.players:
            obj.update()
        for obj in self.balls:
            obj.update()


    def display_redraw(self):
        # redraw board and players

        # draw static background
        self.draw_background()

        ### if test mode is on, draw additional markers on screen
        if self.test_mode:

            # draw sectors around ball and players
            for obj in self.players:
                sector_num = int(obj.size * 4 / self.sector_size)
                for i in range(int(obj.p.x / self.sector_size) - sector_num,
                               int(obj.p.x / self.sector_size) + sector_num + 1):
                    for j in range(int(obj.p.y / self.sector_size) - sector_num,
                                   int(obj.p.y / self.sector_size) + sector_num + 1):
                        pygame.draw.rect(self.screen, (0, 255 - ((i + j) % 2) * 50, 0), (i * self.sector_size, j * self.sector_size, int(self.sector_size), int(self.sector_size)))
            for obj in self.balls:
                sector_num = int(obj.size * 4 / self.sector_size)
                for i in range(int(obj.p.x / self.sector_size) - sector_num,
                               int(obj.p.x / self.sector_size) + sector_num + 1):
                    for j in range(int(obj.p.y / self.sector_size) - sector_num,
                                   int(obj.p.y / self.sector_size) + sector_num + 1):
                        pygame.draw.rect(self.screen, (0, 255 - ((i + j) % 2) * 50, 0), (int(obj.p.x / self.sector_size) * self.sector_size,
                        int(obj.p.y / self.sector_size) * self.sector_size, int(self.sector_size),
                        int(self.sector_size)))

            # draw hitboxes
            for obj in self.players:
                pygame.gfxdraw.aacircle(self.screen, int(obj.p.x), int(obj.p.y), obj.hitbox, (0, 0, 255))
            for obj in self.balls:
                pygame.gfxdraw.aacircle(self.screen, int(obj.p.x), int(obj.p.y), obj.hitbox, (0, 0, 255))

            # draw kick trace
            for obj in self.players:
                if obj.mouse_pos != 0:
                    pygame.draw.line(self.screen, obj.border_color, (int(obj.p.x), int(obj.p.y)), (obj.mouse_pos), 2)

        # check collisions and redraw all players
        for obj in self.players:
            Collision.collide(obj)
            pygame.gfxdraw.filled_circle(self.screen, int(obj.p.x), int(obj.p.y), obj.size, obj.color)
            pygame.gfxdraw.aacircle(self.screen, int(obj.p.x), int(obj.p.y), obj.size, obj.border_color)
            pygame.gfxdraw.aacircle(self.screen, int(obj.p.x), int(obj.p.y), obj.size - 1, obj.border_color)

        # check collisions with posts
        self.goal_left.goal_collide()
        self.goal_right.goal_collide()

        # check collisions and redraw balls
        for obj in self.balls:
            # pygame.gfxdraw.filled_circle(self.screen, int(obj.p.x), int(obj.p.y), obj.size, obj.color)
            # pygame.gfxdraw.aacircle(self.screen, int(obj.p.x), int(obj.p.y), obj.size, obj.border_color)
            # pygame.gfxdraw.aacircle(self.screen, int(obj.p.x), int(obj.p.y), obj.size - 1, obj.border_color)
            self.screen.blit(obj.ballImage,
                             pygame.rect.Rect(obj.p.x - obj.size, obj.p.y - obj.size, obj.size, obj.size))


    # fix objects position, to prevent walls collisions
    def walls_collision(self, obj):
        Collision.walls_collision(obj, self)


    # set game state to -2
    # add point to team which scored
    def goal_scored(self, goal):
        if goal == self.goal_left:
            self.team_right.add_point()
            self.done = 1
        else:
            self.team_left.add_point()
            self.done = -1

        # for AI purpose, after goalscore game goes right to the state = 1
        # self.play_mode = -2
        self.play_mode = 1
    

    # quit python game
    def quit(self):
        self.players.clear()
        self.balls.clear()
        self.sectors.clear()
        pygame.quit()


    def game_state_manager(self):
        if self.play_mode == -2:
            # after goal score, prepare delay
            self.play_mode = -1
            self.delay_counter = self.goal_delay
        elif self.play_mode == -1 and self.delay_counter == 0:
            # if delay passed, reset positions and set mode to 1
            self.play_mode = 1
        elif self.play_mode == 1:
            # if game started (or is after goal), prepare delay
            self.positions_reset()
            self.team_left.reset_positions()
            self.team_right.reset_positions()

            self.play_mode = 2
            self.delay_counter = self.start_delay
        elif self.play_mode == 2 and self.delay_counter == 0:
            # if delay passed, start the game
            self.play_mode = 0


    def positions_reset(self):
        for obj in self.balls:
            # obj.set_move((0, 0), (self.screen_w / 2, self.screen_h / 2))
            obj.set_move((0, 0), (random.randrange((self.screen_w - self.pitch_w) / 2, self.pitch_w + (self.screen_w - self.pitch_w) / 2),
                                 random.randrange((self.screen_h - self.pitch_h) / 2, self.pitch_h + (self.screen_h - self.pitch_h) / 2)))


    def is_done(self):
        return self.done

    # reset game
    def game_reset(self):
        self.positions_reset()
        self.team_left.reset_positions()
        self.team_right.reset_positions()
        self.play_mode = 0
        self.team_left.score = 0
        self.team_right.score = 0
        self.done = 0
