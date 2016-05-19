#!/usr/bin/env python
#####################################################################
# Authors: Christine Hwang (ch458) and Tania Tocalini (tvt9)
# Date:    5-18-2016
# Lab:     On-Campus Lost & Found
# Summary: Displays coordinates for lost objects
#####################################################################

import pygame, Buttons
import sys
import os
import time
import location_me

# OS settings
# os.putenv("SDL_FBDEV", "/dev/fb1")
# os.putenv("SDL_VIDEODRIVER", "fbcon")
# os.putenv("SDL_MOUSEDRV", "TSLIB")
# os.putenv("SDL_MOUSEDEV", "/dev/input/touchscreen")

############################################################
# Pygame Settings
############################################################


pygame.init() # initialize pygame

# settings
size = width,height = 320,240
y_padding = 35
black = 0,0,0
red = (255, 0, 0)
green = (12, 182, 0)
B = location_me.building
F = location_me.floor
  
# set up display
screen  = pygame.display.set_mode(size, 0, 32)

# Update the text on screen stating the coordinates of the lost object
def write_text():
  deftext = "Your lost item is in " + B + " "
  font = pygame.font.SysFont("Calibri", 20)
  ftext = font.render(deftext, 1, (255, 255, 255))
  textpos = ftext.get_rect()
  textpos.centerx = 0.5*width
  textpos.centery = 0.45*height
  screen.blit(ftext, textpos) 
  
  coords = "on floor " + F 
  font = pygame.font.SysFont("Calibri", 20)
  ftext = font.render(coords, 1, (255, 255, 255))
  textpos = ftext.get_rect()
  textpos.centerx = 0.5*width
  textpos.centery = 0.55*height
  screen.blit(ftext, textpos) 
  
############################################################
# Main Function
############################################################
    
def main():
  
  # game objects
  panic_b = Buttons.Button()
  ok_b  = Buttons.Button()

  # state 
  is_pressed = False

  while(True):
    B = location_me.building
    F = location_me.floor
    time.sleep(0.02) # sleep for 0.02s

    screen.fill(black) # draw black background


    # Create the buttons
    if (is_pressed):
      ok_b.create_button(screen, 
        green, 0.35*width, 0.87*height, 125, 25, 0, "I'm OK", (255,255,255))
      write_text()
    else:
      panic_b.create_button(screen, 
        red, 0.35*width, 0.45*height, 125, 25, 0, "PANIC!", (255,255,255))
  
    # Check for button presses
    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
        sys.exit()
      elif (event.type == pygame.MOUSEBUTTONDOWN):
        if (panic_b.pressed(pygame.mouse.get_pos())):
          is_pressed = True
        elif (ok_b.pressed(pygame.mouse.get_pos())):
          is_pressed = False

    pygame.display.flip() # flush display to output              


main()
