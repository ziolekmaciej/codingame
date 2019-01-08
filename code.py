#
#  Created by Maciej Ziółkowski on 28.12.2018
#

import sys
import math

barracks = "barracks"
tower = "tower"
mine = "mine"


def pythagoras(a, b):
    return math.sqrt(a * a + b * b)


def print_debug(text):
    print(text, file=sys.stderr)


def build(site_id, building_type):
    build_str = "BUILD "
    if building_type == "barracks":
        building_type = "BARRACKS-KNIGHT"
    elif building_type == "tower":
        building_type = "TOWER"
    elif building_type == "mine":
        building_type = "MINE"
    print(build_str + str(site_id) + " " + building_type)


def train(site_id):
    train_str = "TRAIN"
    if site_id == -1:
        print(train_str)
    else:
        site_id = str(site_id)
        print(train_str + " " + site_id)


def move(coords):
    x, y = coords
    print("MOVE " + str(x) + " " + str(y))


class Unit:
    def __init__(self, x, y, owner, unit_type, health):
        self.x = x
        self.y = y
        self.owner = owner
        self.unit_type = unit_type
        self.health = health


class Units:
    def __init__(self):
        self.units = []
        self.num_units = 0
        self.gold = 0
        self.touched_site = 0
        self.queen = Queen()

    def add_unit(self, unit: Unit):                             # Add unit to units list
        self.units.append(unit)

    def update_units(self):                                     # Update units in game
        self.units = []                                         # Getting queen info
        self.num_units = int(input())
        for i in range(self.num_units):
            x, y, owner, unit_type, health = [int(j) for j in input().split()]
            self.add_unit(Unit(x, y, owner, unit_type, health))
            if owner == 0 and unit_type == -1:
                self.queen.update_data([x, y, health])

    def update_turn(self):                                      # Updating gold and touching site
        gold, touched_site = [int(i) for i in input().split()]
        self.gold = gold
        self.touched_site = touched_site


class Queen:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.health = 0

    def update_data(self, data):                                # Updating coorginates of queen
        self.x, self.y, self.health = data

    def get_coords(self):                                       # Get queen coords
        return (self.x, self.y)                                 # return tuple of queen coords

    def get_health(self):                                       # Get queen health
        return self.health                                      # return queen's health

    def get_safe_position(self):                                # Get highest distance from enemy for my queen
        safe_x = 0 if self.x < 1920 / 2 else 1920               # returns tuple of coords for corner
        safe_y = 0 if self.y < 1000 / 2 else 1000
        return (safe_x, safe_y)


class Site:
    def __init__(self, site_id, x, y, radius):
        self.site_id = site_id
        self.x = x
        self.y = y
        self.radius = radius
        self.structure_type = -1
        self.owner = -1
        self.param_1 = -1
        self.param_2 = -1
        self.max_mine_size = 0
        self.gold = 0

    def check_barracks(self):                                   # Checks if are barracks on this id
        return self.owner == 0 and self.structure_type == 2

    def check_tower(self):                                      # Checks if is tower on this id
        return self.owner == 0 and self.structure_type == 1 and self.param_2 >= 440

    def check_mine(self):                                       # Checks if is mine on this id
        if self.gold == 0 or self.gold == -1:
            return True
        return self.owner == 0 and self.structure_type == 0 and self.param_1 == self.max_mine_size

    def can_build(self):                                        # Checks if you can build on this site
        return self.owner == -1 and self.structure_type == -1   # return True if you can

    def check_half(self, x):
        result = self.x > 900 if x else self.x < 1000
        return result

    def update(self, gold, max_mine_size, structure_type, owner, param_1, param_2):  # updating data about site
        self.structure_type = structure_type
        self.owner = owner
        self.param_1 = param_1
        self.param_2 = param_2
        self.gold = gold
        self.max_mine_size = max_mine_size

    def calculate_distance(self, x, y):                         # Calculate distance from queen to site
        return pythagoras(self.x - x, self.y -y)                # return distance


class Sites:
    def __init__(self):                                         # Get data from game about sites
        self.sites = []                                         # adding sites to list and sorty by id
        self.num_sites = int(input())
        self.safe_position = 0

        self.focus = -1
        self.barracks_planned = -1
        self.barracks = -1
        self.mines = []
        self.mines_planned = []
        self.towers = []
        self.towers_planned = []

        for i in range(self.num_sites):
            site_id, x, y, radius = [int(j) for j in input().split()]
            self.add_site(site_id, x, y, radius)

    def add_site(self, site_id, x, y, radius):                  # Adding site to sites list
        self.sites.append(Site(site_id, x, y, radius))

    def lowest_distance(self, coords, type):                    # Find nearest free site from coords
        x, y = coords                                           # return site_id or -1 if not exist
        if type == mine or type == barracks:
            free_sites = [site for site in self.sites if site.can_build()]
        elif type == tower:
            safe_x, safe_y = self.safe_position
            free_sites = [site for site in self.sites if site.can_build() and site.check_half(safe_x)]
        result = min(free_sites, key=lambda site: site.calculate_distance(x, y)).site_id if bool(free_sites) else -1
        return result

    def update_sites(self):                                      # Update data about sites from game
        self.mines = []
        self.towers = []
        self.barracks = -1
        for i in range(self.num_sites):
            site_id, gold, max_mine_size, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
            self.sites[site_id].update(gold, max_mine_size, structure_type, owner, param_1, param_2)
            if self.sites[site_id].check_mine():
                self.mines.append(site_id)
                continue
            if self.sites[site_id].check_tower():
                self.towers.append(site_id)
                continue
            if self.sites[site_id].check_barracks():
                self.barracks = site_id

    def get_sites_for_buildings(self, coords):
        x, y = coords
        self.sites.sort(key=lambda site: site.calculate_distance(x, y))
        self.barracks_planned = self.sites[0].site_id
        [self.mines_planned.append(item.site_id) for item in self.sites[1:4]]
        [self.towers_planned.append(item.site_id) for item in self.sites[4:7]]
        self.sites.sort(key=lambda site: site.site_id)

    def are_mines(self):
        for mine_planned in self.mines_planned:
            if mine_planned not in self.mines:
                self.focus = mine_planned
                return mine_planned
        self.focus = -1
        return -1

    def are_towers(self):
        for tower_planned in self.towers_planned:
            if tower_planned not in self.towers:
                self.focus = tower_planned
                return tower_planned
        self.focus = -1
        return -1

    def is_barrack(self):
        return self.barracks_planned == self.barracks


class Game:
    def __init__(self):
        self.sites = Sites()
        self.units = Units()
        self.turn = 0
        self.play_game()

    def update_game(self):                                      # Updating data from game
        self.units.update_turn()
        self.sites.update_sites()
        self.units.update_units()
        self.turn += 1

    def play_game(self):                                        # Game loop
        while True:
            self.update_game()
            if self.turn == 1:
                self.first_turn()
            self.generate_queen_action()
            self.generate_training()

    def first_turn(self):
        self.sites.safe_position = self.units.queen.get_safe_position()
        self.sites.get_sites_for_buildings(self.sites.safe_position)

    def generate_queen_action(self):                            # Generate Queen move
        if not self.sites.is_barrack():
            build(self.sites.barracks_planned, barracks)
        elif self.sites.are_mines() != -1:
            build(self.sites.focus, mine)
        elif self.sites.are_towers() != -1:
            build(self.sites.focus, tower)
        else:
            move(self.sites.safe_position)

    def generate_training(self):                                # Generate training command
            if self.sites.barracks == -1:
                train(-1)
            else:
                train(self.sites.barracks)


# GAME ==========================================================================
game = Game()
