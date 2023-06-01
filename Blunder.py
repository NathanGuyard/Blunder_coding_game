import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

#J'import List, Optional, et Tuple pour rajouter de la précision dans mon code en spéficiant le format de mes variables 
from typing import List, Optional, Tuple

#Je stock les directions / Obstacle présent sur la carte 
#Je stock ma position sous le forme tuple en précisant le format que je veux stocké "int"
Position = Tuple[int, int]

STRONG_WALL_SYMBOL = "#"
WEAK_WALL_SYMBOL = "X"
START_SYMBOL = "@"
FINISH_SYMBOL = "$"
SOUTH_SYMBOL = "S"
EAST_SYMBOL = "E"
NORTH_SYMBOL = "N"
WEST_SYMBOL = "W"
BEER_SYMBOL = "B"
INVERTER_SYMBOL = "I"
TELEPORTER_SYMBOL = "T"
EMPTY_SYMBOL = " "

SOUTH = "SOUTH"
EAST = "EAST"
NORTH = "NORTH"
WEST = "WEST"


#Je définie ma classe Cell pour initié et reset 
class Cell:
    #J'initie ma class et lui passe en argument self,symbol et je précise que symbol sera toujours en "str"
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.reset()

    def reset(self):
        #Je définie mes différents state et je rajoute en option grace à l'import de Typing une chaine de caractères "str"
        self.prev_blunder_reverse_state: Optional[str] = None
        self.prev_blunder_break_mode_state: Optional[str] = None
        self.prev_blunder_direction: Optional[str] = None

#Je crée ma classe blunder avec l'ensemble de c'est priorité 
class Blunder:
    def __init__(self):
        self.priorities: List[str] = [SOUTH, EAST, NORTH, WEST]
        self.reverse_state = False
        self.break_mode_state = False
        self.direction = SOUTH # Répond partiellement à la question 1 
        self.x = 0
        self.y = 0
        self.moves: List[str] = []
#Je crée une function qui permet le déplacement de Blunder 
    def move(self):
        if self.direction == SOUTH:
            self.y += 1
        elif self.direction == EAST:
            self.x += 1
        elif self.direction == NORTH:
            self.y -= 1
        elif self.direction == WEST:
            self.x -= 1
        self.moves.append(self.direction)

#Je crée ma classe game avec l'ensemble de c'est priorité 
class Game:
    def __init__(self):
        self.grid: List[List[Cell]] = []
        self.grid_height = 0
        self.grid_width = 0
        self.blunder = Blunder()
        self.teleporter1: Optional[Position] = None
        self.teleporter2: Optional[Position] = None
        self.infinite_loop = False

    @property

    def current_symbol(self) -> str:
        # Récupère le symbole de la case actuelle, où se trouve blunder
        return self.grid[self.blunder.y][self.blunder.x].symbol

    def reset_grid_state(self):
        # Boucle sur les hauteurs de la grille
        for y in range(self.grid_height):
            # Boucle sur les largeurs de la grille
            for x in range(self.grid_width):
                # Réinitialise l'état de la case à la position (x, y)
                self.grid[y][x].reset()
    
    #Répond à la question 4 
    def is_valid_move(self, direction: str) -> bool:
        if direction == SOUTH:  # Vérifie si la direction est vers le SOUTH
            return self.is_valid_position(self.blunder.x, self.blunder.y + 1)  # Vérifie si la position vers le SOUTH est valide
        elif direction == EAST:  # Vérifie si la direction est vers EAST
            return self.is_valid_position(self.blunder.x + 1, self.blunder.y)  # Vérifie si la position vers EAST est valide
        elif direction == NORTH:  # Vérifie si la direction est vers le NORTH
            return self.is_valid_position(self.blunder.x, self.blunder.y - 1)  # Vérifie si la position vers le NORTH est valide
        else:  # WEST (OUEST) Sinon vers WEST 
            return self.is_valid_position(self.blunder.x - 1, self.blunder.y)  # Vérifie si la position vers WEST est valide


    def is_valid_position(self, x: int, y: int) -> bool:
        # Vérifie que la position est dans la grille est bonne
        if x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height:
            return False
        
        # Vérifie que la case n'est pas un mur fort
        cell = self.grid[y][x]
        if cell.symbol == STRONG_WALL_SYMBOL:
            return False
        
        # Vérifie que la case n'est pas un mur faible si le mode casseur est désactivé
        if cell.symbol == WEAK_WALL_SYMBOL and not self.blunder.break_mode_state:
            return False
        
        # Si toutes les conditions sont remplies, la position est valide
        return True

    #Répond à la question 5,6,7,8 
    def update_blunder_state(self):
        # Vérifie le symbole de la case actuelle pour mettre à jour l'état du blunder
        if self.current_symbol == SOUTH_SYMBOL:
            # Si le symbole est SOUTH_SYMBOL, met à jour la direction du blunder vers le SUD
            self.blunder.direction = SOUTH

        elif self.current_symbol == EAST_SYMBOL:
            # Si le symbole est EAST_SYMBOL, met à jour la direction du blunder vers l'EST
            self.blunder.direction = EAST

        elif self.current_symbol == NORTH_SYMBOL:
            # Si le symbole est NORTH_SYMBOL, met à jour la direction du blunder vers le NORD
            self.blunder.direction = NORTH

        elif self.current_symbol == WEST_SYMBOL:
            # Si le symbole est WEST_SYMBOL, met à jour la direction du blunder vers l'OUEST
            self.blunder.direction = WEST

        elif self.current_symbol == BEER_SYMBOL:
            # Si le symbole est BEER_SYMBOL, inverse l'état du mode pause du blunder
            self.blunder.break_mode_state = not self.blunder.break_mode_state

        elif self.current_symbol == INVERTER_SYMBOL:
            # Si le symbole est INVERTER_SYMBOL, inverse l'état de marche avant/marche arrière du blunder
            self.blunder.reverse_state = not self.blunder.reverse_state
            # Inverse l'ordre des priorités pour refléter le nouvel état
            self.blunder.priorities.reverse()

        elif self.current_symbol == TELEPORTER_SYMBOL:
            # Si le symbole est TELEPORTER_SYMBOL, effectue un téléport vers une autre position

            if (self.blunder.x, self.blunder.y) == self.teleporter1:
                # Si le blunder se trouve à la position du teleporter1, le téléporte vers le teleporter2

                self.blunder.x, self.blunder.y = self.teleporter2
                
            elif (self.blunder.x, self.blunder.y) == self.teleporter2:
                # Si le blunder se trouve à la position du teleporter2, le téléporte vers le teleporter1

                self.blunder.x, self.blunder.y = self.teleporter1

    def move_blunder(self):
    # Met à jour l'état du personnage principal (Blunder)
        self.update_blunder_state()

        # Vérifie si le déplacement dans la direction actuelle est valide
        if not self.is_valid_move(self.blunder.direction):
            # Si ce n'est pas le cas, essaie chaque direction de priorité pour trouver un déplacement valide
            for direction in self.blunder.priorities:
                if self.is_valid_move(direction):
                    # Si une direction de priorité est valide, change la direction de Blunder et effectue le déplacement
                    self.blunder.direction = direction
                    self.blunder.move()
                    break
        else:
            # Si le déplacement dans la direction actuelle est valide, effectue le déplacement
            self.blunder.move()

        # Récupère l'objet de la case sur laquelle Blunder se trouve actuellement
        cell = self.grid[self.blunder.y][self.blunder.x]
        # Récupère l'état précédent de Blunder pour cette case
        cell_state = [cell.prev_blunder_reverse_state, cell.prev_blunder_break_mode_state, cell.prev_blunder_direction]
        # Récupère l'état actuel de Blunder
        blunder_state = [self.blunder.reverse_state, self.blunder.break_mode_state, self.blunder.direction]
        # Vérifie si l'état de Blunder a changé depuis le dernier passage sur cette case
        if cell_state != blunder_state:
            # Si l'état a changé, met à jour l'état précédent de Blunder pour cette case
            cell.prev_blunder_reverse_state = self.blunder.reverse_state
            cell.prev_blunder_break_mode_state = self.blunder.break_mode_state
            cell.prev_blunder_direction = self.blunder.direction
        else:
            # Si l'état n'a pas changé depuis le dernier passage sur cette case, cela signifie qu'il y a une boucle infinie
            self.infinite_loop = True





def read_input_data(game: Game):
    game.grid_height, game.grid_width = map(int, input().split())
    
    # Créer la liste des lignes de symboles en une seule fois
    symbols_list = [input() for _ in range(game.grid_height)]
    
    # Créer la liste des listes de cellules
    game.grid = [[Cell(symbol) for symbol in row] for row in symbols_list]

    # Parcourir les cellules et détecter les symboles spéciaux
    for y, row in enumerate(game.grid):
        for x, cell in enumerate(row):
            if cell.symbol == START_SYMBOL:
                game.blunder.x = x
                game.blunder.y = y
            elif cell.symbol == TELEPORTER_SYMBOL:
                if not game.teleporter1:
                    game.teleporter1 = (x, y)
                elif not game.teleporter2:
                    game.teleporter2 = (x, y)


if __name__ == "__main__":
    # création du jeu et initialisation avec les données d'entrée
    game = Game()
    read_input_data(game)
    
    # boucle principale de jeu jusqu'à ce que Blunder atteigne la sortie ou boucle infinie
    #Si blunder rejoind la case FINISH_SYMBOL (question 2) alors il meurt et le jeu s'arrête ou si c'est une infinite_loop le jeu s'arrete également (Question 10)
    while game.current_symbol != FINISH_SYMBOL and not game.infinite_loop: 
        # déplace Blunder
        game.move_blunder()
        
        # si Blunder est dans un état de boucle infinie, sortir de la boucle principale
        if game.infinite_loop:
            break
        
        # si Blunder est dans l'état de mode casseur et rencontre un mur faible, le casse et répond à la question 7 
        if game.blunder.break_mode_state and game.current_symbol == WEAK_WALL_SYMBOL:
            game.grid[game.blunder.y][game.blunder.x] = Cell(EMPTY_SYMBOL)
            game.reset_grid_state()
    
    # si Blunder a atteint la sortie, imprimer sa séquence de mouvements
    if not game.infinite_loop:
        for move in game.blunder.moves:
            print(move)
    # sinon, imprimer "LOOP"
    else:
        print("LOOP")
