
#Éllen Oliveira Silva Neves e Maria Gabriela Siqueira Tavares
#2º ano - Técnico em Informática Integrado ao Ensino Médio

import os
import sys
import pygame
from random import randint

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'					# Imagem centralizada na tela

size = width, height = (500, 708) 						# Tamanho da janela
screen = pygame.display.set_mode(size)	# Cria a Janela
pygame.mouse.set_visible(False)							# Esconde o cursor do mouse durante o jogo
black = 0, 0, 0											# Cor preta no sistema RGB (Red/Green/Blue)

'''
Classe "Nave"

A primeira classe eh muito simples, herdada da classe Sprite (nativa do PyGame). Um sprite eh um elemento grafico do jogo, e possui 2 propriedades importantes: image e rect. 
Image e' a imagem em si, carregada do disco (os principais formatos sao suportados, tais como JPG, GIF, PNG e BMP) e rect representa o retangulo virtual que contem a imagem 
(imagine um retangulo circunscrito a imagem). Alterando as propriedades centerx, centery, top, bottom, left e right de rect podemos posicionar o sprite onde quisermos na tela.
'''

class Nave(pygame.sprite.Sprite):
	def __init__(self): 								# __init__ eh o construtor em Python
		pygame.sprite.Sprite.__init__(self)				# chamando o construtor da superclasse
		self.image = pygame.image.load('images/cat.png') # Define qual imagem serah desenhada na tela
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect()				# Cria um retangulo (invisivel) em torno da imagem
		self.rect.centerx = width/2						# Coord x inicial da imagem
		self.rect.centery = height-35					# Coord y inicial da imagem

'''
Classe "Invasor"

A segunda classe eh bem similar. A unica diferenca eh no metodo update, que faz com que o invasor "passeie" pela tela. Alem disso, caso o invasor atinja um canto da tela, ele muda de direcao.

O metodo "update" eh executado a cada loop do jogo para alterar a posicao na qual o objeto deve ser desenhado. Vale lembrar que no nosso caso a origem do eixo esta no canto superior esquerdo da tela.
'''

class Invasor(pygame.sprite.Sprite):
	speed = (0,0)
	def __init__(self, images):
		self.images = images
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(images[0], (100, 100)) 
		self.rect = self.image.get_rect()
		self.rect.centerx = 100#randint(50,width-50)
		self.rect.centery = 100#randint(35,height/2-5)
		self.speed = [randint(-4,4),randint(-2,2)]		# a velocidade de movimento do invasor eh aleatoria
		# se speed=(4, -2), por exemplo, entao o objeto eh movido 4 unidades na direcao x e -2 unidades na direcao y.

	def update(self, tempo):
		self.rect.move_ip(self.speed)					# muda a posicao do objeto de acordo com o atributo. 

		if tempo==0: # de tempos em tempos (a cada 40 ciclos), a velocidade do objeto vai mudar
			self.speed[0] = randint(-4,4)
			self.speed[1] = randint(-2,2)

		if self.rect.right > width or self.rect.left < 0: 
			# se o objeto chegar no canto esquerdo ou direito, sua velocidade no eixo x eh invertida.
			self.speed[0] = -self.speed[0] 
		if self.rect.top < 0 or self.rect.bottom > 2*(height/4):
			# caso o objeto atinja o topo ou o 2/3 do fundo da tela, sua velocidade no eixo y eh invertida.
			self.speed[1] = -self.speed[1]

		if tempo < 20: 
			self.image = pygame.transform.scale(self.images[0], (100, 100)) 
		else: 
			self.image = pygame.transform.scale(self.images[1], (100, 100)) 
		
'''
Classe "Tiro"

Como na classe Invasor, ha o construtor e o metodo update.
'''

class Tiro(pygame.sprite.Sprite):
	def __init__(self, images):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(images[0], (30, 30))
		self.rect = self.image.get_rect()
		self.rect.centery = height-70
		self.speed = [0,0]

	def update(self,objetos,tiros, images):
		self.rect.move_ip(self.speed)
		
		if tiros%2 == 0:
			self.image = pygame.transform.scale(images[1], (30,30))
		else:
			self.image = pygame.transform.scale(images[0], (30,30))

		if self.rect.top < 0: 
			# se o tiro atingir o topo da tela, ele desaparece e volta a ficar parado em sua posicao inicial
			self.rect.centery = height-70				# posicao inicial
			self.speed = [0,0]							# velocidade parada
			objetos.remove(self) 						# removido da lista de objetos que serao exibidos (para sumir da tela)
			return tiros+1 								# se o usuario errou um tiro, ele tem uma chance a menos

		return tiros # se o tiro ainda nao saiu da tela, o usuario ainda tem chance de acerta-lo.
		
'''
Classe "Fundo"

Apenas desenha uma imagem no centro da tela.
'''

class Fundo(pygame.sprite.Sprite):
	def __init__(self,img):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(img)
		self.rect = self.image.get_rect()
		self.rect.centerx = width/2
		self.rect.centery = height/2


def main(args):

	# Criando a lista com as duas imagens do invasor que serao usadas para desenha-lo
	imagens_invasor1 = [pygame.image.load('images/jhope_flower_png.png'), pygame.image.load('images/hosekflower.png')] 
	imagens_invasor2 = [pygame.image.load('images/jin_1.png'), pygame.image.load('images/jin_2.png')]
	imagens_invasor3 = [pygame.image.load('images/jk_1.png'), pygame.image.load('images/jk_2.png')]
	imagens_invasor4 = [pygame.image.load('images/sg_1.png'), pygame.image.load('images/sg_2.png')]
	imagens_invasor5 = [pygame.image.load('images/kt_1.png'), pygame.image.load('images/kt_2.png')]
	imagens_invasor6 = [pygame.image.load('images/jm_1.png'), pygame.image.load('images/jm_2.png')]
	imagens_invasor7 = [pygame.image.load('images/nj_1.png'), pygame.image.load('images/nj_2.png')]

	imagens_invasores = [ imagens_invasor1, imagens_invasor2, imagens_invasor3, imagens_invasor4, imagens_invasor5, imagens_invasor6, imagens_invasor7 ]
	n_invasores = 1

	imagens_tiros = [pygame.image.load('images/musicnote1.png'), pygame.image.load('images/musicnote2.png')]
	

	# Criando um objeto da classe Invasor
	invasores = []
	
	for i in range(n_invasores):
		invasores.append( Invasor(imagens_invasores[n_invasores-1 + i]) )

	# Criando um objeto da classe Nave
	n = Nave()

	# Criando um objeto da classe Tiro, inicialmente parado
	t = Tiro(imagens_tiros)
	
	f = Fundo('images/city_at_sunset_0.gif')

	# Lista com os objetos a serem desenhados. A principio, o tiro nao eh desenhado.
	objetos = [f, n] 

	# Define o titulo da janela
	pygame.display.set_caption('Bangtan Sonyeondan - A invasão') 
	clock = pygame.time.Clock()
	# pygame.key.set_repeat(1,1)

	acertou = False 			# indica se o usuario ja acertou um tiro no invasor
	tiros = 0					# quantidade de tiros gastos pelo usuario
	tempo = 0					# contador para controlar o tempo de mudar a imagem do invasor



	if os.path.exists('audio/idol_bts_audio.mp3'):
		pygame.mixer.music.load('audio/idol_bts_audio.mp3')
		pygame.mixer.music.play()
		pygame.mixer.music.set_volume(1)

		clock = pygame.time.Clock()
		clock.tick(10)

	else:
		print('Dj Juninho Portugal is busy right now')

	while n_invasores < 8 and tiros < 8:
		clock.tick(120)			# garante que o programa nao vai rodar a mais que 120fps
		tempo = (tempo+1)%40	# o tempo varia sempre entre 0 e 39 (portanto, sao 40 ciclos)



		''' O jogo tambem precisa detectar quando o jogador apertar as setas Q ou ESC (para terminar o jogo),
		quando o jogador movimentar o mouse e quando o jogador apertar algum botao do mouse. 
		Isso eh feito atraves do seguinte trecho de codigo: '''
	
		# O centro da nave no eixo x eh sempre a posicao x de onde estiver o mouse
		n.rect.centerx = pygame.mouse.get_pos()[0] 

		for event in pygame.event.get():
			# Cada evento do teclado ou mouse eh tratado aqui
			if event.type == pygame.MOUSEBUTTONDOWN and not t in objetos: 
				# se o jogador tiver disparado um tiro, e nenhum tiro jah estiver aparecendo na tela
				t.speed = [0,-8]							# define a velocidade y do tiro
				t.rect.centerx = pygame.mouse.get_pos()[0]	# posiciona o tiro no eixo x onde ele foi disparado
				objetos.append(t) 							# inclui o tiro na lista de objetos a serem desenhados
				

			elif event.type == pygame.KEYDOWN:
				# Se alguma tecla for apertada no teclado
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					#Veja todas as teclas em http://www.pygame.org/docs/ref/key.html
					print('Bye')
					sys.exit()

			elif event.type == pygame.QUIT:
				print('Bye')
				sys.exit()

		''' Agora vamos atualizar as posicoes do tiro e do invasor a cada loop do jogo,
		utilizando o metodo update criado em suas classes.'''

		for invasor in invasores: invasor.update(tempo)

		tiros = t.update(objetos, tiros, imagens_tiros) 					# atualiza a posicao do tiro

		''' Agora vamos detectar se o tiro colidiu com a nave. Nesse caso, o jogo acaba e o usuario venceu. 
		Existem varias formas de detectar colisoes de sprites. A mais simples eh: 
		sprite.rect.colliderect(sprite.rect)
		Este metodo retorna "True" caso os retangulos dos 2 sprites estejam se sobrepondo (ou seja, colidindo).'''

		for invasor in invasores:
			if t.rect.colliderect(invasor.rect): 				# verifica se o retangulo do tiro coincide com o do invasor
				invasores.remove(invasor)
				t.rect.centery = height-70
				t.speed = [0,0]
				objetos.remove(t)
				
				
		if invasores == []:
			n_invasores = n_invasores * 2
			if n_invasores == 8: break

			for i in range(n_invasores):
				invasores.append( Invasor(imagens_invasores[n_invasores-1 + i]) )


		''' Por fim, o programa desenha todos os objetos na tela a cada loop do jogo. 
		Apos calculadas as novas posicoes de cada um, a forma mais eficiente de atualizarmos a tela eh preenche-la 
		com o fundo preto, para que os objetos antigos (da iteracao anterior) sejam apagados: isso eh muito mais 
		simples do que ter que apaga-los um a um. O metodo blit "renderiza" cada objeto na tela, e quando todos 
		estiverem prontos o metodo flip efetivamente atualiza a tela para o jogador.'''

		screen.fill(black) 									# desenha um fundo preto por cima do que ja existia
		for objeto in objetos: 
			screen.blit(objeto.image, objeto.rect)			# desenha cada objeto da lista de objetos a serem desenhados
		for invasor in invasores: 
			screen.blit(invasor.image, invasor.rect)			# desenha cada objeto da lista de objetos a serem desenhados

		pygame.display.flip()


	'''
	O CODIGO A PARTIR DAQUI SO SERA EXECUTADO QUANDO UM TIRO ACERTAR O INVASOR, OU QUANDO ACABAREM OS TIROS
	'''

	pygame.mixer.music.stop()
	if tiros < 8: f = Fundo('images/youwin.jpg')
	else:
		 f = Fundo('images/gameover.jpg')

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print('Bye')
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				print('Bye')
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q or event.key == pygame.K_RETURN:
					print('Bye')
					sys.exit()
	
		screen.blit(f.image, f.rect)
		pygame.display.flip()
	


if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))


