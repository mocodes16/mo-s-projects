from pygame import *
from map import *
import random
init()
SELECTED_CHARACTER = None
bullets = None
all_sprites_group = sprite.Group()
enemy_group = sprite.Group()
all_sprites = sprite.Group()

screen = display.set_mode((screen_width, screen_height))

clock = time.Clock()
fps = 60


class MainMenu:
    def __init__(self):
        display.set_caption("Menu")
        self.screen = display.set_mode((screen_width, screen_height))
        self.background = image.load("mainmenu.png")
        self.background = transform.scale(self.background, (screen_width, screen_height))
        self.title_text = "Gun Brawl"
        self.title_colour = (255, 255, 255)
        self.title_pos = (340, 50)
        self.startButton = Button(300, 200, 600, 100, "PLAY THE FRIGGIN GAME", self.nextScreen)
        self.settingButton = Button(300, 400, 600, 100, "Controls", None)
        self.title_font = font.Font("Transformers Movie.ttf", 100)
        self.currentScreen = self

    def drawScreen(self, screen):
        screen.blit(self.background, (0, 0))
        self.title_text_surface = self.title_font.render(self.title_text, True, self.title_colour)
        screen.blit(self.title_text_surface, self.title_pos)
        self.startButton.draw(screen)
        self.settingButton.draw(screen)

    def handleClick(self):
        self.startButton.handleClick()

    def nextScreen(self):
        self.currentScreen = CharacterScreen()

    def update(self):
        return self.currentScreen


class CharacterScreen:
    def __init__(self):
        self.selectedCharacterImage = None
        display.set_caption("Pick a Character")
        self.screen = display.set_mode((screen_width, screen_height))
        self.background = image.load("option.jpg")
        self.background = transform.scale(self.background, (screen_width, screen_height))
        self.title_text = "Pick a character"
        self.title_colour = (255, 255, 255)
        self.title_pos = (150, 70)
        self.sharon = image.load("sharonpoo.png")
        self.sharon = transform.scale(self.sharon, (162,142))
        self.sharonplayzr = image.load("wasteman.png")
        self.sharonplayzr = transform.scale(self.sharonplayzr, (50,50))
        self.sharonplayzl = transform.flip(self.sharonplayzr, True, False)
        self.mrh = image.load("mrhamflett4.png")
        self.mrh = transform.scale(self.mrh, (142, 147))
        self.mrhplayzl = image.load("mrhamflett1.png")
        self.mrhplayzr = transform.flip(self.mrhplayzl, True, False)
        self.chipmunk = image.load("misssultana3.png")
        self.chipmunk = transform.scale(self.chipmunk, (144, 154))
        self.chipmunkplayzr = image.load("misssultana2.png")
        self.chipmunkplayzl = transform.flip(self.chipmunkplayzr, True, False)
        self.mrhButton = Button(400, 200, 250, 100, "MrHamflett", self.startGameAwesome)
        self.chipmunkButton = Button(50, 200, 250, 100, "Chipmunk", self.startGameChipmunk)
        self.sharonButton = Button(800, 200, 250, 100, "Sharon", self.startGameSharon)
        self.backButton = Button(20,30,100,100,"Back",self.previousScreen)
        self.title_font = font.Font("Transformers Movie.ttf", 100)
        self.currentScreen = self
        self.teleporter = image.load("teleport.png")
        self.teleporter = transform.scale(self.teleporter, (272, 168))

    def drawScreen(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.teleporter, (370, 500))
        screen.blit(self.teleporter, (10, 500))
        screen.blit(self.teleporter, (750, 500))
        screen.blit(self.mrh, (450, 350))
        screen.blit(self.chipmunk, (100, 350))
        screen.blit(self.sharon,(800,350))
        self.title_text_surface = self.title_font.render(self.title_text, True, self.title_colour)
        screen.blit(self.title_text_surface, self.title_pos)
        self.mrhButton.draw(screen)
        self.chipmunkButton.draw(screen)
        self.sharonButton.draw(screen)

    def handleClick(self):
        self.mrhButton.handleClick()
        self.chipmunkButton.handleClick()
        self.sharonButton.handleClick()

    def displayCharacter(self):
        self.currentScreen = GameScreen()
    def startGameAwesome(self):
        global SELECTED_CHARACTER
        SELECTED_CHARACTER = [self.mrhplayzl, self.mrhplayzr]
        self.currentScreen = GameScreen()
    def startGameChipmunk(self):
        global SELECTED_CHARACTER
        SELECTED_CHARACTER = [self.chipmunkplayzl, self.chipmunkplayzr]
        self.currentScreen = GameScreen()

    def startGameSharon(self):
        global SELECTED_CHARACTER
        SELECTED_CHARACTER = [self.sharonplayzl,self.sharonplayzr]
        self.currentScreen = GameScreen()
    def previousScreen(self):
        self.currentScreen = MainMenu()

    def update(self):
        return self.currentScreen


class GameScreen:
    def __init__(self):
        self.player = Player((100,100))
        self.enemy = Enemy((900,360),self.player.rect)
        self.currentScreen = self
        self.background = image.load("background2.jpg")
        self.background = transform.scale(self.background, (screen_width, screen_height))
        self.level = Level(platforms, screen)
        self.backButton = Button(20, 30, 100, 100, "Back", self.previousScreen)

    def drawScreen(self, screen):
        screen.blit(self.background, (0, 0))
        self.level.drawLevel()
        self.player.drawPlayer(screen)
        self.enemy.draw(screen)
        self.backButton.draw(screen)

    def previousScreen(self):
        self.currentScreen = CharacterScreen()

    def handleClick(self):
        self.backButton.handleClick()

    def update(self):
        self.player.getInput()
        self.player.update(self.level)
        self.enemy.update(self.level)
        return self


class Button:
    def __init__(self, x, y, w, h, text, callback=None):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.callback = callback
        self.font = font.Font("Transformers Movie.ttf", 40)
        self.text_colour = (0, 0, 0)
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.buttonColour = (48, 69, 41)
        self.lightButtonColour = (80, 200, 120)
        self.buttonRect = Rect(self.x, self.y, self.width, self.height)
        self.hovered = False
        self.clicked = False

    def draw(self, screen):
        pos = mouse.get_pos()
        if self.buttonRect.collidepoint(pos):
            self.hovered = True
        else:
            self.hovered = False
        draw.rect(screen, self.buttonColour, self.buttonRect)  # draws the buttons
        text_rect = self.image.get_rect(center=self.buttonRect.center)  # centres the text
        screen.blit(self.image, text_rect)

    def handleClick(self):
        if self.buttonRect.collidepoint(mouse.get_pos()):  # checks if mouse is hovering over button
            if mouse.get_pressed()[0]:  # checks left of mouse is clicked
                self.click = True
                if self.callback:  # check if an action has been set
                    self.callback()
            else:
                self.click = False


class Tile(sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = image.load("block.jpg")
        self.image = transform.scale(self.image, (64,30))
        self.rect = self.image.get_rect(topleft=pos)

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

    def getTiles(self):
        return self.tiles

    def setup_level(self, layout):
        self.tiles = sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    x = col_index * tile_size
                    y = row_index * tile_size

    def drawLevel(self):
        # drawing platform
        self.tiles.draw(self.display_surface)

class Enemy(sprite.Sprite):
    def __init__(self, pos, player_rect):
        super().__init__(enemy_group, all_sprites_group)
        self.image = image.load("pudu.png")
        self.image = transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 4
        self.direction = math.Vector2()
        self.velocity = math.Vector2()
        self.position = math.Vector2(pos)
        self.gravity = 0.1
        self.onPlatform = False
        self.jump_speed = -3
        self.player_rect = player_rect  # Store the player's rectangle

    def move(self):
        # Simple AI which will move left or right randomly
        if random.randint(0, 1) == 0:
            self.direction.x = -1
        else:
            self.direction.x = 1

    def applyGravity(self):
        self.velocity.y += self.gravity

    def hunt_player(self):
        # Determine the direction towards the player
        player_center = self.player_rect.center  # Use player_rect to get player's position
        enemy_center = self.rect.center
        direction_to_player = math.Vector2(player_center[0] - enemy_center[0], player_center[1] - enemy_center[1])

        # Normalize the direction vector
        if direction_to_player.length() > 0:
            self.direction = direction_to_player.normalize()

        # Update the velocity based on the direction and speed
        self.velocity = self.direction * self.speed

        # Update the enemy's position based on velocity
        self.position += self.velocity
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def checkCollisions(self,level):
        tiles = level.getTiles()
        self.rect.x += self.velocity.x
        collisions = sprite.spritecollide(self, tiles, False)
        for tile in collisions:
            if self.velocity.x > 0:
                self.rect.right = tile.rect.left
            elif self.velocity.x < 0:
                self.rect.left = tile.rect.right

        self.rect.y += self.velocity.y
        collisions = sprite.spritecollide(self, tiles, False)
        for tile in collisions:
            if self.velocity.y > 0:
                self.rect.bottom = tile.rect.top
                self.onPlatform = True
                self.velocity.y = 0
            elif self.velocity.y < 0:
                self.rect.top = tile.rect.bottom
                self.velocity.y = 0

    def update(self, level):
        self.hunt_player()  # Pass player_rect to hunt_player method
        self.move()
        self.applyGravity()
        self.checkCollisions(level)
        self.position += self.direction * self.speed
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(sprite.Sprite):
    def __init__(self, pos):
        global SELECTED_CHARACTER
        global player_rect
        super().__init__()
        self.rect = SELECTED_CHARACTER[0].get_rect(topleft=pos)
        self.direction = math.Vector2(0, 0)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.gravity = 0.1
        self.onPlatform = False
        self.jump_speed = -3
        self.bullets = sprite.Group()
        self.facing_right = True
        self.lastShot = 0

    def drawPlayer(self, screen):
        if not self.facing_right:
            screen.blit(SELECTED_CHARACTER[0], self.rect)
        else:
            screen.blit(SELECTED_CHARACTER[1], self.rect)


    def jump(self):
        self.direction.y = self.jump_speed

    def getInput(self):
        keys = key.get_pressed()  # Handle player movement
        if not keys[K_LEFT] or keys[K_RIGHT]:
            self.direction.x = 0
        if keys[K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        if keys[K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        if keys[K_UP]:
            self.jump()
        if keys[K_SPACE]:
            currentTime = time.get_ticks()
            if currentTime - self.lastShot > 100:
                self.lastShot = currentTime
                self.shoot()  # Call shoot method when spacebar is pressed


    def applyGravity(self):
        self.direction.y += self.gravity

    def update(self, level):
        self.getInput()
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y
        self.applyGravity()
        if not self.onPlatform:
            self.direction.y += self.gravity
        # check for platform
        tiles = level.getTiles()
        if sprite.spritecollideany(self, tiles):
            self.onPlatform = True
            self.direction.y = 0


    def shoot(self):
        if self.facing_right:
            bullet_direction = math.Vector2(1, 0)
        else:
            bullet_direction = math.Vector2(-1, 0)
        bullet = Bullet(self.rect.midtop, bullet_direction)
        all_sprites.add(bullet)


class Bullet(sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.imagel = image.load("bullet.png")
        self.imagel = transform.scale(self.imagel, (35, 20))
        self.imager = transform.flip(self.imagel, True, False)
        bullets = [self.imagel, self.imager]
        # Determine which image to use based on the direction
        if direction.x > 0:  # Facing right
            self.image = self.imager
        else:  # Facing left
            self.image = self.imagel
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 1
        self.direction = direction.normalize()
        self.pos = math.Vector2(pos)

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.topleft = self.pos

running = True
currentScreen = MainMenu()

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            currentScreen.handleClick()
    keys = key.get_pressed()  # Handle player movement
    if keys[K_ESCAPE]:
        running = False

    screen.fill((255, 255, 255))
    currentScreen = currentScreen.update()
    currentScreen.drawScreen(screen) # draw the currentscreen

    all_sprites.update()  # Update all sprites
    all_sprites.draw(screen)

    display.flip()