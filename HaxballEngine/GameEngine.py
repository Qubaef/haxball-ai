import pygame
import pygame.gfxdraw
from math import ceil
from HaxballEngine.Goal import Goal
from HaxballEngine.Properties import Properties, InternalProperties, ColorPalette
from HaxballEngine.Team import Team

from HaxballEngine.Collision import Collision


class GameEngine(object):
    bots_timer = 0

    goal_delay = 0  # in milliseconds
    start_delay = 0  # in milliseconds
    delay_counter = 0

    play_mode = 1
    # play_mode flags states:
    # play_mode = 0 => game running
    # play_mode = -2 => game freezed, players and ball not set on the right positions, waiting time not initialized (set after goal score)
    # play_mode = -1 => game freezed, players and ball not set on the right positions, waiting time initialized (set after goal score and -2 state)
    # play_mode = 1 => game freezed, players and ball set on the right positions, waiting time not initialized (set at the beginning of the game and after -1 state (after goal score cooldown))
    # play_mode = 2 => game freezed, players and ball set on the right positions, waiting time initialized (set after 1 state; after time counter drops to 0, game starts)

    balls = []  # list containing balls
    players = []  # list containing players

    def __init__(self):
        pygame.init()

        self.done = False
        self.screen = pygame.display.set_mode(InternalProperties.SCREEN_SIZE)
        self.fps_clock = pygame.time.Clock()

        # 2D array containing arrays, to store object in the sectors and optimise collisions
        sectorsY = ceil(InternalProperties.SCREEN_HEIGHT / InternalProperties.COLLISION_SECTOR_SIZE)
        sectorsX = ceil(InternalProperties.SCREEN_WIDTH / InternalProperties.COLLISION_SECTOR_SIZE)
        self.sectors = [[[] for j in range(sectorsY)] for i in range(sectorsX)]

        # create goals
        screen_margin = (InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2
        self.goal_left = Goal(self, ColorPalette.PITCH_1,
                              (InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2,
                              screen_margin + InternalProperties.PITCH_HEIGHT * 6 / 16,
                              screen_margin + InternalProperties.PITCH_HEIGHT * 10 / 16, 50, -1)
        self.goal_right = Goal(self, ColorPalette.PITCH_2, InternalProperties.PITCH_WIDTH + (
                InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2,
                               screen_margin + InternalProperties.PITCH_HEIGHT * 6 / 16,
                               screen_margin + InternalProperties.PITCH_HEIGHT * 10 / 16, 50, 0)

        self.team_right = Team(self, ColorPalette.TEAM_1, self.goal_right, 1)
        self.team_left = Team(self, ColorPalette.TEAM_2, self.goal_left, -1)

    def draw_background(self):
        # draw background
        self.screen.fill(ColorPalette.BACKGROUND)

        # draw score
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        score_left = font.render(str(self.team_left.score), False, self.team_left.color)
        score_right = font.render(str(self.team_right.score), False, self.team_right.color)

        self.screen.blit(score_left, (InternalProperties.SCREEN_WIDTH / 10, InternalProperties.SCREEN_HEIGHT / 20))
        self.screen.blit(score_right, (InternalProperties.SCREEN_WIDTH * 9 / 10, InternalProperties.SCREEN_HEIGHT / 20))

        if self.play_mode == -1:
            status_message = font.render('GOAL!', False, (0, 0, 0))
            self.screen.blit(status_message,
                             (InternalProperties.SCREEN_WIDTH * 3 / 10, InternalProperties.SCREEN_HEIGHT / 20))
        elif self.play_mode == 2 and self.delay_counter < 500:
            status_message = font.render('PLAY!', False, (0, 0, 0))
            self.screen.blit(status_message,
                             (InternalProperties.SCREEN_WIDTH * 3 / 10, InternalProperties.SCREEN_HEIGHT / 20))

        # draw pitch border
        pygame.draw.rect(self.screen, ColorPalette.BORDER,
                         ((
                                      InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2 - InternalProperties.BORDER_WIDTH,
                          (
                                      InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2 - InternalProperties.BORDER_WIDTH,
                          InternalProperties.PITCH_WIDTH + InternalProperties.BORDER_WIDTH * 2 - 1,
                          InternalProperties.PITCH_HEIGHT + InternalProperties.BORDER_WIDTH * 2 - 1),
                         InternalProperties.BORDER_WIDTH)

        # draw pitch stripes
        for i in range(0, 10):
            if i % 2:
                pygame.draw.rect(self.screen, ColorPalette.PITCH_1,
                                 ((
                                          InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2 + i * InternalProperties.PITCH_WIDTH / 10,
                                  (InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2,
                                  InternalProperties.PITCH_WIDTH / 10,
                                  InternalProperties.PITCH_HEIGHT))
            else:
                pygame.draw.rect(self.screen, ColorPalette.PITCH_2,
                                 ((
                                          InternalProperties.SCREEN_WIDTH - InternalProperties.PITCH_WIDTH) / 2 + i * InternalProperties.PITCH_WIDTH / 10,
                                  (InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2,
                                  InternalProperties.PITCH_WIDTH / 10,
                                  InternalProperties.PITCH_HEIGHT))

        # draw pitch lines

        # middle line
        pygame.draw.rect(self.screen, ColorPalette.BORDER,
                         ((InternalProperties.SCREEN_WIDTH / 2) - InternalProperties.BORDER_WIDTH + 1,
                          (InternalProperties.SCREEN_HEIGHT - InternalProperties.PITCH_HEIGHT) / 2,
                          InternalProperties.BORDER_WIDTH * 2, InternalProperties.PITCH_HEIGHT))

        # circle
        pygame.gfxdraw.aacircle(self.screen,
                                int(InternalProperties.SCREEN_WIDTH / 2),
                                int(InternalProperties.SCREEN_HEIGHT / 2),
                                int(InternalProperties.PITCH_WIDTH / 8), ColorPalette.BORDER)

        pygame.gfxdraw.aacircle(self.screen,
                                int(InternalProperties.SCREEN_WIDTH / 2),
                                int(InternalProperties.SCREEN_HEIGHT / 2),
                                int(InternalProperties.PITCH_WIDTH / 8 - 1), ColorPalette.BORDER)

        pygame.gfxdraw.aacircle(self.screen,
                                int(InternalProperties.SCREEN_WIDTH / 2),
                                int(InternalProperties.SCREEN_HEIGHT / 2),
                                int(InternalProperties.PITCH_WIDTH / 8 - 2), ColorPalette.BORDER)

        # dot
        pygame.gfxdraw.filled_circle(self.screen,
                                     int(InternalProperties.SCREEN_WIDTH / 2),
                                     int(InternalProperties.SCREEN_HEIGHT / 2),
                                     InternalProperties.BORDER_WIDTH * 3, ColorPalette.BORDER)

        # draw goals and borders
        pygame.draw.rect(self.screen, ColorPalette.BORDER, (
            self.goal_left.get_px() - InternalProperties.BORDER_WIDTH, self.goal_left.get_py() - InternalProperties.BORDER_WIDTH,
            self.goal_left.get_width() + InternalProperties.BORDER_WIDTH - 1,
            self.goal_left.get_height() + InternalProperties.BORDER_WIDTH * 2 - 1),
                         InternalProperties.BORDER_WIDTH)
        pygame.draw.rect(self.screen, self.goal_left.color, (
            self.goal_left.get_px(), self.goal_left.get_py(), self.goal_left.get_width(), self.goal_left.get_height()))

        pygame.draw.rect(self.screen, ColorPalette.BORDER, (
            self.goal_right.get_px(), self.goal_right.get_py() - InternalProperties.BORDER_WIDTH,
            self.goal_right.get_width() + InternalProperties.BORDER_WIDTH - 1,
            self.goal_right.get_height() + InternalProperties.BORDER_WIDTH * 2 - 1),
                         InternalProperties.BORDER_WIDTH)
        pygame.draw.rect(self.screen, self.goal_right.color, (
            self.goal_right.get_px(), self.goal_right.get_py(), self.goal_right.get_width(),
            self.goal_right.get_height()))

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
        return self.fps_clock.tick(InternalProperties.TARGET_FPS)

    def new_player(self, player, team_number=None):
        # add new player to the game and team
        self.players.append(player)

        if team_number is None:
            if self.team_left.size() >= self.team_right.size():
                self.team_right.add_player(player)
            else:
                self.team_left.add_player(player)
        else:
            if team_number == 1:
                self.team_left.add_player(player)
            else:
                self.team_right.add_player(player)

    def new_ball(self, ball):
        self.balls.append(ball)

    def redraw(self):

        # control game states
        self.game_state_manager()

        # dt is time since last tick
        dt = self.clock_tick()

        self.bots_timer += dt

        if self.delay_counter != 0:
            self.delay_counter -= dt
        if self.delay_counter < 0:
            self.delay_counter = 0

        if self.play_mode == 0:
            # update objects positions and redraw players
            self.update()

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

        # if test mode is on, draw additional markers on screen
        if Properties.TEST_MODE:

            # draw sectors around ball and players
            for obj in self.players:
                sector_num = int(obj.size * 4 / InternalProperties.COLLISION_SECTOR_SIZE)
                for i in range(int(obj.p.x / InternalProperties.COLLISION_SECTOR_SIZE) - sector_num,
                               int(obj.p.x / InternalProperties.COLLISION_SECTOR_SIZE) + sector_num + 1):
                    for j in range(int(obj.p.y / InternalProperties.COLLISION_SECTOR_SIZE) - sector_num,
                                   int(obj.p.y / InternalProperties.COLLISION_SECTOR_SIZE) + sector_num + 1):
                        pygame.draw.rect(self.screen, (0, 255 - ((i + j) % 2) * 50, 0), (
                            i * InternalProperties.COLLISION_SECTOR_SIZE, j * InternalProperties.COLLISION_SECTOR_SIZE, int(InternalProperties.COLLISION_SECTOR_SIZE), int(InternalProperties.COLLISION_SECTOR_SIZE)))
            for obj in self.balls:
                sector_num = int(obj.size * 4 / InternalProperties.COLLISION_SECTOR_SIZE)
                for i in range(int(obj.p.x / InternalProperties.COLLISION_SECTOR_SIZE) - sector_num,
                               int(obj.p.x / InternalProperties.COLLISION_SECTOR_SIZE) + sector_num + 1):
                    for j in range(int(obj.p.y / InternalProperties.COLLISION_SECTOR_SIZE) - sector_num,
                                   int(obj.p.y / InternalProperties.COLLISION_SECTOR_SIZE) + sector_num + 1):
                        pygame.draw.rect(self.screen, (0, 255 - ((i + j) % 2) * 50, 0), (
                            int(obj.p.x / InternalProperties.COLLISION_SECTOR_SIZE) * InternalProperties.COLLISION_SECTOR_SIZE,
                            int(obj.p.y / InternalProperties.COLLISION_SECTOR_SIZE) * InternalProperties.COLLISION_SECTOR_SIZE, int(InternalProperties.COLLISION_SECTOR_SIZE),
                            int(InternalProperties.COLLISION_SECTOR_SIZE)))

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
        else:
            self.team_left.add_point()

        self.play_mode = -2
        self.done = True

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
            obj.set_move((0, 0), (InternalProperties.SCREEN_WIDTH / 2, InternalProperties.SCREEN_HEIGHT / 2))
