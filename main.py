import pygame
import os
import random
import time
pygame.init()


# TODO: topun plakalardan sekmesini ve sağ ve sola çarpınca yanmasını sağla (belkican barıda koyanilirsin)

#----------------VALUES--------------
WIN_WIDTH = 900
WIN_HEIGHT = 500
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 120
BALL_RAD = 25
LINE_WIDTH = 4
FPS = 30


#--------------SOUNDS----------------
PING = pygame.mixer.Sound("./Sounds/pong.wav")
MUSIC = pygame.mixer.music.load("./Sounds/cyberpong3.wav")
END_SOUND = pygame.mixer.Sound("./Sounds/samurai.wav")
pygame.mixer.music.play(-1)


#--------------WINDOW----------------
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Cyberpong 2077")


#-------------TEXT------------------
label = pygame.font.SysFont(None, 76)
point1 = point2 = pygame.font.SysFont(None, 76)


#---------------FUNCTIONS------------
def draw(player_position1, player_position2, BALL_WIDTH,
	BALL_HEIGHT, renk, bg_renk, text_color, line_renk, player1_point, player2_point):
	#-------------OBJECTS-----------------
	player1 = pygame.Rect(WIN_WIDTH - 2 * PLAYER_WIDTH, player_position1, PLAYER_WIDTH, PLAYER_HEIGHT)
	player2 = pygame.Rect(0 + PLAYER_WIDTH, player_position2, PLAYER_WIDTH, PLAYER_HEIGHT)
	ball = render_ball(BALL_WIDTH, BALL_HEIGHT)
	line = pygame.Rect(WIN_WIDTH//2 - LINE_WIDTH//2, 0, LINE_WIDTH, WIN_HEIGHT)
	WIN.fill(bg_renk)
	point1_text = point1.render(player1_point, True, renk)
	point2_text = point2.render(player2_point, True, renk)
	text = label.render("Made By EGE", True, text_color)
	WIN.blit(text, (WIN_WIDTH//3, WIN_HEIGHT//2))
	WIN.blit(point1_text, (76, 20))
	WIN.blit(point2_text, (WIN_WIDTH - 76, 20))
	pygame.draw.rect(WIN, renk, player1)
	pygame.draw.rect(WIN, renk, player2)
	pygame.draw.rect(WIN, line_renk, line)
	pygame.draw.ellipse(WIN, renk, ball)

	pygame.display.update()


def render_ball(ball_x, ball_y):
	ball = pygame.Rect(ball_x, ball_y, BALL_RAD, BALL_RAD)
	return ball


def main():
	#----------------COLORS---------------
	WHITE = (255, 255, 255)
	GRAY = (200, 200, 200)
	DARKBLUE = (38, 70, 83)
	NEON_GREEN = (6, 250, 1)
	DARK = (0, 0, 0)
	#--------------PLAYERS-------------
	PLAYER_POSITION1 = PLAYER_POSITION2 = WIN_HEIGHT//2 - PLAYER_HEIGHT//2
	PLAYER_VEL = 8
	PLAYER1_POINT = PLAYER2_POINT = 0
	#----------------BALL--------------
	BALL_WIDTH = WIN_WIDTH//2 - BALL_RAD//2
	BALL_HEIGHT = random.randint(0, WIN_HEIGHT - BALL_RAD)
	BALL_VEL_X = 4
	BALL_VEL_Y = 4
	run = True
	puan_oyuncu1 = 0
	puan_oyuncu2 = 0

	clock = pygame.time.Clock()

	last = 0
	last_color_timer = 0

	bg_bolor = DARKBLUE
	color = GRAY
	text_color = DARKBLUE
	line_renk = GRAY

	while run:
		PLAYER1_POINT = str(PLAYER1_POINT)
		PLAYER2_POINT = str(PLAYER2_POINT)
		clock.tick(FPS)
		now = pygame.time.get_ticks()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		# TOPU X EKSENINDA HAREKET ETTIRME
		if (WIN_WIDTH - BALL_RAD > BALL_WIDTH + BALL_RAD or PLAYER_WIDTH < BALL_WIDTH):
			BALL_WIDTH += BALL_VEL_X

		# TOPUN PLAKALARDAN SEKMESI
		if (WIN_WIDTH - BALL_RAD <= BALL_WIDTH + BALL_RAD or 2 * PLAYER_WIDTH >= BALL_WIDTH) and (
			PLAYER_POSITION1 <= BALL_HEIGHT <= PLAYER_POSITION1 + PLAYER_HEIGHT or
			PLAYER_POSITION2 <= BALL_HEIGHT <= PLAYER_POSITION2 + PLAYER_HEIGHT):
			BALL_VEL_X = -BALL_VEL_X
			BALL_WIDTH += BALL_VEL_X


		if (0 >= BALL_WIDTH or WIN_WIDTH <= BALL_WIDTH + BALL_RAD):
			if 0 >= BALL_WIDTH:
				PLAYER2_POINT = int(PLAYER2_POINT) + 5
			if WIN_WIDTH <= BALL_WIDTH + BALL_RAD:
				PLAYER1_POINT = int(PLAYER1_POINT) + 5

			PLAYER1_POINT = str(PLAYER1_POINT)
			PLAYER2_POINT = str(PLAYER2_POINT)

			pygame.mixer.music.stop()
			END_SOUND.play()
			time.sleep(7)
			last = now
			last_color_timer = now
			BALL_VEL_Y = BALL_VEL_X = 4
			PLAYER_VEL = 8
			BALL_WIDTH = WIN_WIDTH//2 - BALL_RAD//2
			BALL_HEIGHT = random.randint(0, WIN_HEIGHT - BALL_RAD)
			color = GRAY
			bg_bolor = DARKBLUE
			text_color = DARKBLUE
			line_renk = GRAY
			pygame.mixer.music.play()


		# TOPUN Y EKSENINDE HAREKETI
		if BALL_HEIGHT + BALL_RAD < WIN_HEIGHT and BALL_HEIGHT > 0:
			BALL_HEIGHT += BALL_VEL_Y

		# TOPUN YUKARI ASAGIDAN SEKMESI
		if BALL_HEIGHT + BALL_RAD >= WIN_HEIGHT or BALL_HEIGHT <= 0:
			BALL_VEL_Y = -BALL_VEL_Y
			BALL_HEIGHT += BALL_VEL_Y


		if now - last > 5000:
			last = now
			PLAYER_VEL += 2

			if BALL_VEL_X > 0:
				BALL_VEL_X += 2
			if BALL_VEL_X < 0:
				BALL_VEL_X -= 2

			if BALL_VEL_Y > 0:
				BALL_VEL_Y += 2
			if BALL_VEL_Y < 0:
				BALL_VEL_Y -= 2

		if now - last_color_timer > 21200:
			bg_bolor = DARK
			color = NEON_GREEN
			text_color = NEON_GREEN
			line_renk = DARK


		key_pressed = pygame.key.get_pressed()
		if key_pressed[pygame.K_UP] and PLAYER_POSITION1 > 10:
			PLAYER_POSITION1 -= PLAYER_VEL
		if key_pressed[pygame.K_DOWN] and PLAYER_POSITION1+PLAYER_HEIGHT <= WIN_HEIGHT - 10:
			PLAYER_POSITION1 += PLAYER_VEL

		if key_pressed[pygame.K_w] and PLAYER_POSITION2 > 10:
			PLAYER_POSITION2 -= PLAYER_VEL
		if key_pressed[pygame.K_s] and PLAYER_POSITION2+PLAYER_HEIGHT <= WIN_HEIGHT - 10:
			PLAYER_POSITION2 += PLAYER_VEL

		draw(PLAYER_POSITION1, PLAYER_POSITION2, BALL_WIDTH, BALL_HEIGHT,
			color, bg_bolor, text_color, line_renk, PLAYER1_POINT, PLAYER2_POINT)


	pygame.quit()


if __name__ == "__main__":
	main()
