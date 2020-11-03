import pygame, math, sys
from pygame.locals import *

Window_size = (600,600)
Window = pygame.display.set_mode(Window_size)

Display_size = (400,400)
Display = pygame.Surface(Display_size)

mapa = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Cam():
    def __init__(self, pos, dirt, plane):
        self.pos = pos
        self.dirt = dirt
        self.plane = plane
        
    def Rotate(self, angle):
        self.dirt[0] = self.dirt[0] * math.cos(angle) - self.dirt[1] * math.sin(angle)
        self.dirt[1] = self.dirt[0] * math.sin(angle) + self.dirt[1] * math.sin(angle)
        
        self.plane[0] = self.plane[0] * math.cos(angle) - self.plane[1] * math.sin(angle)
        self.plane[1] = self.plane[0] * math.sin(angle) + self.plane[1] * math.sin(angle)
    
    def Increment_direct(self):
        self.pos[0] += self.dirt[0]
        self.pos[1] += self.dirt[1]
    
qtd_light = 360 

hit_cima = 0
hit_baixo = 1 

tamanho_padrao = 300
distanica_project = 10

def Render(lista_control, Display):
    for light in lista_control:
        largura = Display_size[0]/qtd_light; altura = light[1]
        x = largura * light; y = Display_size[1]/2 - light[1]/2
        surf = pygame.Surface((largura, altura))
        surf.fill((255,255,255))
        Display.blit(surf, (x,y))        
        
def Render(camera, Display):
    deltadistx = 1; deltadisty = 1
    sidedistx = 1; sidedisty = 1
    lista_control = []
    for light in range(1, qtd_light+1):
        number_atual = 2*light/qtd_light -1
        raydirx = camera.dirt[0] + camera.plane[0] * number_atual
        raydiry = camera.dirt[1] + camera.plane[1] * number_atual
        
        mapx = int(camera.pos[0])
        mapy = int(camera.pos[1])
        
        if(not raydirx == 0):
            deltadistx = abs(1/raydirx)
        if(not raydiry == 0):
            deltadisty = abs(1/raydiry)
            
        hit = 0
        side = hit_baixo
             
        if(raydirx < 0):
            stepx = -1
            sidedistx = (camera.pos[0] - mapx) * deltadistx
        else:
            stepx = 1
            sidedistx = (mapx + 1 - camera.pos[0]) * deltadistx
         
        if(raydiry < 0):
            stepy = -1
            sidedisty = (camera.pos[1] - mapy) * deltadisty
        else:
            stepy = 1
            sidedisty = (mapx + 1 - camera.pos[1]) * deltadisty
            
        while(hit == 0):
            if(sidedistx < sidedisty):
                sidedistx += deltadistx
                mapx += stepx
                side = hit_cima
            else:
                sidedisty += deltadisty
                mapy += stepy
                side = hit_baixo  
            if(mapa[mapx][mapy] > 0):
                hit = 1
        
        if(side == hit_cima):
            perpwalldist = (mapx - camera.pos[0] + (1 - stepx)/2)/raydirx
        else:
            perpwalldist = (mapy - camera.pos[1] + (1 - stepy)/2)/raydiry
        
        if(hit == 1):
            if(not perpwalldist == 0):
                tamanho = tamanho_padrao/perpwalldist * distanica_project
                lista_control.append([light, tamanho]) 
            
    Render(lista_control, Display) 

angle_rotation = 10 * math.pi/180
    
def Get_event(cam):
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
    pressed = pygame.key.get_pressed()
    
    if(pressed[K_UP]):
        cam.Increment_direct()
    
    if(pressed[K_LEFT]):
        cam.Rotate(angle_rotation)
    if(pressed[K_RIGHT]):
        cam.Rotate(-angle_rotation)   

def Main():
    Is_running = True
    cam = Cam([10,10],[-1,0],[0,0.66])
    while(Is_running):
        Display.fill((0,0,0))
        
        Render(cam, Display)
        surf = pygame.transform.scale(Display, Window_size)
        Window.blit(surf, (0,0))
        pygame.display.update()

if __name__ == "__main__":
    Main()