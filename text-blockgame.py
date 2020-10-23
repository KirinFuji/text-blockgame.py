# text-blockgame.py
# Written By KirinFuji from scratch
#
# Written to test Object Oriented Programming concepts as I learn then.
#
import math

class Vector3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z        

    def GetPos(self):
        if self.x < 0:
            self.x += 32
        if self.y < 0:
            self.y += 32
        if self.z < 0:
            self.z += 8
        return (self.x,self.y,self.z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector3(x,y,z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector3(x,y,z)

    # Overload the division operator, to give the distance between 2 vector3, if used on the objects.
    def __truediv__ (self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return math.sqrt(x*x + y*y + z*z)

class World:
    def __init__(self,width=32,length=32,height=8):
        self.Dimensions = (width,length,height)
        self.Grid = [[[None for x in range(width)] for y in range(length)] for z in range(height)]
        self.Time = 0
        self.Day = 0

    def UpdateBlock(self,pos,value):
        try:
            if type(pos) != tuple:
                raise TypeError(pos)
            self.Grid[pos[0]][pos[1]][pos[2]] = value
        except TypeError as err:
            print(err)

    def GetBlock(self,pos):
        try:
            if type(pos) != tuple:
                raise TypeError(pos)
            return self.Grid[pos[0]][pos[1]][pos[2]]
        except TypeError as err:
            print(err)

class Object:
    def __init__(self,type_,name,texture,colour,tooltip="Object Missing Tooltip",pos=(0,0,0)):
        self.Type = type_
        self.Name = name        
        self.Texture = texture
        self.Colour = colour
        self.Tooltip = tooltip
        self.Position = Vector3(pos[0],pos[1],pos[2])

class Entity(Object):
    def __init__(self,type_,name,texture,colour,tooltip="Entity Missing Tooltip",pos=(0,0,0),Level=0,Damage=0,MaxHealth=10,Holding=None):
        super().__init__(type_,name,texture,colour,tooltip,pos)
        self.Level = Level
        self.Damage = Damage
        self.MaxHealth = MaxHealth
        self.Holding = Holding
        self.Health = self.MaxHealth


class Player_Ent(Entity):
    def __init__(self,type_,name,texture,colour,tooltip="Player Missing Tooltip",pos=(0,0,0),Level=0,Damage=0,MaxHealth=10,Holding=None):
        super().__init__(type_,name,texture,colour,tooltip,pos,Level,Damage,MaxHealth,Holding)
        self.canDig = False
        self.canMine = False
        self.canEat = False
        self.canHeal = False
        self.canMove = True
        self.Inventory = [[None for x in range(9)] for y in range(3)]
        self.Hotbar = [None for x in range(9)]

    def canAttack(self):
        if self.Holding == "Sword":
            return True

    def Move(self,direction,spaces):
        if self.canMove:
            if direction == "North":
                self.Position = self.Position + Vector3(spaces,0,0)

            if direction == "South":
                self.Position = self.Position - Vector3(spaces,0,0)

            if direction == "East":
                self.Position = self.Position + Vector3(0,spaces,0)

            if direction == "West":
                self.Position = self.Position - Vector3(0,spaces,0)

            if direction == "Up":
                self.Position = self.Position + Vector3(0,0,spaces)

            if direction == "Down":
                self.Position = self.Position - Vector3(0,0,spaces)                

class Block(Object):
    def __init__(self,type_,name,texture,colour,tooltip="Block Missing Tooltip",pos=(0,0,0),diggable=False,mineable=False,contents=None,inhabitant=None):
        super().__init__(type_,name,texture,colour,tooltip,pos)
        self.isBlock = True
        self.isDiggable = diggable
        self.isMineable = mineable
        self.contains = contents
        self.inhabitedBy = inhabitant

def Console(Player,GameWorld):
    while True:
        try:
            
            print("> ", end = '')
            input_ = input()
            # Do Stuff
            #print(f"Echo: {input_}")
            input_.split()
            if "exit" in input_:
                break
            elif "help" in input_:
                print("Available Commands:\nmove\n SubCommands:\n  north\n  south\n  east\n  west\n  up\n  down\ninspect\n SubCommands:\n  texture\n  colour\n  pos\nstatus\nhelp\nexit")
            elif "status" in input_:
                try:
                    t_ = GameWorld.GetBlock(Player.Position.GetPos()).Type
                    n_ = GameWorld.GetBlock(Player.Position.GetPos()).Name
                except AttributeError:
                    t_ = "None"
                    n_ = "Air"
                print(f"Player: {Player.Name} @ {Player.Position.GetPos()} Type: {t_} Name: {n_}")
            elif "move" in input_:
                if "north" in input_:
                    Player.Move("North",1)
                elif "south" in input_:
                    Player.Move("South",1)
                elif "east" in input_:
                    Player.Move("East",1)
                elif "west" in input_:
                    Player.Move("West",1)
                elif "up" in input_:
                    Player.Move("Up",1)  
                elif "down" in input_:
                    Player.Move("Down",1)                  
            elif "inspect" in input_:
                if "texture" in input_:
                    print(GameWorld.GetBlock(Player.Position.GetPos()).Texture)
                elif "colour" in input_:
                    print(GameWorld.GetBlock(Player.Position.GetPos()).Colour)
                elif "pos" in input_:
                    print(GameWorld.GetBlock(Player.Position.GetPos()).Position.GetPos())
                else:
                    print("SubCommands: texture, colour, pos")
            else:
                print("Command not Found")
            #
        except AttributeError as err:
            print(f"Error with action: {err}" )
        except Exception as err:
            print(f"Console Error:{err}")
            break

def __main__():

    # Instantiate the world
    GameWorld = World(width=32,length=32,height=8)
    #Fill layer 0 with bedrock
    for x in list(range(len(GameWorld.Grid))):
        for y in list(range(len(GameWorld.Grid[x]))):
            if GameWorld.Grid[x][y][0] == None:
                GameWorld.Grid[x][y][0] = Block("Block","Bedrock","Solid Compacted Coarse","Black",tooltip="Unbreakable Floor",pos=(x,y,0))
    #Fill Layer 1 with stone
    for x in list(range(len(GameWorld.Grid))):
        for y in list(range(len(GameWorld.Grid[x]))):
            if GameWorld.Grid[x][y][1] == None:
                GameWorld.Grid[x][y][1] = Block("Block","Stone","Solid Compacted Smooth","Grey",mineable=True,pos=(x,y,1))
    #Add 3 blocks to layer 2 for testing
    GameWorld.Grid[0][0][2] = Block("Block","Dirt","Loose Rough Chunks","Brown",diggable=True,mineable=True,pos=(0,0,2))
    GameWorld.Grid[1][0][2] = Block("Block","Stone","Solid Compacted Smooth","Grey",mineable=True,pos=(1,0,2))
    GameWorld.Grid[1][1][2] = Block("Block","Sand","Fine Tiny Grains","Yellow-Tan",diggable=True,mineable=True,pos=(1,1,2))
    # Instantiate our player
    KirinFuji = Player_Ent("Player","KirinFuji","KirinFuji.bmp","Purple-Green",tooltip="KirinFuji's Player Character",pos=(0,0,2),MaxHealth=20,Damage=1)
    # Start the console loop

    Console(KirinFuji,GameWorld)

    # Print out each block name and position if not None
    for x in list(range(len(GameWorld.Grid))):
        for y in list(range(len(GameWorld.Grid[x]))):
            for z in list(range(len(GameWorld.Grid[x][y]))):
                if GameWorld.Grid[x][y][z] != None:
                    print(f"{GameWorld.Grid[x][y][z].Name} @ {GameWorld.Grid[x][y][z].Position.GetPos()}")
    print("Done")

if __name__ == "__main__":
    __main__()
