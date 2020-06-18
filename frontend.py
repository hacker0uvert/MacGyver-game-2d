#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Frontend window management and textures manipulation module
"""

import os

import pygame as pg

import backend as bckd
import settings as stg

RESOURCES_DIR = stg.RESOURCES_DIR
LABYRINTH = bckd.Labyrinth()

class Window:
    """ Physical window management
    """

    def __init__(self):
        """ Window class initiator
        """
        self.resources_dir = RESOURCES_DIR
        self.icon_file = stg.ICON_FILE
        self.window_resolution = stg.WINDOW_RESOLUTION
        self.window_caption = stg.WINDOW_CAPTION

    def load(self):
        """ Window loading function
        """
        pg.display.init()
        self.screen = pg.display.set_mode(self.window_resolution)
        pg.display.set_caption(self.window_caption)
        self.icon()

    def icon(self):
        """ Window icon's loading function
        """
        with open(os.path.join(self.resources_dir, self.icon_file), 'r') as file:
            ico = pg.image.load(file)
        pg.display.set_icon(ico)

    def background_init(self, surfaces):
        """ Walls and corridors background textures initialisation.
        In the json file, 'wall' is corresponding to 'W' in the labyrinth_matrix.
        'c' stands for 'corridor'
        """
        x_iterator, y_iterator = 0, 0
        while y_iterator in range(LABYRINTH.grid_len):
            while x_iterator in range(LABYRINTH.grid_len):
                if LABYRINTH.labyrinth_matrix[y_iterator][x_iterator] == 'W':
                    self.screen.blit(surfaces['wall'], (x_iterator*LABYRINTH.box_px_len, y_iterator*LABYRINTH.box_px_len))
                else:
                    self.screen.blit(surfaces['corridor'], (x_iterator*LABYRINTH.box_px_len, y_iterator*LABYRINTH.box_px_len))
                x_iterator += 1
            y_iterator += 1
            x_iterator = 0
        pg.display.flip()


class Texture:
    """ Textures manipulation
    """

    def __init__(self):
        """ Class initiator
        """
        self.surfaces = {}
        self.script_dir = stg.SCRIPT_DIR
        self.surfaces_json_dir = stg.SURFACES_JSON_DIR
        self.surfaces_file = stg.SURFACES_FILE
        self.resources_dir = RESOURCES_DIR
        self.surfaces_json = self.surfaces_dict()

    def surface_load(self, img_file):
        """ Texture surface image loading function
        """
        with open(os.path.join(self.resources_dir, img_file), 'r') as file:
            texture_surface = pg.image.load(file).convert()
        return texture_surface

    def crop_surface(self, texture_surface, coordinates):
        """ Texture surface crop function
        """
        x_length = coordinates[2] - coordinates[0]
        y_length = coordinates[3] - coordinates[1]
        # pylint doesn't understand pg.Surface call thus returns an arguments error
        # pylint: disable-msg=too-many-function-args
        # creation of a new Surface with the cropped texture's horizontal and vertical dimensions
        cropped_texture_surface = pg.Surface((x_length, y_length))
        # pylint: enable-msg=too-many-function-args
        # adding the cropped texture to the newly created Surface
        cropped_texture_surface.blit(texture_surface, (0, 0), coordinates)
        # for a window's definition of 600*600 and a 15*15 matrix:
        # converting the Surface to a 40*40 pixels rectangle, so as to correspond
        # to window's 600*600 pixels definition: 15*15 texture rectangles matrix
        cropped_texture_surface = pg.transform.scale(cropped_texture_surface, (LABYRINTH.box_px_len, LABYRINTH.box_px_len))
        return cropped_texture_surface

    def get_surface(self, img_file, coordinates):
        """ Texture surface image file load and crop
        """
        texture_surface = self.surface_load(img_file)
        cropped_texture_surface = self.crop_surface(texture_surface, coordinates)
        return cropped_texture_surface

    def load_surfaces_json(self):
        """ Surfaces dictionnary loading function, from json file
        """
        surfaces_json = stg.json_load(self.surfaces_json_dir, self.surfaces_file)
        return surfaces_json

    def surfaces_dict(self):
        """ Surfaces dictionnary definition function.
        Values are defined from surfaces_json dict.
        """
        surfaces_json = self.load_surfaces_json()
        for i in surfaces_json:
            surface = self.get_surface(surfaces_json[i][0], surfaces_json[i][1])
            self.surfaces[i] = surface
        return surfaces_json

def main():
    """ Window is loaded on script execution.
    Surfaces are then printed on script for test purposes
    """
    display = Window()
    display.load()
    surfaces = Texture()
    i = 0
    while i < len(surfaces.surfaces):
        display.screen.blit(surfaces.surfaces[list(surfaces.surfaces.keys())[i]], (i*LABYRINTH.box_px_len, 0))
        i += 1
    pg.display.flip()

if __name__ == '__main__':
    main()