import sys
from random import choice, random
import pygame
import hashlib

pygame.init()


class HUD(object):
    HEIGHT, WIDTH = 800, 600
    field_size = 4
    PADDING = 10

    COLOR_WHITE = (255, 255, 255)
    COLOR_GRAY = (200, 200, 200)
    COLOR_GRAY_2 = (220, 220, 220)
    COLOR_BACKGROUND = (244, 240, 229)
    COLOR_FIELD_TABLE = (187, 173, 160)
    COLOR_EMPTY_CELL = (205, 192, 180)
    COLOR_CELL_TEXT_WHITE = (249, 246, 242)
    COLOR_CELL_TEXT_BLACK = (122, 112, 103)

    cell_font = pygame.font.SysFont("Clear Sans", 72)
    title_font = pygame.font.SysFont("Clear Sans", 100)
    score_title_font = pygame.font.SysFont("Clear Sans", 55)
    score_font = pygame.font.SysFont("Clear Sans", 60)

    CELL_COLORS = {
        0: (205, 192, 180),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46)
    }

    def __init__(self, matrix, FIELD_SIZE, SCORE, BEST_SCORE):
        self.matrix = matrix
        self.field_size = FIELD_SIZE
        self.score = SCORE
        self.best_score = BEST_SCORE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption('2048 Game')
        pygame.display.set_icon(pygame.image.load('icon.png'))

    def draw(self):
        self.screen.fill(self.COLOR_BACKGROUND)
        self.draw_score_table()
        self.draw_field_table()

        pygame.display.flip()

    def draw_score_table(self):
        title = self.title_font.render("2048", 1, self.COLOR_CELL_TEXT_BLACK)
        title_place = title.get_rect(center=(self.PADDING * 2 + 100, self.PADDING * 2 + 100))
        self.screen.blit(title, title_place)

        best_score_title = self.score_title_font.render("Best:", 1, self.COLOR_CELL_TEXT_BLACK)
        best_score_sign_place = best_score_title.get_rect(
            center=(self.WIDTH - (self.PADDING * 2 + 250), self.PADDING * 2 + 70))
        self.screen.blit(best_score_title, best_score_sign_place)

        best_score = self.score_font.render(str(self.best_score[0]), 1, self.COLOR_CELL_TEXT_BLACK)
        best_score_place = best_score.get_rect(center=(self.WIDTH - (self.PADDING * 2 + 250), self.PADDING * 2 + 120))
        self.screen.blit(best_score, best_score_place)

        score_title = self.score_title_font.render("Score:", 1, self.COLOR_CELL_TEXT_BLACK)
        score_sign_place = score_title.get_rect(center=(self.WIDTH - (self.PADDING * 2 + 80), self.PADDING * 2 + 70))
        self.screen.blit(score_title, score_sign_place)

        score = self.score_font.render(str(self.score[0]), 1, self.COLOR_CELL_TEXT_BLACK)
        score_place = score.get_rect(center=(self.WIDTH - (self.PADDING * 2 + 80), self.PADDING * 2 + 120))
        self.screen.blit(score, score_place)

    def draw_field_table(self):
        pygame.draw.rect(self.screen, self.COLOR_FIELD_TABLE,
                         (self.PADDING, 200 + self.PADDING, self.WIDTH - self.PADDING * 2,
                          self.HEIGHT - 200 - self.PADDING * 2))
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.screen, self.CELL_COLORS[self.matrix[i][j]],
                                 (self.PADDING * 2 + 142 * j, self.PADDING * 2 + 200 + 142 * i, 132, 132))
                if self.matrix[i][j] != 0:
                    text = self.cell_font.render(str(self.matrix[i][j]), 1,
                                                 self.COLOR_CELL_TEXT_BLACK if self.matrix[i][
                                                                                   j] < 8 else self.COLOR_CELL_TEXT_WHITE)
                    place = text.get_rect(center=(self.PADDING + 142 * j + 75, self.PADDING + 142 * i + 280))
                    self.screen.blit(text, place)

    def draw_lose_screen(self):
        smooth_background = pygame.Surface((self.WIDTH, self.HEIGHT))
        smooth_background.fill(self.COLOR_BACKGROUND)
        smooth_background.set_alpha(140)
        self.screen.blit(smooth_background, (0, 0))

        title = self.title_font.render("You Lose...", 1, self.COLOR_CELL_TEXT_BLACK)
        title_place = title.get_rect(center=(self.PADDING + self.WIDTH // 2, self.PADDING * 2 + 150))
        self.screen.blit(title, title_place)

        score_title = self.score_title_font.render("Score:", 1, self.COLOR_CELL_TEXT_BLACK)
        score_sign_place = score_title.get_rect(center=(self.WIDTH // 2, self.PADDING * 2 + 210))
        self.screen.blit(score_title, score_sign_place)

        score = self.score_font.render(str(self.score[0]), 1, self.COLOR_CELL_TEXT_BLACK)
        score_place = score.get_rect(center=(self.WIDTH // 2, self.PADDING * 2 + 250))
        self.screen.blit(score, score_place)

        tips = self.score_font.render("Press any key to continue...", 1, self.COLOR_CELL_TEXT_BLACK)
        tips_place = score.get_rect(center=(67, self.PADDING * 2 + 500))
        self.screen.blit(tips, tips_place)

        pygame.display.flip()

    def draw_win_screen(self):
        smooth_background = pygame.Surface((self.WIDTH, self.HEIGHT))
        smooth_background.fill(self.COLOR_BACKGROUND)
        smooth_background.set_alpha(140)
        self.screen.blit(smooth_background, (0, 0))

        title = self.title_font.render("You win!", 1, self.COLOR_CELL_TEXT_BLACK)
        title_place = title.get_rect(center=(self.PADDING + self.WIDTH // 2, self.PADDING * 2 + 150))
        self.screen.blit(title, title_place)

        score_title = self.score_title_font.render("Score:", 1, self.COLOR_CELL_TEXT_BLACK)
        score_sign_place = score_title.get_rect(center=(self.WIDTH // 2, self.PADDING * 2 + 210))
        self.screen.blit(score_title, score_sign_place)

        score = self.score_font.render(str(self.score[0]), 1, self.COLOR_CELL_TEXT_BLACK)
        score_place = score.get_rect(center=(self.WIDTH // 2, self.PADDING * 2 + 250))
        self.screen.blit(score, score_place)

        tips = self.score_font.render("Press any key to continue...", 1, self.COLOR_CELL_TEXT_BLACK)
        tips_place = score.get_rect(center=(75, self.PADDING * 2 + 500))
        self.screen.blit(tips, tips_place)

        pygame.display.flip()


class Logic(object):
    START_CELLS = 3

    def __init__(self, MATRIX, FIELD_SIZE, SCORE):
        self.FIELD_SIZE = FIELD_SIZE
        self.score = SCORE
        self.matrix = MATRIX

    def generate_start_cells(self):
        for _ in range(self.START_CELLS):
            self.generate_new_num()

    def move(self, param):
        # Up
        if param == 1:
            for i in range(self.FIELD_SIZE):
                j, j1 = 0, 1
                while j1 < self.FIELD_SIZE:
                    if self.matrix[j][i] == self.matrix[j1][i]:
                        self.matrix[j][i] *= 2
                        self.matrix[j1][i] = 0
                        self.score[0] += self.matrix[j][i]
                    elif self.matrix[j][i] == 0:
                        self.matrix[j][i], self.matrix[j1][i] = self.matrix[j1][i], self.matrix[j][i]
                    elif self.matrix[j1][i] != 0:
                        self.matrix[j + 1][i], self.matrix[j1][i] = self.matrix[j1][i], self.matrix[j + 1][i]
                        j += 1
                    j1 += 1
        # Right
        elif param == 2:
            for i in range(self.FIELD_SIZE):
                j, j1 = self.FIELD_SIZE - 1, self.FIELD_SIZE - 2
                while j1 >= 0:
                    if self.matrix[i][j] == self.matrix[i][j1]:
                        self.matrix[i][j] *= 2
                        self.matrix[i][j1] = 0
                        self.score[0] += self.matrix[j][i]
                    elif self.matrix[i][j] == 0:
                        self.matrix[i][j], self.matrix[i][j1] = self.matrix[i][j1], self.matrix[i][j]
                    elif self.matrix[i][j1] != 0:
                        self.matrix[i][j - 1], self.matrix[i][j1] = self.matrix[i][j1], self.matrix[i][j - 1]
                        j -= 1
                    j1 -= 1
        # Down
        elif param == 3:
            for i in range(self.FIELD_SIZE):
                j, j1 = self.FIELD_SIZE - 1, self.FIELD_SIZE - 2
                while j1 >= 0:
                    if self.matrix[j][i] == self.matrix[j1][i]:
                        self.matrix[j][i] *= 2
                        self.matrix[j1][i] = 0
                        self.score[0] += self.matrix[j][i]
                    elif self.matrix[j][i] == 0:
                        self.matrix[j][i], self.matrix[j1][i] = self.matrix[j1][i], self.matrix[j][i]
                    elif self.matrix[j1][i] != 0:
                        self.matrix[j - 1][i], self.matrix[j1][i] = self.matrix[j1][i], self.matrix[j - 1][i]
                        j -= 1
                    j1 -= 1
        # Left
        elif param == 4:
            for i in range(self.FIELD_SIZE):
                j, j1 = 0, 1
                while j1 < self.FIELD_SIZE:
                    if self.matrix[i][j] == self.matrix[i][j1]:
                        self.matrix[i][j] *= 2
                        self.matrix[i][j1] = 0
                        self.score[0] += self.matrix[j][i]
                    elif self.matrix[i][j] == 0:
                        self.matrix[i][j], self.matrix[i][j1] = self.matrix[i][j1], self.matrix[i][j]
                    elif self.matrix[i][j1] != 0:
                        self.matrix[i][j + 1], self.matrix[i][j1] = self.matrix[i][j1], self.matrix[i][j + 1]
                        j += 1
                    j1 += 1

    def get_empty_list(self):
        empty_list = []
        for i in range(self.FIELD_SIZE):
            for j in range(self.FIELD_SIZE):
                if self.matrix[i][j] == 0:
                    empty_list.append((i, j))
        return empty_list

    def generate_new_num(self):
        empty_list = self.get_empty_list()
        if empty_list:
            i, j = choice(empty_list)
            if random() <= 0.75:
                self.matrix[i][j] = 2
            else:
                self.matrix[i][j] = 4

    def is_empty_cell(self):
        if self.get_empty_list():
            return True
        else:
            return False

    def is_lose(self):
        if self.is_empty_cell():
            return False
        for i in range(self.FIELD_SIZE):
            for j in range(self.FIELD_SIZE):
                if self.matrix[abs(i - 1)][j] == self.matrix[i][j] \
                        or self.matrix[i][abs(j - 1)] == self.matrix[i][j] \
                        or i + 1 < self.FIELD_SIZE and self.matrix[i + 1][j] == self.matrix[i][j] \
                        or j + 1 < self.FIELD_SIZE and self.matrix[i][j + 1] == self.matrix[i][j]:
                    return False
        return True

    def is_win(self):
        for i in range(self.FIELD_SIZE):
            for j in range(self.FIELD_SIZE):
                if self.matrix[i][j] == 2048:
                    return True
        return False


class Game(object):
    FIELD_SIZE = 4
    BEST_SCORE = [0]
    DEBUG = 0

    def __init__(self):
        if self.DEBUG:
            self.MATRIX = [
                [2, 4, 8, 16],
                [32, 64, 128, 4],
                [256, 1024, 4, 2],
                [2, 2, 1024, 0]
            ]
        else:
            self.MATRIX = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]

        self.get_best_score()
        self.SCORE = [0]
        self.GAME_STATE = 1
        self.hud = HUD(self.MATRIX, self.FIELD_SIZE, self.SCORE, self.BEST_SCORE)
        self.logic = Logic(self.MATRIX, self.FIELD_SIZE, self.SCORE)

    def set_best_score(self):
        with open("best_score.sf", "w") as file:
            score_hash = hashlib.sha256(str(self.SCORE[0]).encode())
            data = [score_hash.hexdigest(), str(self.SCORE[0])]
            string = ":".join(data)
            file.write(string)

    def get_best_score(self):
        with open("best_score.sf", "r") as file:
            data = file.readline()
            if not data:
                return
            h256, score = data.split(":")
            if h256 == hashlib.sha256(score.encode()).hexdigest():
                self.BEST_SCORE[0] = int(score)
            else:
                return

    def is_best_score(self):
        return True if self.SCORE[0] > self.BEST_SCORE[0] else False

    def start(self):
        while True:

            self.logic.generate_start_cells()
            self.hud.draw()

            while self.GAME_STATE:

                if self.logic.is_lose() or self.logic.is_win():
                    self.GAME_STATE = 0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    elif event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_UP:
                            self.logic.move(1)
                            self.logic.generate_new_num()
                            self.hud.draw()

                        elif event.key == pygame.K_RIGHT:
                            self.logic.move(2)
                            self.logic.generate_new_num()
                            self.hud.draw()

                        elif event.key == pygame.K_DOWN:
                            self.logic.move(3)
                            self.logic.generate_new_num()
                            self.hud.draw()

                        elif event.key == pygame.K_LEFT:
                            self.logic.move(4)
                            self.logic.generate_new_num()
                            self.hud.draw()

            if self.is_best_score():
                self.set_best_score()

            self.hud.draw_lose_screen() if self.logic.is_lose() else self.hud.draw_win_screen()
            is_continue = 0
            while not is_continue:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    elif event.type == pygame.KEYDOWN:
                        is_continue = 1

            self.__init__()


def main():
    game = Game()
    game.start()


main()
