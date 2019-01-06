import sys
import math

def pythagoras(a, b):
    return math.sqrt(a * a + b * b)


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
        self.num_sites = 0
        self.gold = 0
        self.touched_site = 0
        self.queen_coords = 0

    def add_unit(self, unit: Unit):
        self.units.append(unit)

    def update_units(self):
        self.units = []
        self.num_units = int(input())
        for i in range(self.num_units):
            x, y, owner, unit_type, health = [int(j) for j in input().split()]
            self.add_unit(Unit(x, y, owner, unit_type, health))
            if owner == 0 and unit_type == -1:
                self.queen_coords = [x, y]

    def update_turn(self):
        gold, touched_site = [int(i) for i in input().split()]
        self.gold = gold
        self.touched_site = touched_site

    def get_safe_position(self):
        x, y = self.queen_coords
        safe_x = 0 if x < 1920 / 2 else 1920
        safe_y = 0 if y < 1000 / 2 else 1000
        return (safe_x, safe_y)

class Site:
    def __init__(self, site_id, x, y, radius):
        self.site_id = site_id
        self.x = x
        self.y = y
        self.radius = radius
        self.structure_type = -1
        self.owner = -1

    def update(self, structure_type, owner):  # updating data about site
        self.structure_type = structure_type
        self.owner = owner

    def check_barracks(self):
        return self.owner == 0 and self.structure_type == 2

    def can_build(self):
        return self.owner == -1 and self.structure_type == -1

    def calculate_distance(self, x, y):
        return pythagoras(self.x - x, self.y -y)


class Sites:
    def __init__(self):
        self.sites = []
        self.num_sites = int(input())
        self.barracks = -1

        for i in range(self.num_sites):
            site_id, x, y, radius = [int(j) for j in input().split()]
            self.add_site(site_id, x, y, radius)

    def add_site(self, site_id, x, y, radius):
        self.sites.append(Site(site_id, x, y, radius))

    def update_sites(self):
        for i in range(self.num_sites):
            site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2  = [int(j) for j in input().split()]
            self.sites[site_id].update(structure_type, owner)
            if self.sites[site_id].check_barracks():
                self.barracks = site_id

    def lowest_distance(self, coords):
        safe_x, safe_y = coords
        free_sites = [site for site in self.sites if site.can_build()]
        return min(free_sites, key=lambda site: site.calculate_distance(safe_x, safe_y)).site_id

class Game:
    def __init__(self):
        self.sites = Sites()
        self.units = Units()
        self.turn = 0
        self.play_game()

    def update_game(self):
        self.units.update_turn()
        self.sites.update_sites()
        self.units.update_units()
        self.turn += 1

    def play_game(self):                                       
        while True:
            self.update_game()
            if self.turn == 1:
                self.first_turn()
            self.generate_action()

    def first_turn(self):
        self.safe_position = self.units.get_safe_position()
        self.barracks_planned = self.sites.lowest_distance(self.safe_position)

    def generate_action(self):                            
        if self.sites.barracks != self.barracks_planned:
            print("BUILD " + str(self.barracks_planned) + " BARRACKS-KNIGHT")
            print("TRAIN")
        else:
            print("WAIT")
            print("TRAIN " + str(self.sites.barracks))

# GAME ==========================================================================
game = Game()
