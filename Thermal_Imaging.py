# -*- coding: utf-8 -*-
import random, sys, pygame, time, copy
from pygame.locals import *
import numpy as np
import cv2
from pylepton import Lepton
import Buttons
from pqRadio import *
import os
import thread

Debug = False

IMAGEWIDTH = 80 # width of the captured image, in pixels
IMAGEHEIGHT = 60 # height in pixels
SCALE = 4 # scale level for disp
WINDOWWIDTH = IMAGEWIDTH * SCALE + 160 # width of the program's window, in pixels
WINDOWHEIGHT = IMAGEHEIGHT * SCALE + 80 # height in pixels
IMAGEDISPLAYWIDTH = IMAGEWIDTH * SCALE # width of the display image, in pixels
IMAGEDISPLAYHEIGHT = IMAGEHEIGHT * SCALE # height in pixels

colormap_ironblack = [255, 255, 255, 253, 253, 253, 251, 251, 251, 249, 249, 249, 247, 247, 247, 245, 245, 245, 243, 243, 243, 241, 241, 241, 239, 239, 239, 237, 237, 237, 235, 235, 235, 233, 233, 233, 231, 231, 231, 229, 229, 229, 227, 227, 227, 225, 225, 225, 223, 223, 223, 221, 221, 221, 219, 219, 219, 217, 217, 217, 215, 215, 215, 213, 213, 213, 211, 211, 211, 209, 209, 209, 207, 207, 207, 205, 205, 205, 203, 203, 203, 201, 201, 201, 199, 199, 199, 197, 197, 197, 195, 195, 195, 193, 193, 193, 191, 191, 191, 189, 189, 189, 187, 187, 187, 185, 185, 185, 183, 183, 183, 181, 181, 181, 179, 179, 179, 177, 177, 177, 175, 175, 175, 173, 173, 173, 171, 171, 171, 169, 169, 169, 167, 167, 167, 165, 165, 165, 163, 163, 163, 161, 161, 161, 159, 159, 159, 157, 157, 157, 155, 155, 155, 153, 153, 153, 151, 151, 151, 149, 149, 149, 147, 147, 147, 145, 145, 145, 143, 143, 143, 141, 141, 141, 139, 139, 139, 137, 137, 137, 135, 135, 135, 133, 133, 133, 131, 131, 131, 129, 129, 129, 126, 126, 126, 124, 124, 124, 122, 122, 122, 120, 120, 120, 118, 118, 118, 116, 116, 116, 114, 114, 114, 112, 112, 112, 110, 110, 110, 108, 108, 108, 106, 106, 106, 104, 104, 104, 102, 102, 102, 100, 100, 100, 98, 98, 98, 96, 96, 96, 94, 94, 94, 92, 92, 92, 90, 90, 90, 88, 88, 88, 86, 86, 86, 84, 84, 84, 82, 82, 82, 80, 80, 80, 78, 78, 78, 76, 76, 76, 74, 74, 74, 72, 72, 72, 70, 70, 70, 68, 68, 68, 66, 66, 66, 64, 64, 64, 62, 62, 62, 60, 60, 60, 58, 58, 58, 56, 56, 56, 54, 54, 54, 52, 52, 52, 50, 50, 50, 48, 48, 48, 46, 46, 46, 44, 44, 44, 42, 42, 42, 40, 40, 40, 38, 38, 38, 36, 36, 36, 34, 34, 34, 32, 32, 32, 30, 30, 30, 28, 28, 28, 26, 26, 26, 24, 24, 24, 22, 22, 22, 20, 20, 20, 18, 18, 18, 16, 16, 16, 14, 14, 14, 12, 12, 12, 10, 10, 10, 8, 8, 8, 6, 6, 6, 4, 4, 4, 2, 2, 2, 0, 0, 0, 0, 0, 9, 2, 0, 16, 4, 0, 24, 6, 0, 31, 8, 0, 38, 10, 0, 45, 12, 0, 53, 14, 0, 60, 17, 0, 67, 19, 0, 74, 21, 0, 82, 23, 0, 89, 25, 0, 96, 27, 0, 103, 29, 0, 111, 31, 0, 118, 36, 0, 120, 41, 0, 121, 46, 0, 122, 51, 0, 123, 56, 0, 124, 61, 0, 125, 66, 0, 126, 71, 0, 127, 76, 1, 128, 81, 1, 129, 86, 1, 130, 91, 1, 131, 96, 1, 132, 101, 1, 133, 106, 1, 134, 111, 1, 135, 116, 1, 136, 121, 1, 136, 125, 2, 137, 130, 2, 137, 135, 3, 137, 139, 3, 138, 144, 3, 138, 149, 4, 138, 153, 4, 139, 158, 5, 139, 163, 5, 139, 167, 5, 140, 172, 6, 140, 177, 6, 140, 181, 7, 141, 186, 7, 141, 189, 10, 137, 191, 13, 132, 194, 16, 127, 196, 19, 121, 198, 22, 116, 200, 25, 111, 203, 28, 106, 205, 31, 101, 207, 34, 95, 209, 37, 90, 212, 40, 85, 214, 43, 80, 216, 46, 75, 218, 49, 69, 221, 52, 64, 223, 55, 59, 224, 57, 49, 225, 60, 47, 226, 64, 44, 227, 67, 42, 228, 71, 39, 229, 74, 37, 230, 78, 34, 231, 81, 32, 231, 85, 29, 232, 88, 27, 233, 92, 24, 234, 95, 22, 235, 99, 19, 236, 102, 17, 237, 106, 14, 238, 109, 12, 239, 112, 12, 240, 116, 12, 240, 119, 12, 241, 123, 12, 241, 127, 12, 242, 130, 12, 242, 134, 12, 243, 138, 12, 243, 141, 13, 244, 145, 13, 244, 149, 13, 245, 152, 13, 245, 156, 13, 246, 160, 13, 246, 163, 13, 247, 167, 13, 247, 171, 13, 248, 175, 14, 248, 178, 15, 249, 182, 16, 249, 185, 18, 250, 189, 19, 250, 192, 20, 251, 196, 21, 251, 199, 22, 252, 203, 23, 252, 206, 24, 253, 210, 25, 253, 213, 27, 254, 217, 28, 254, 220, 29, 255, 224, 30, 255, 227, 39, 255, 229, 53, 255, 231, 67, 255, 233, 81, 255, 234, 95, 255, 236, 109, 255, 238, 123, 255, 240, 137, 255, 242, 151, 255, 244, 165, 255, 246, 179, 255, 248, 193, 255, 249, 207, 255, 251, 221, 255, 253, 235, 255, 255, 24]
colormap_rainbow = [1, 3, 74, 0, 3, 74, 0, 3, 75, 0, 3, 75, 0, 3, 76, 0, 3, 76, 0, 3, 77, 0, 3, 79, 0, 3, 82, 0, 5, 85, 0, 7, 88, 0, 10, 91, 0, 14, 94, 0, 19, 98, 0, 22, 100, 0, 25, 103, 0, 28, 106, 0, 32, 109, 0, 35, 112, 0, 38, 116, 0, 40, 119, 0, 42, 123, 0, 45, 128, 0, 49, 133, 0, 50, 134, 0, 51, 136, 0, 52, 137, 0, 53, 139, 0, 54, 142, 0, 55, 144, 0, 56, 145, 0, 58, 149, 0, 61, 154, 0, 63, 156, 0, 65, 159, 0, 66, 161, 0, 68, 164, 0, 69, 167, 0, 71, 170, 0, 73, 174, 0, 75, 179, 0, 76, 181, 0, 78, 184, 0, 79, 187, 0, 80, 188, 0, 81, 190, 0, 84, 194, 0, 87, 198, 0, 88, 200, 0, 90, 203, 0, 92, 205, 0, 94, 207, 0, 94, 208, 0, 95, 209, 0, 96, 210, 0, 97, 211, 0, 99, 214, 0, 102, 217, 0, 103, 218, 0, 104, 219, 0, 105, 220, 0, 107, 221, 0, 109, 223, 0, 111, 223, 0, 113, 223, 0, 115, 222, 0, 117, 221, 0, 118, 220, 1, 120, 219, 1, 122, 217, 2, 124, 216, 2, 126, 214, 3, 129, 212, 3, 131, 207, 4, 132, 205, 4, 133, 202, 4, 134, 197, 5, 136, 192, 6, 138, 185, 7, 141, 178, 8, 142, 172, 10, 144, 166, 10, 144, 162, 11, 145, 158, 12, 146, 153, 13, 147, 149, 15, 149, 140, 17, 151, 132, 22, 153, 120, 25, 154, 115, 28, 156, 109, 34, 158, 101, 40, 160, 94, 45, 162, 86, 51, 164, 79, 59, 167, 69, 67, 171, 60, 72, 173, 54, 78, 175, 48, 83, 177, 43, 89, 179, 39, 93, 181, 35, 98, 183, 31, 105, 185, 26, 109, 187, 23, 113, 188, 21, 118, 189, 19, 123, 191, 17, 128, 193, 14, 134, 195, 12, 138, 196, 10, 142, 197, 8, 146, 198, 6, 151, 200, 5, 155, 201, 4, 160, 203, 3, 164, 204, 2, 169, 205, 2, 173, 206, 1, 175, 207, 1, 178, 207, 1, 184, 208, 0, 190, 210, 0, 193, 211, 0, 196, 212, 0, 199, 212, 0, 202, 213, 1, 207, 214, 2, 212, 215, 3, 215, 214, 3, 218, 214, 3, 220, 213, 3, 222, 213, 4, 224, 212, 4, 225, 212, 5, 226, 212, 5, 229, 211, 5, 232, 211, 6, 232, 211, 6, 233, 211, 6, 234, 210, 6, 235, 210, 7, 236, 209, 7, 237, 208, 8, 239, 206, 8, 241, 204, 9, 242, 203, 9, 244, 202, 10, 244, 201, 10, 245, 200, 10, 245, 199, 11, 246, 198, 11, 247, 197, 12, 248, 194, 13, 249, 191, 14, 250, 189, 14, 251, 187, 15, 251, 185, 16, 252, 183, 17, 252, 178, 18, 253, 174, 19, 253, 171, 19, 254, 168, 20, 254, 165, 21, 254, 164, 21, 255, 163, 22, 255, 161, 22, 255, 159, 23, 255, 157, 23, 255, 155, 24, 255, 149, 25, 255, 143, 27, 255, 139, 28, 255, 135, 30, 255, 131, 31, 255, 127, 32, 255, 118, 34, 255, 110, 36, 255, 104, 37, 255, 101, 38, 255, 99, 39, 255, 93, 40, 255, 88, 42, 254, 82, 43, 254, 77, 45, 254, 69, 47, 254, 62, 49, 253, 57, 50, 253, 53, 52, 252, 49, 53, 252, 45, 55, 251, 39, 57, 251, 33, 59, 251, 32, 60, 251, 31, 60, 251, 30, 61, 251, 29, 61, 251, 28, 62, 250, 27, 63, 250, 27, 65, 249, 26, 66, 249, 26, 68, 248, 25, 70, 248, 24, 73, 247, 24, 75, 247, 25, 77, 247, 25, 79, 247, 26, 81, 247, 32, 83, 247, 35, 85, 247, 38, 86, 247, 42, 88, 247, 46, 90, 247, 50, 92, 248, 55, 94, 248, 59, 96, 248, 64, 98, 248, 72, 101, 249, 81, 104, 249, 87, 106, 250, 93, 108, 250, 95, 109, 250, 98, 110, 250, 100, 111, 251, 101, 112, 251, 102, 113, 251, 109, 117, 252, 116, 121, 252, 121, 123, 253, 126, 126, 253, 130, 128, 254, 135, 131, 254, 139, 133, 254, 144, 136, 254, 151, 140, 255, 158, 144, 255, 163, 146, 255, 168, 149, 255, 173, 152, 255, 176, 153, 255, 178, 155, 255, 184, 160, 255, 191, 165, 255, 195, 168, 255, 199, 172, 255, 203, 175, 255, 207, 179, 255, 211, 182, 255, 216, 185, 255, 218, 190, 255, 220, 196, 255, 222, 200, 255, 225, 202, 255, 227, 204, 255, 230, 206, 255, 233, 208]
colormap_grayscale = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24, 25, 25, 25, 26, 26, 26, 27, 27, 27, 28, 28, 28, 29, 29, 29, 30, 30, 30, 31, 31, 31, 32, 32, 32, 33, 33, 33, 34, 34, 34, 35, 35, 35, 36, 36, 36, 37, 37, 37, 38, 38, 38, 39, 39, 39, 40, 40, 40, 41, 41, 41, 42, 42, 42, 43, 43, 43, 44, 44, 44, 45, 45, 45, 46, 46, 46, 47, 47, 47, 48, 48, 48, 49, 49, 49, 50, 50, 50, 51, 51, 51, 52, 52, 52, 53, 53, 53, 54, 54, 54, 55, 55, 55, 56, 56, 56, 57, 57, 57, 58, 58, 58, 59, 59, 59, 60, 60, 60, 61, 61, 61, 62, 62, 62, 63, 63, 63, 64, 64, 64, 65, 65, 65, 66, 66, 66, 67, 67, 67, 68, 68, 68, 69, 69, 69, 70, 70, 70, 71, 71, 71, 72, 72, 72, 73, 73, 73, 74, 74, 74, 75, 75, 75, 76, 76, 76, 77, 77, 77, 78, 78, 78, 79, 79, 79, 80, 80, 80, 81, 81, 81, 82, 82, 82, 83, 83, 83, 84, 84, 84, 85, 85, 85, 86, 86, 86, 87, 87, 87, 88, 88, 88, 89, 89, 89, 90, 90, 90, 91, 91, 91, 92, 92, 92, 93, 93, 93, 94, 94, 94, 95, 95, 95, 96, 96, 96, 97, 97, 97, 98, 98, 98, 99, 99, 99, 100, 100, 100, 101, 101, 101, 102, 102, 102, 103, 103, 103, 104, 104, 104, 105, 105, 105, 106, 106, 106, 107, 107, 107, 108, 108, 108, 109, 109, 109, 110, 110, 110, 111, 111, 111, 112, 112, 112, 113, 113, 113, 114, 114, 114, 115, 115, 115, 116, 116, 116, 117, 117, 117, 118, 118, 118, 119, 119, 119, 120, 120, 120, 121, 121, 121, 122, 122, 122, 123, 123, 123, 124, 124, 124, 125, 125, 125, 126, 126, 126, 127, 127, 127, 128, 128, 128, 129, 129, 129, 130, 130, 130, 131, 131, 131, 132, 132, 132, 133, 133, 133, 134, 134, 134, 135, 135, 135, 136, 136, 136, 137, 137, 137, 138, 138, 138, 139, 139, 139, 140, 140, 140, 141, 141, 141, 142, 142, 142, 143, 143, 143, 144, 144, 144, 145, 145, 145, 146, 146, 146, 147, 147, 147, 148, 148, 148, 149, 149, 149, 150, 150, 150, 151, 151, 151, 152, 152, 152, 153, 153, 153, 154, 154, 154, 155, 155, 155, 156, 156, 156, 157, 157, 157, 158, 158, 158, 159, 159, 159, 160, 160, 160, 161, 161, 161, 162, 162, 162, 163, 163, 163, 164, 164, 164, 165, 165, 165, 166, 166, 166, 167, 167, 167, 168, 168, 168, 169, 169, 169, 170, 170, 170, 171, 171, 171, 172, 172, 172, 173, 173, 173, 174, 174, 174, 175, 175, 175, 176, 176, 176, 177, 177, 177, 178, 178, 178, 179, 179, 179, 180, 180, 180, 181, 181, 181, 182, 182, 182, 183, 183, 183, 184, 184, 184, 185, 185, 185, 186, 186, 186, 187, 187, 187, 188, 188, 188, 189, 189, 189, 190, 190, 190, 191, 191, 191, 192, 192, 192, 193, 193, 193, 194, 194, 194, 195, 195, 195, 196, 196, 196, 197, 197, 197, 198, 198, 198, 199, 199, 199, 200, 200, 200, 201, 201, 201, 202, 202, 202, 203, 203, 203, 204, 204, 204, 205, 205, 205, 206, 206, 206, 207, 207, 207, 208, 208, 208, 209, 209, 209, 210, 210, 210, 211, 211, 211, 212, 212, 212, 213, 213, 213, 214, 214, 214, 215, 215, 215, 216, 216, 216, 217, 217, 217, 218, 218, 218, 219, 219, 219, 220, 220, 220, 221, 221, 221, 222, 222, 222, 223, 223, 223, 224, 224, 224, 225, 225, 225, 226, 226, 226, 227, 227, 227, 228, 228, 228, 229, 229, 229, 230, 230, 230, 231, 231, 231, 232, 232, 232, 233, 233, 233, 234, 234, 234, 235, 235, 235, 236, 236, 236, 237, 237, 237, 238, 238, 238, 239, 239, 239, 240, 240, 240, 241, 241, 241, 242, 242, 242, 243, 243, 243, 244, 244, 244, 245, 245, 245, 246, 246, 246, 247, 247, 247, 248, 248, 248, 249, 249, 249, 250, 250, 250, 251, 251, 251, 252, 252, 252, 253, 253, 253, 254, 254, 254, 255, 255, 255]

colorspace = [colormap_ironblack, colormap_rainbow, colormap_grayscale]
colorspace_select = 0
rect_instance = pygame.Rect(0, 0, 0, 0)

selected_images_rect = [[], [], []]
selected_images_flag = [False, False, False]

cropping_rect = rect_instance
cropping_rect_xy = []
cropping = False

selected_images_warning_rect = [[], [], []]
selected_images_warning_flag = [False, False, False]

selected_images_rect_max_width = 72
selected_images_rect_max_height = 72
selected_images_rect_min_width = 8
selected_images_rect_min_height = 8
selected_images_label = ['A', 'B', 'C']
selected_images_ref_value = [99999, 99999, 99999]

find_ref = [False, False, False]
OPTIONS = [0.2, 0.1, 0.05]
selected_images_ref_threhold = [OPTIONS[0], OPTIONS[0], OPTIONS[0]]
to_compare = [False, False, False]
to_compare_count = [0, 0, 0]
to_compare_count_threshold = 10
notified = [False, False, False]
warning = [True, True, True]

zeroDegreeV = 7200
minTemp = 40.2
minTempV = 7950
maxTemp = 240
maxTempV = 15300
TempDiff =  (maxTemp - minTemp) / (maxTempV - minTempV)
minDisTemp = ''
maxDisTemp = ''

#                 R    G    B
WHITE		= 	(255, 255, 255)
BLACK		= 	(  0,   0,   0)
GREEN		= 	(  0, 255,   0)
RED			=	(255, 	0,	 0)

SCREENCOLOR = BLACK
CROPRECTLINECOLOR = WHITE
CROPINGRECTLINECOLOR = GREEN
TEXTCOLOR = WHITE
WARNINGRECTLINECOLOR = RED

#Initialize pygame
pygame.init()

class Thermal_Imaging:
	
	def __init__(self):
		self.main()
		

	def display(self):
		self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
		pygame.display.set_caption('FLIR Lepton')
		pygame.font.init()
		self.font = pygame.font.Font('freesansbold.ttf', 16)
		self.ButtonRainbow = Buttons.Button()
		self.ButtonIronblack = Buttons.Button()
		self.ButtonGery = Buttons.Button()
		self.Exit = Buttons.Button()
		self.rs = [RadioGroup(), RadioGroup(), RadioGroup()]
		self.r1 = [None, None, None]
		self.r2 = [None, None, None]
		self.r3 = [None, None, None]
		for i in range(0, 3):
			self.r1[i] = Radio(self, [440,21 + 82 * i], '20%', True)
			self.r2[i] = Radio(self, [440,41 + 82 * i], '10%', False)
			self.r3[i] = Radio(self, [440,61 + 82 * i], '5%', False)
			self.rs[i].add(self.r1[i])
			self.rs[i].add(self.r2[i])
			self.rs[i].add(self.r3[i])
		
	
	def update_display(self):		
		global find_ref
		
		self.screen.fill(SCREENCOLOR)
		
		image = self.capture_image()
		frame = pygame.transform.smoothscale(self.get_frame(image), (IMAGEDISPLAYWIDTH, IMAGEDISPLAYHEIGHT))
		self.screen.blit(frame, (0, 0))
		if cropping:
			pygame.draw.rect(self.screen, CROPINGRECTLINECOLOR, cropping_rect, 2)
		selected_images_display_height = 0
		for i in range(0, 3):
			if selected_images_flag[i]:
				#draw selected rectangle
				pygame.draw.rect(self.screen, CROPRECTLINECOLOR, selected_images_rect[i], 2)
				if selected_images_rect[i].x > 16:
					#draw label for elected rectangle on left
					self.drawText(selected_images_label[i], selected_images_rect[i].x - 16, selected_images_rect[i].y + selected_images_rect[i].h / 2 - 8)
				else:
					#draw label for elected rectangle on right
					self.drawText(selected_images_label[i], selected_images_rect[i].x + selected_images_rect[i].w + 6, selected_images_rect[i].y + selected_images_rect[i].h / 2 - 8)
				frame = pygame.transform.smoothscale(self.get_cropped_frame(image, i), (selected_images_rect[i].w, selected_images_rect[i].h))
				offset = (selected_images_rect_max_height - selected_images_rect[i].h) / 2
				#draw cropped image
				self.screen.blit(frame, (350, 5 + (selected_images_rect_max_height + 10) * i + offset))		
				self.drawText(selected_images_label[i], 330, (selected_images_rect_max_height + 10) * i + selected_images_rect[i].h / 2 - 8 + 5 + offset)
				self.r1[i].draw()
				self.r2[i].draw()
				self.r3[i].draw()
				#draw warning rectangle
				if selected_images_warning_flag[i]:
					if warning[i]:
						rect_temp = pygame.Rect(350 - 2, 5 + (selected_images_rect_max_height + 10) * i + offset - 2, selected_images_rect[i].width + 4, selected_images_rect[i].height + 4)
						pygame.draw.rect(self.screen, WARNINGRECTLINECOLOR, rect_temp, 2)
					warning[i] = not warning[i]
		self.drawText('Min : ' + minDisTemp, 335, 255)
		self.drawText('Max : ' + maxDisTemp, 335, 285)
			
		#Parameters:surface,color,x,y,length,height,width,text,text_color
		self.ButtonIronblack.create_button(self.screen, (254,63,30), 10, 265, 60, 30, 18, "Ironblack", (255,255,255))
		self.ButtonRainbow.create_button(self.screen, (30,30,254), 80, 265, 60, 30, 18, "Rainbow", (255,255,255))
		self.ButtonGery.create_button(self.screen, (65,65,65), 150, 265, 60, 30, 18, "Greyscale", (255,255,255))
		self.Exit.create_button(self.screen, (87,160,70), 245, 265, 60, 30, 20, "Exit", (255,255,255))
		
		pygame.display.update()
		
		
	def drawText(self, text, x, y, color=TEXTCOLOR):
		text = self.font.render(text, 1, color)
		self.screen.blit(text, (x, y))
		
	
	def checkForEvent(self):
		for event in pygame.event.get(): # event handling loop
			global colorspace_select, selected_images_rect, selected_images_flag, cropping, cropping_rect, cropping_rect_xy, find_ref
			
			if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
					
			elif event.type == MOUSEBUTTONUP:
				for i in range(0, 3):
					res =  self.rs[i].check(pygame.mouse.get_pos())
					if res != -1:
						selected_images_ref_threhold[i] = OPTIONS[res]
						to_compare_count[i] = 0
				
				if cropping:
					if cropping_rect.w < 0:
						cropping_rect.w = -cropping_rect.w
						cropping_rect.x = cropping_rect.x - cropping_rect.w
					if cropping_rect.h < 0:
						cropping_rect.h = -cropping_rect.h
						cropping_rect.y = cropping_rect.y - cropping_rect.h
						
					if cropping_rect.w > selected_images_rect_min_width and cropping_rect.h > selected_images_rect_min_height:
						for i in range(0, 3):
							if not selected_images_flag[i]:
								selected_images_rect[i] = cropping_rect
								selected_images_flag[i] = True
								find_ref[i] = True	
								break
					
					cropping = False
					
			elif event.type == MOUSEBUTTONDOWN:
				if self.Exit.pressed(pygame.mouse.get_pos()):
					pygame.quit()
					sys.exit()
				elif self.ButtonIronblack.pressed(pygame.mouse.get_pos()):
					colorspace_select = 0
				elif self.ButtonRainbow.pressed(pygame.mouse.get_pos()):
					colorspace_select = 1
				elif self.ButtonGery.pressed(pygame.mouse.get_pos()):
					colorspace_select = 2
				else:
					if not cropping:
						img_rect = pygame.Rect(0, 0, IMAGEDISPLAYWIDTH, IMAGEDISPLAYHEIGHT)
						if img_rect.collidepoint(pygame.mouse.get_pos()):
						
							for i in range(0, 3):
								if selected_images_flag[i]:
									if selected_images_rect[i].collidepoint(pygame.mouse.get_pos()):
										selected_images_flag[i] = False
										to_compare[i] = False
										return
										
							x = pygame.mouse.get_pos()[0]
							y = pygame.mouse.get_pos()[1]
							
							cropping_rect = pygame.Rect(x, y, 3, 3)
							cropping_rect_xy = [x, y]
							cropping = True
							
			if event.type == pygame.MOUSEMOTION:				
				if cropping:
					x = pygame.mouse.get_pos()[0]
					y = pygame.mouse.get_pos()[1]
					
					if x > IMAGEDISPLAYWIDTH:
						x = IMAGEDISPLAYWIDTH
					if y > IMAGEDISPLAYHEIGHT:
						y = IMAGEDISPLAYHEIGHT
						
					xy = cropping_rect_xy
					width = x - xy[0]
					height = y - xy[1]
					
					if abs(width) > selected_images_rect_max_width:
						if width > 0:
							width = selected_images_rect_max_width
						else:
							width = -selected_images_rect_max_width
					if abs(height) > selected_images_rect_max_height:
						if height > 0:
							height = selected_images_rect_max_height
						else:
							height = -selected_images_rect_max_height
						
					cropping_rect = pygame.Rect(xy[0], xy[1], width, height)
				
				
	def capture_image(self):
		global minDisTemp, maxDisTemp
		
		with Lepton('/dev/spidev0.1') as l:
			a,_ = l.capture()
		a = np.rot90(a) 

		for i in range(0, 3):
			if to_compare[i]:
				avg = self.get_avg_value(a, i)
				if Debug:
					print "%s %d %f" % (selected_images_label[i], avg, selected_images_ref_value[i])
					print "%d %s" % (to_compare_count[i], notified[i])
				if not notified[i]:
					if avg >= (1 + selected_images_ref_threhold[i]) * selected_images_ref_value[i]:
						to_compare_count[i] += 1
					else:
						to_compare_count[i] = 0
				else:
					if avg < (1 + selected_images_ref_threhold[i]) * selected_images_ref_value[i]:
						to_compare_count[i] -= 1
					else:
						to_compare_count[i] = to_compare_count_threshold
					if to_compare_count[i] == 0:
						notified[i] = False
						selected_images_warning_flag[i] = False
				if to_compare_count[i] == to_compare_count_threshold and not notified[i]:
					notification_text = selected_images_label[i] + ":\nref: " + str(selected_images_ref_value[i]) + "\nthreshold: " + str(selected_images_ref_threhold[i]) + "\ncurrent: " + str(avg)
					#TO-DO Please implement your own notification.
					# for contact in self.email_list:
						# thread.start_new_thread(self.push_notification_email, (contact, "Warning", notification_text))
					# for contact in self.sms_list:
						# contact = int(contact)
						# thread.start_new_thread(self.push_notification_sms, (contact, notification_text))
					notified[i] = True
					selected_images_warning_flag[i] = True
			if find_ref[i]:
				selected_images_ref_value[i] = self.get_avg_value(a, i)
				find_ref[i] = False
				to_compare[i] = True
				if Debug:
					print "%s %f" % (selected_images_label[i], selected_images_ref_value[i])
			
		img = np.zeros((IMAGEWIDTH, IMAGEHEIGHT, 3), np.uint8)
		minValue = 65535;
		maxValue = 0;
		
		for i in range(0, IMAGEWIDTH):
			for j in range(0, IMAGEHEIGHT):
				value = a[i][j][0]
				if value > maxValue:
					maxValue = value
				if value < minValue:
					minValue = value
					
		minDisTemp = self.getTempture(minValue) + ' deg C'
		maxDisTemp = self.getTempture(maxValue) + ' deg C'
					
		diff = maxValue - minValue
		scale = 255.0 / diff
							
		for i in range(0, IMAGEWIDTH):
			for j in range(0, IMAGEHEIGHT):
				value = int((a[i][j][0] - minValue) * scale)
				img[i][j] = (colorspace[colorspace_select][3 * value + 0], colorspace[colorspace_select][3 * value + 1], colorspace[colorspace_select][3 * value + 2])
		
		return img
		
		
	def get_frame(self, img):
		#img = np.rot90(img)
		return pygame.surfarray.make_surface(img)
		
		
	def get_cropped_frame(self, img, index):
		rect = selected_images_rect[index]
		#img = np.rot90(img)
		cropped_img = img[(rect.x / SCALE + 1):(rect.x / SCALE + rect.w / SCALE), (rect.y / SCALE + 1):(rect.y / SCALE + rect.h / SCALE)]	
		
		return pygame.surfarray.make_surface(cropped_img)
		
	
	def getTempture(self, value):
		return '{0:.2f}'.format((value - zeroDegreeV) * TempDiff)
		
		
	def get_avg_value(self, img, index):
		rect = selected_images_rect[index]
		w = rect.w / SCALE
		h = rect.h / SCALE
		#img = np.rot90(img)
		img = img[(rect.x / SCALE + 1):(rect.x / SCALE + w), (rect.y / SCALE + 1):(rect.y / SCALE + h)]
		w -= 1
		h -= 1
		
		return np.sum(img) / w / h - zeroDegreeV
		
		
	# def load_notification_list(self):
		# self.load_email_list()
		# self.load_sms_list()
		
		
	# def load_email_list(self):
		# self.email_list = []
		# file = open('emaillist.txt', 'r')
		# for line in file:
			# self.email_list.append(line)
		
	# def load_sms_list(self):
		# self.sms_list = []
		# file = open('smslist.txt', 'r')
		# for line in file:
			# self.sms_list.append(line)
		
		
	# def push_notification_email(self, email_to, email_subject, email_body):
		# os.system('python ./sendmail.py -t "' + email_to + '" -s "' + str(email_subject) + '" -b "' + str(email_body) + '"')
		
		
	# def push_notification_sms(self, phone_number, phone_text):
		# os.system('python ./PySmsGateway.py' + ' -p ' + str(phone_number) + ' -m ' + '"' + phone_text + '"')
		
		
	def main(self):
		self.display()
		# self.load_notification_list()
		while True:
			self.update_display()
			self.checkForEvent()
			

if __name__ == '__main__':
    obj = Thermal_Imaging()
