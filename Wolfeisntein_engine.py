# -*- coding: utf-8 -*-
import pygame, math, sys
from pygame.locals import *

Window_size = (600,600)
Window = pygame.display.set_mode(Window_size)

Display_size = (600,600)
Display = pygame.Surface(Display_size)


mapa = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
block_size = (1,1)
velocity_ratio = 5

class Cam():
    def __init__(self, pos, dirt, plane):
        self.pos = pos
        self.dirt = dirt
        self.plane = plane
        self.momentum = [self.dirt[0]/velocity_ratio,self.dirt[1]/velocity_ratio]
        
    def Rotate(self, angle):
        self.dirt[0] = self.dirt[0] * math.cos(angle) - self.dirt[1] * math.sin(angle)
        self.dirt[1] = self.dirt[0] * math.sin(angle) + self.dirt[1] * math.cos(angle)
        
        self.plane[0] = self.plane[0] * math.cos(angle) - self.plane[1] * math.sin(angle)
        self.plane[1] = self.plane[0] * math.sin(angle) + self.plane[1] * math.cos(angle)

        self.momentum = [self.dirt[0]/velocity_ratio,self.dirt[1]/velocity_ratio]
    
    def Increment_direct(self):
       self.pos[0] += self.momentum[0]
       self.pos[1] += self.momentum[1]
        
    def Maintain_module(self, falt):
        self.dirt[0] *= (1+falt)
        self.dirt[1] *= (1+falt)

    def Can_i(self):
        sumx = self.pos[0] + self.dirt[0]
        sumy = self.pos[1] + self.dirt[1]

        if(sumx >= len(mapa)-3 or sumy >= len(mapa[0])-3):
            return False
        return True
    
qtd_light = 300

hit_cima = 0
hit_baixo = 1
modulo_direcao = 1 

tamanho_padrao = 1000

angle_rotation = 1 * math.pi/180

d_know = 0
vertical = 1
horizontal = 2

red = (0,0,255)
blue = (0,255,0)
        
def Module(vector):
    #calcular modulo de vetor tri e bi dimensional
    soma = 0
    for component in vector:
        soma += math.pow(component, 2)
    return math.sqrt(soma)
        
def Check_hit(delta, camera, check_esq, check_down, ray):
    mapx = int(camera.pos[0]/block_size[0])
    mapy = int(camera.pos[1]/block_size[1])
    tamanho = 0; color = 0
    if(check_esq):
        stepx = -1
        side_x = (camera.pos[0] - mapx*block_size[0]) * delta[0]
    else:
        stepx = 1
        side_x = (mapx*block_size[0] + block_size[0] - camera.pos[0]) * delta[0]

    if(check_down):
        stepy = 1
        side_y = (mapy*block_size[1] + 1 - camera.pos[1]) * delta[1]
    else:
        stepy = -1
        side_y = (camera.pos[1] - mapy*block_size[1]) * delta[1]

    hit = 0
    side = d_know

    while(hit == 0):
        if(side_x < side_y):
            mapx += stepx
            side_x += delta[0]
            side = vertical

        else:
            mapy += stepy
            side_y += delta[1]
            side = horizontal
        if(mapa[mapx][mapy] == 1):
            hit = 1

    if(side == vertical):
        perpWallDist = (mapx*block_size[0] - camera.pos[0] + (1 - stepx) / 2) / ray[0]
        color = red
    else:
        perpWallDist = (mapy*block_size[1] - camera.pos[1] + (1 - stepy) / 2) / ray[1]
        color = blue

    tamanho = tamanho_padrao/perpWallDist 
    return [side_x, side_y, color], tamanho
                         
def Dda_algorithm(camera, Display):
    lista_tamanho = []
    lista_2d = []; color = 0; lista_color = []
    for light in range(qtd_light):
        camera_x = (2*light/qtd_light) - 1

        ray_x = camera.dirt[0] + camera.plane[0]*camera_x
        ray_y = camera.dirt[1] + camera.plane[1]*camera_x

        if(not(ray_x == 0 or ray_y == 0)):
            delta_x = abs(1/ray_x)
            delta_y = abs(1/ray_y)

        check_esq = False
        check_down = True

        if(ray_x < 0):
            check_esq = True
        if(ray_y < 0):
            check_down = False

        control_2d, tamanho = Check_hit([delta_x, delta_y], camera, check_esq, check_down, [ray_x,ray_y])
        if(not tamanho == 0):
            lista_tamanho.append([light, tamanho, control_2d[2]])
            lista_2d.append(control_2d)

    Render(lista_tamanho, Display)

ratio = 64

def Render_2d(cam, lista, Display):
    d2_space = pygame.Surface((len(mapa[0])*block_size[0]*ratio,len(mapa)*block_size[1]*ratio))
    surf = pygame.Surface([block_size[0]*ratio,block_size[1]*ratio])
    surf.fill((255,255,255))
    y = 0
    for linha in mapa:
        x = 0
        for coluna in linha:
            if(coluna == 1):
                d2_space.blit(surf, (x * block_size[0] * ratio, y * block_size[1] * ratio))    
            x+=1
        y+=1
    transformed_pos = [cam.pos[1]*ratio,cam.pos[0]*ratio]
    for light in lista:
        pygame.draw.line(d2_space, (255,255,255), transformed_pos, [light[1]*ratio,light[0]*ratio])
    
    d2_space = pygame.transform.scale(d2_space, (150,150))
    Display.blit(d2_space, (0,0))
    
def Render(lista_control, Display):
    x=0
    for light in lista_control:
        largura = Display_size[0]/qtd_light; altura = int(light[1])
        x = largura * light[0]; y = Display_size[1]/2 - light[1]/2
        surf = pygame.Surface((largura, altura))
        surf.fill(light[2])
        Display.blit(surf, (x,y))
        x+=1

def Get_event(cam):
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
    pressed = pygame.key.get_pressed()
    
    if(pressed[K_UP] and cam.Can_i()):
        cam.Increment_direct()
    
    if(pressed[K_LEFT]):
        cam.Rotate(angle_rotation)
    if(pressed[K_RIGHT]):
        cam.Rotate(-angle_rotation)   

def Main():
    Is_running = True
    cam = Cam([12,12],[-1, 0],[0,0.66])
    frame_clock = pygame.time.Clock()
    while(Is_running):
        Get_event(cam)
        Display.fill((0,0,0))
        
        Dda_algorithm(cam, Display)
        
        surf = pygame.transform.scale(Display, Window_size)
        Window.blit(surf, (0,0))
        pygame.display.update()
        frame_clock.tick(60)

if __name__ == "__main__":
    Main()
