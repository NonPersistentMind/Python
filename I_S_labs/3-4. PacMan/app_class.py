import pygame
import random
import sys
import copy
import json
import psutil
import time

import counters
import memory_profiler
from memory_profiler import *
from pygame import surface

from settings import *
from player_class import *
from analytics import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.walls = []
        self.coins = []
        self.emptycells = []
        self.p_pos = None
        self.load()
        #self.player = Player(self, vec(self.p_pos))


    # @profile(stream=counters.fp)
    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'pause':
                counters.totalTime = 0
                counters.counter = 0
                self.pause_events()
                self.pause_update()
                self.pause_draw()
            elif self.state == 'playing':
                self.playing()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    #@profile
    def playing(self):
        while self.state == 'playing':
            self.playing_events()
            self.playing_update()
            self.playing_draw()

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.walls = []
        self.coins = []
        self.emptycells = []
        #self.p_pos = []
        self.generate()
        self.background = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT))
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                        pygame.draw.rect(self.background, WHITE, (xidx * self.cell_width, yidx * self.cell_height,
                                                                  self.cell_width, self.cell_height))
                    elif char == "0":
                        self.emptycells.append(vec(xidx, yidx))
                        pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
                                                                  self.cell_width, self.cell_height))
            rid = random.randint(0, len(self.emptycells))
            self.coins.append(self.emptycells[rid])
            rid = random.randint(0, len(self.emptycells))
            self.p_pos = [self.emptycells[rid][0], self.emptycells[rid][1]]
            self.player = Player(self, vec(self.p_pos))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height),
                             (WIDTH, x * self.cell_height))


    def reset(self):
        #self.player.grid_pos = vec(self.player.starting_pos)
        #self.player.pix_pos = self.player.get_pix_pos()
        #self.player.direction *= 0
        #self.player.target = self.coins[0]
        #self.player.path = self.player.BFS([int(self.p_pos[0]), int(self.p_pos[1])], [
        #    int(self.player.target[0]), int(self.player.target[1])])
        #self.player.newpath([int(self.player.grid_pos[0]), int(self.player.grid_pos[1])], [
        #    int(self.player.target[0]), int(self.player.target[1])])
        self.player = Player(self, vec(self.p_pos))
        self.state = "pause"

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "pause"

    def start_update(self):
        pass


    def start_draw(self):
        self.draw_text('PUSH SPACE BAR TO CONTINUE', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('Space - PAUSE', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        self.draw_text('Enter - RUN BFS', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 75], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        self.draw_text('R - RELOCATE POINT', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 100], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        self.draw_text('G - GENERATE NEW MAZE', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 125], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        pygame.display.update()


    def pause_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.load()
                    #self.reset()
                if event.key == pygame.K_r:
                    rid = random.randint(0, len(self.emptycells))
                    self.coins = []
                    self.coins.append(self.emptycells[rid])
                    self.reset()
                if event.key == pygame.K_RETURN:
                    self.state = 'playing'
                if event.key == pygame.K_SPACE:
                    self.state = 'start'

    def pause_update(self):
        pass

    def pause_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        self.player.draw()
        pygame.display.update()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.load()
                    #self.reset()
                    self.state = 'pause'
                if event.key == pygame.K_r:
                    rid = random.randint(0, len(self.emptycells))
                    self.coins = []
                    self.coins.append(self.emptycells[rid])
                    self.reset()
                if event.key == pygame.K_1:
                    self.playing_update()
                if event.key == pygame.K_SPACE:
                    self.state = 'start'


    def playing_update(self):
        self.player.update()
        if self.player.grid_pos == self.coins[0]:
            self.reset()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        self.player.draw()
        pygame.display.update()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    def generate(self):
        maze = [[1] * COLS for i in range(ROWS + 1)]

        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if i % 2 == 1 and j % 2 == 1 and i != ROWS and j != COLS - 1:
                    maze[i][j] = 0

        stack = []
        startxid = 1
        startyid = 1
        checked = []
        unchecked = []
        checked.append((startxid, startyid))

        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == 0:
                    unchecked.append((i, j))

        while unchecked != []:
            randlist = []
            if (startxid, startyid + 2) in unchecked:
                randlist.append((startxid, startyid + 2))
            if (startxid + 2, startyid) in unchecked:
                randlist.append((startxid + 2, startyid))
            if (startxid - 2, startyid) in unchecked:
                randlist.append((startxid - 2, startyid))
            if (startxid, startyid - 2) in unchecked:
                randlist.append((startxid, startyid - 2))
            if len(randlist) == 0 and stack != []:
                coord = stack.pop()
                startxid = coord[0]
                startyid = coord[1]
                continue
            stack.append((startxid, startyid))
            rid = random.randint(0, len(randlist) - 1)
            pair = randlist[rid]

            if pair == (startxid, startyid + 2):
                maze[startxid][startyid + 1] = 0
            if pair == (startxid + 2, startyid):
                maze[startxid + 1][startyid] = 0
            if pair == (startxid - 2, startyid):
                maze[startxid - 1][startyid] = 0
            if pair == (startxid, startyid - 2):
                maze[startxid][startyid - 1] = 0
            startxid = pair[0]
            startyid = pair[1]
            checked.append((startxid, startyid))
            unchecked.remove((startxid, startyid))

        walllist = []
        #destroyable = 0

        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == 1:
                    walllist.append((i, j))

        #destroyable = len(walllist) // 10
        destroyable = 100
        for i in range(destroyable):
            randw = random.randint(0, len(walllist) - 1)
            if walllist[randw][0] == 0 or walllist[randw][1] == 0 or walllist[randw][0] == ROWS or walllist[randw][1] == COLS - 1:
                i -= 1
                walllist.remove((walllist[randw][0], walllist[randw][1]))
                continue
            maze[walllist[randw][0]][walllist[randw][1]] = 0
            walllist.remove((walllist[randw][0], walllist[randw][1]))
        with open('walls.txt', 'w') as f:
            for i in range(len(maze)):
                for j in range(len(maze[i])):
                    json.dump(maze[i][j], f)
                    if j == COLS - 1:
                        f.writelines('\n')