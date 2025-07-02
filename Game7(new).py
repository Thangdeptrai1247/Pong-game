import pygame
import sys

pygame.init()

WIDTH, HEIGHT = (800, 600)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 6
    
    def move(self, up=False):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed 

    def draw(self,screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y ,30, 30)
        self.speed_x = 4
        self.speed_y = 4

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speed_x *= -1
    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Pong game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('None', 40)

        self.left_paddle = Paddle(10, HEIGHT//2 - 50)
        self.right_paddle = Paddle(WIDTH - 20, HEIGHT//2 - 50)
        self.ball = Ball(WIDTH//2 - 15, HEIGHT//2 - 15)

        self.left_score = 0
        self.right_score = 0

        self.winner = None

    def handle_input(self) :
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.left_paddle.rect.top > 0:
            self.left_paddle.move(up=True)
        if keys[pygame.K_s] and self.left_paddle.rect.bottom < HEIGHT:
            self.left_paddle.move(up=False)

        if keys[pygame.K_UP] and self.right_paddle.rect.top > 0:
            self.right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and self.right_paddle.rect.bottom < HEIGHT:
            self.right_paddle.move(up=False)

    def check_collision(self):
        if self.ball.rect.colliderect(self.left_paddle.rect) and self.ball.speed_x < 0:
            self.ball.rect.left = self.left_paddle.rect.right
            self.ball.speed_x *= -1

        if self.ball.rect.colliderect(self.right_paddle.rect) and self.ball.speed_x > 0:
            self.ball.rect.right = self.right_paddle.rect.left
            self.ball.speed_x *= -1
    
    def update_score(self):
        if self.ball.rect.right < 0:
            self.right_score += 1
            self.winner = 'right'
            self.ball.reset()

        elif self.ball.rect.left > WIDTH:
            self.left_score += 1
            self.winner = 'left'
            self.ball.reset()

    def draw(self):
        self.screen.fill(BLACK)

        pygame.draw.aaline(self.screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        left_text = self.font.render(f'{self.left_score}', True, WHITE)
        right_text = self.font.render(f'{self.right_score}', True, WHITE)
        self.screen.blit(left_text,(WIDTH//4, 20))
        self.screen.blit(right_text, (WIDTH*3//4, 20))

        restart_text = self.font.render('Welcome to game Pong', True, WHITE)
        self.screen.blit(restart_text,(WIDTH // 2 - restart_text.get_width()// 2, HEIGHT - 40))

        if self.winner:
            win_msg = 'Player on the right wins! Press R to continue playing' if self.winner == 'left' else'Player'
            ' on the left wins! Press R to continue playing'
            win_text = self.font.render(win_msg, True, WHITE)
            self.screen.blit(win_text,(WIDTH // 4 - restart_text.get_width() // 2, HEIGHT // 2 - 30))

        pygame.display.flip()

    def reset_game(self):
        self.left_score = 0 
        self.right_score = 0 
        self.winner = None
        self.ball.reset()
        self.left_paddle.rect.centery = HEIGHT // 2
        self.right_paddle.rect.centery = HEIGHT // 2

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
            if not self.winner:
                self.handle_input()
                self.ball.move()
                self.check_collision()
                self.update_score()
                self.draw()
                self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()

