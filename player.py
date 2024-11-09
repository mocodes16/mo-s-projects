from pygame import*
from
class Player(sprite.Sprite):
    def __init__(self,character_selected):
        super().__init__()
        self.player_x = 400
        self.player_y = 400
        self.playerwidth = 60
        self.playerheight = 60
        self.jump_height = 50
        self.jump_count = 10
        self.playerDirection = math.Vector2(0,0)
        self.y_velocity = -16
        self.gravityvalue = 0.2
        self.mrhamflett = image.load("mrhamflett.png")
        self.mrhamflett = transform.scale(self.mrhamflett, (80, 123))
        self.chipmunk = image.load("misssultana.png")
        self.character_selected = character_selected

    def drawPlayer(self, screen):
        if  self.character_selected == "mrhamflett":
            character_image = self.mrhamflett
        else:
            character_image = self.chipmunk

        screen.blit(character_image, (self.player_x, self.player_y))

    def jump(self):
        self.playerDirection.y = self.y_velocity

    def gravity(self):
        self.playerDirection.y += self.gravityvalue
        self.player_y += self.playerDirection.y * 2

    def getInput(self):
        keys = key.get_pressed()  # Handle player movement
        if keys[K_LEFT]:
            self.playerDirection.x = 1
        if keys[K_RIGHT]:
            self.playerDirection.x = -1
        if keys[K_UP]:
            self.jump()

    def update(self):
        self.getInput()
        self.player_x += self.playerDirection.x * 2
       # self.gravity()

