# Importar librerías/modulos
import arcade
import time
import webbrowser

# Versión del juego
version = "Alpha"

# Tamaño de la ventana (ancho y alto)
s_width = 800
s_height = 600

# Parámetro relacionado a la velocidad del personaje
MOVEMENT_SPEED = 5

# Margen de pixeles Jugador - Pantalla
LEFT_VIEWPORT_MARGIN = 400
RIGHT_VIEWPORT_MARGIN = 400
BOTTOM_VIEWPORT_MARGIN = 400
TOP_VIEWPORT_MARGIN = 400


# Menú de inicio
class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        print("Now in main menu.")
        self.background = None  # Parámetro del background (imagen de fondo) vacio
        arcade.set_background_color(arcade.color.BLACK)

    # Configurar la vista
    def setup(self):
        self.background = arcade.load_texture("resources/images/menu_screenf.jpg")  # Se añade la imagen al background

    # Mostrar la imagen de fondo y generar texto en pantalla
    def on_draw(self):
        arcade.start_render()

        # Generar la imagen mediante un rectángulo
        arcade.draw_lrwh_rectangle_textured(0, 0, s_width, s_height, self.background)

    # Casos donde se hace uso del mouse/ratón
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and 334 <= x <= 482 and 315 <= y <= 371:  # Main Game
            tutorial_view = TutorialView()
            tutorial_view.setup()
            self.window.show_view(tutorial_view)

        elif button == arcade.MOUSE_BUTTON_LEFT and 264 <= x <= 536 and 220 <= y <= 278:  # Settings Menu
            settings_view = Settings()
            settings_view.setup()
            self.window.show_view(settings_view)

        elif button == arcade.MOUSE_BUTTON_LEFT and 264 <= x < 536 and 133 <= y <= 189:  # Exit game
            print("User left the game through main menu.")
            exit()


# Nivel 1
class GameView1(arcade.View):
    def __init__(self):
        super().__init__()
        print("Now in game, level 1.")
        self.window.set_mouse_visible(False)
        self.player_list = None
        self.player = None
        self.background = None
        self.ground_list = None
        self.walls_list = None
        # Movimiento de la pantalla
        self.view_bottom = 0
        self.view_left = 0
        self.setup()

    def setup(self):
        self.background = arcade.load_texture('resources/images/galaxy.png')
        self.view_left = 0
        self.view_bottom = 0

        # Cargar al jugador
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedWalkingSprite()

        # Animaciones
        # Personaje quieto a la derecha
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("resources/images/animated_characters"
                                                                    "/charlie/charlie_stand.png"))

        # Personaje quieto a la izquierda
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("resources/images/animated_characters/charlie"
                                                                   "/charlie_stand.png", mirrored=True))

        # Personaje caminando a la derecha
        self.player.walk_right_textures = []
        for i in range(0, 8):
            self.player.walk_right_textures.append(arcade.load_texture(f"resources/images/animated_characters"
                                                                       f"/charlie/charlie_walk{i}.png"))

        # Personaje caminando a la izquierda
        self.player.walk_left_textures = []
        for i in range(0, 8):
            self.player.walk_left_textures.append(arcade.load_texture(f"resources/images/animated_characters"
                                                                      f"/charlie/charlie_walk{i}.png",
                                                                      mirrored=True))

        # Personaje caminando arriba y/o abajo
        self.player.walk_down_textures = []
        self.player.walk_up_textures = []

        for i in range(0, 4):
            self.player.walk_down_textures.append(arcade.load_texture(f"resources/images/animated_characters/charlie"
                                                                      f"/charlie_wdown{i}.png"))

        for i in range(0, 4):
            self.player.walk_up_textures.append(arcade.load_texture(f"resources/images/animated_characters/charlie"
                                                                    f"/charlie_wdown{i}.png"))

        # Parámetros de aparición del jugador
        self.player.scale = 1
        self.player.center_x = 50
        self.player.center_y = 434
        self.player_list.append(self.player)

        # Cargar el mapa y los layers
        my_map = arcade.tilemap.read_tmx("resources/mapas/nivel 3.tmx")
        self.ground_list = arcade.tilemap.process_layer(my_map, "ground", 1)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        arcade.draw_lrwh_rectangle_textured(-625, -625, 6400, 6400, self.background)
        self.ground_list.draw()
        self.player.update_animation()
        self.player_list.draw()

        # Movimiento de la pantalla
        changed = False

        # Izquierda
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Derecha
        right_boundary = self.view_left + s_width - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Arriba
        top_boundary = self.view_bottom + s_height - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Abajo
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Desplazamiento
            arcade.set_viewport(
                self.view_left,
                s_width + self.view_left,
                self.view_bottom,
                s_height + self.view_bottom,
            )

    def update(self, delta_time):
        self.player.update()
        # Límites de ventana
        if self.player.center_x >= 1014:
            print("Boundary!")
            self.player.center_x = 1014

        elif self.player.center_x <= 10:
            print("Boundary!")
            self.player.center_x = 10

        if self.player.center_y >= 1014:
            print("Boundary!")
            self.player.center_y = 1014

        elif self.player.center_y <= 16:
            print("Boundary!")
            self.player.center_y = 16

        # Siguiente nivel
        if self.player.center_x == 1014 and 192 <= self.player.center_y <= 288:
            print("Next level!")
            next_view = GameView2()
            next_view.setup()
            self.window.show_view(next_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:  # 65307
            self.window.set_mouse_visible(True)
            pause = PauseView(self)
            self.window.show_view(pause)
            print(f"Pressed {key}")
        if key == arcade.key.W or key == arcade.key.UP:  # 119 and 65362
            self.player.change_y = MOVEMENT_SPEED
            print(f"Pressed {key}")
        if key == arcade.key.A or key == arcade.key.LEFT:  # 97 and 65361
            self.player.change_x = -MOVEMENT_SPEED
            print(f"Pressed {key}")
        if key == arcade.key.S or key == arcade.key.DOWN:  # 115 and 65364
            self.player.change_y = -MOVEMENT_SPEED
            print(f"Pressed {key}")
        elif key == arcade.key.D or key == arcade.key.RIGHT:  # 100 and 65363
            self.player.change_x = MOVEMENT_SPEED
            print(f"Pressed {key}")

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
            print(f"Released {key}")
        elif key == arcade.key.A or key == arcade.key.D or key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
            print(f"Released {key}")


# Nivel 2
class GameView2(arcade.View):
    def __init__(self):
        super().__init__()
        print("Now in game, level 2.")
        self.window.set_mouse_visible(False)
        self.player_list = None
        self.player = None
        self.background = None
        self.ground_list = None
        self.walls_list = None
        self.view_bottom = 0
        self.view_left = 0

        # Movimiento de la pantalla
        self.view_bottom = 0
        self.view_left = 0
        self.setup()

    def setup(self):
        self.background = arcade.load_texture('resources/images/galaxy.png')
        self.view_left = 0
        self.view_bottom = 0

        # Cargar al jugador
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedWalkingSprite()

        # Animaciones
        # Personaje quieto a la derecha
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("resources/images/animated_characters"
                                                                    "/charlie/charlie_stand.png"))

        # Personaje quieto a la izquierda
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("resources/images/animated_characters/charlie"
                                                                   "/charlie_stand.png", mirrored=True))

        # Personaje caminando a la derecha
        self.player.walk_right_textures = []
        for i in range(0, 8):
            self.player.walk_right_textures.append(arcade.load_texture(f"resources/images/animated_characters"
                                                                       f"/charlie/charlie_walk{i}.png"))

        # Personaje caminando a la izquierda
        self.player.walk_left_textures = []
        for i in range(0, 8):
            self.player.walk_left_textures.append(arcade.load_texture(f"resources/images/animated_characters"
                                                                      f"/charlie/charlie_walk{i}.png",
                                                                      mirrored=True))

        # Personaje caminando arriba y/o abajo
        self.player.walk_down_textures = []
        self.player.walk_up_textures = []

        for i in range(0, 4):
            self.player.walk_down_textures.append(arcade.load_texture(f"resources/images/animated_characters/charlie"
                                                                      f"/charlie_wdown{i}.png"))

        for i in range(0, 4):
            self.player.walk_up_textures.append(arcade.load_texture(f"resources/images/animated_characters/charlie"
                                                                    f"/charlie_wdown{i}.png"))

        # Parámetros de aparición del jugador
        self.player.scale = 1
        self.player.center_x = 50
        self.player.center_y = 434
        self.player_list.append(self.player)

        # Cargar el mapa y los layers
        my_map = arcade.tilemap.read_tmx("resources/mapas/nivel 1.tmx")
        self.ground_list = arcade.tilemap.process_layer(my_map, "ground", 1)
        self.walls_list = arcade.tilemap.process_layer(my_map, "planet", 1)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        arcade.draw_lrwh_rectangle_textured(-625, -625, 6400, 6400, self.background)
        self.ground_list.draw()
        self.walls_list.draw()
        self.player.update_animation()
        self.player_list.draw()

        # Movimiento de la pantalla
        changed = False

        # Izquierda
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Derecha
        right_boundary = self.view_left + s_width - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Arriba
        top_boundary = self.view_bottom + s_height - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Abajo
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Desplazamiento
            arcade.set_viewport(
                self.view_left,
                s_width + self.view_left,
                self.view_bottom,
                s_height + self.view_bottom,
            )

    def update(self, delta_time):
        self.player.update()
        # Límites de ventana
        if self.player.center_x >= 1014:
            print("Boundary!")
            self.player.center_x = 1024

        elif self.player.center_x <= 10:
            print("Boundary!")
            self.player.center_x = 10

        if self.player.center_y >= 1014:
            print("Boundary!")
            self.player.center_y = 1014

        elif self.player.center_y <= 16:
            print("Boundary!")
            self.player.center_y = 16

        # Siguiente nivel
        if self.player.center_x == 1024 and 352 <= self.player.center_y <= 448:
            print("Next level")
            next_view = GameView3()
            next_view.setup()
            self.window.show_view(next_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:  # 65307
            self.window.set_mouse_visible(True)
            pause = PauseView(self)
            self.window.show_view(pause)
            print(f"Pressed {key}")
        if key == arcade.key.W or key == arcade.key.UP:  # 119 and 65362
            self.player.change_y = MOVEMENT_SPEED
            print(f"Pressed {key}")
        if key == arcade.key.A or key == arcade.key.LEFT:  # 97 and 65361
            self.player.change_x = -MOVEMENT_SPEED
            print(f"Pressed {key}")
        if key == arcade.key.S or key == arcade.key.DOWN:  # 115 and 65364
            self.player.change_y = -MOVEMENT_SPEED
            print(f"Pressed {key}")
        elif key == arcade.key.D or key == arcade.key.RIGHT:  # 100 and 65363
            self.player.change_x = MOVEMENT_SPEED
            print(f"Pressed {key}")

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
            print(f"Released {key}")
        elif key == arcade.key.A or key == arcade.key.D or key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
            print(f"Released {key}")


# Nivel 3
class GameView3(arcade.View):
    def __init__(self):
        super().__init__()
        print("Now in game, level 3.")
        self.window.set_mouse_visible(False)
        self.player_list = None
        self.player = None
        self.background = None
        self.ground_list = None
        self.walls_list = None
        self.walls2_list = None
        self.view_bottom = 0
        self.view_left = 0
        self.setup()

        # Movimiento de la pantalla
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):

        self.background = arcade.load_texture('resources/images/galaxy.png')
        self.view_left = 0
        self.view_bottom = 0

        # Cargar al jugador
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedWalkingSprite()

        # Animaciones
        # Personaje quieto a la derecha
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("resources/images/animated_characters"
                                                                    "/charlie/charlie_stand.png"))

        # Personaje quieto a la izquierda
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("resources/images/animated_characters/charlie"
                                                                   "/charlie_stand.png", mirrored=True))

        # Personaje caminando a la derecha
        self.player.walk_right_textures = []
        for i in range(0, 8):
            self.player.walk_right_textures.append(arcade.load_texture(f"resources/images/animated_characters"
                                                                       f"/charlie/charlie_walk{i}.png"))

        # Personaje caminando a la izquierda
        self.player.walk_left_textures = []
        for i in range(0, 8):
            self.player.walk_left_textures.append(arcade.load_texture(f"resources/images/animated_characters"
                                                                      f"/charlie/charlie_walk{i}.png",
                                                                      mirrored=True))

        # Personaje caminando arriba y/o abajo
        self.player.walk_down_textures = []
        self.player.walk_up_textures = []

        for i in range(0, 4):
            self.player.walk_down_textures.append(arcade.load_texture(f"resources/images/animated_characters/charlie"
                                                                      f"/charlie_wdown{i}.png"))

        for i in range(0, 4):
            self.player.walk_up_textures.append(arcade.load_texture(f"resources/images/animated_characters/charlie"
                                                                    f"/charlie_wdown{i}.png"))

        # Parámetros de aparición del jugador
        self.player.scale = 1
        self.player.center_x = 100
        self.player.center_y = 100
        self.player_list.append(self.player)

        # Cargar el mapa y los layers
        my_map = arcade.tilemap.read_tmx("resources/mapas/mundo.tmx")
        self.ground_list = arcade.tilemap.process_layer(my_map, "Ground", 1)
        self.walls_list = arcade.tilemap.process_layer(my_map, "Walls", 1, use_spatial_hash=True)
        self.doorlever_list = arcade.tilemap.process_layer(my_map, "doorlever", use_spatial_hash=True)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        arcade.draw_lrwh_rectangle_textured(-625, -625, 6400, 6400, self.background)
        self.ground_list.draw()
        self.walls_list.draw()
        self.doorlever_list.draw()
        self.player.update_animation()
        self.player_list.draw()

        # Movimiento de la pantalla
        changed = False

        # Izquierda
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Derecha
        right_boundary = self.view_left + s_width - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Arriba
        top_boundary = self.view_bottom + s_height - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Abajo
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Desplazamiento
            arcade.set_viewport(
                self.view_left,
                s_width + self.view_left,
                self.view_bottom,
                s_height + self.view_bottom,
            )

    def update(self, delta_time):
        self.player.update()

        def collision_x():
            print("Collision.")
            self.player.center_y -= 5
            self.player.change_x = 0
            self.player.change_y = 0

        def collision_x2():
            print("Collision.")
            self.player.center_y += 5
            self.player.change_x = 0
            self.player.change_y = 0

        def collision_y():
            print("Collision.")
            self.player.center_x += 5
            self.player.change_x = 0
            self.player.change_y = 0

        def collision_y2():
            print("Collision.")
            self.player.center_x -= 5
            self.player.change_x = 0
            self.player.change_y = 0

        # Límites de ventana
        if self.player.center_x >= 3190:
            print("Boundary!")
            self.player.center_x = 3190

        elif self.player.center_x <= 10:
            print("Boundary!")
            self.player.center_x = 10

        if self.player.center_y >= 3190:
            print("Boundary!")
            self.player.center_y = 3190

        elif self.player.center_y <= 16:
            print("Boundary!")
            self.player.center_y = 16

        # Colisiones

        # Abscisas
        # Primer Tramo
        if 0 <= self.player.center_x <= 61 and 145 <= self.player.center_y <= 196:
            collision_x()
        elif 0 <= self.player.center_x <= 210 and 180 <= self.player.center_y <= 200:
            collision_x()
        elif 225 <= self.player.center_x <= 1280 and 120 <= self.player.center_y <= 130:
            collision_x()
        elif 1376 <= self.player.center_x <= 2176 and 120 <= self.player.center_y <= 130:
            collision_x()
        elif 2272 <= self.player.center_x <= 3040 and 120 <= self.player.center_y <= 130:
            collision_x()
        elif 95 <= self.player.center_x <= 1280 and 572 <= self.player.center_y <= 582:
            collision_x2()

        # Segundo Tramo
        elif 706 <= self.player.center_x <= 1279 and 600 <= self.player.center_y <= 1287:
            collision_x()
        elif 192 <= self.player.center_x <= 608 and 600 <= self.player.center_y <= 627:
            collision_x()
        elif 2271 <= self.player.center_x <= 3010 and 395 <= self.player.center_y <= 398:
            collision_x2()
        elif 2048 <= self.player.center_x <= 2912 and 470 <= self.player.center_y <= 475:
            collision_x()
        elif 1950 <= self.player.center_x <= 2175 and 455 <= self.player.center_y <= 460:
            collision_x2()

        # Tercer Tramo
        elif 704 <= self.player.center_x <= 1280 and 1290 <= self.player.center_y <= 1293:
            collision_x2()
        elif 607 <= self.player.center_x <= 1056 and 1365 <= self.player.center_y <= 1375:
            collision_x()
        elif 1152 <= self.player.center_x <= 1376 and 1334 <= self.player.center_y <= 1344:
            collision_x()
        elif 0 <= self.player.center_x <= 95 and 1865 <= self.player.center_y <= 1870:
            collision_x2()
        elif 192 <= self.player.center_x <= 800 and 1893 <= self.player.center_y <= 1897:
            collision_x2()
        elif 0 <= self.player.center_x <= 672 and 1939 <= self.player.center_y <= 1950:
            collision_x()
        elif 768 <= self.player.center_x <= 897 and 1940 <= self.player.center_y <= 1950:
            collision_x()
        elif 896 <= self.player.center_x <= 1312 and 1720 <= self.player.center_y <= 1725:
            collision_x()
        elif 800 <= self.player.center_x <= 1056 and 1666 <= self.player.center_y <= 1672:
            collision_x2()
        elif 2048 <= self.player.center_x <= 2912 and 896 <= self.player.center_y <= 906:
            collision_x2()
        elif 2048 <= self.player.center_x <= 2912 and 980 <= self.player.center_y <= 990:
            collision_x()
        elif 2048 <= self.player.center_x <= 2912 and 1635 <= self.player.center_y <= 1645:
            collision_x2()
        elif 2303 <= self.player.center_x <= 3008 and 1705 <= self.player.center_y <= 1715:
            collision_x()
        elif 1696 <= self.player.center_x <= 1952 and 1636 <= self.player.center_y <= 1642:
            collision_x2()
        elif 1792 <= self.player.center_x <= 2208 and 1709 <= self.player.center_y <= 1719:
            collision_x()
        elif 1152 <= self.player.center_x <= 1952 and 1525 <= self.player.center_y <= 1535:
            collision_x()
        elif 2304 <= self.player.center_x <= 3104 and 2110 <= self.player.center_y <= 2120:
            collision_x2()

        # Parte superior
        elif 95 <= self.player.center_x <= 3200 and 3092 <= self.player.center_y <= 3100:
            collision_x()
        elif 191 <= self.player.center_x <= 672 and 3010 <= self.player.center_y <= 3016:
            collision_x2()
        elif 768 <= self.player.center_x <= 1952 and 3010 <= self.player.center_y <= 3016:
            collision_x2()
        elif 768 <= self.player.center_x <= 1952 and 2200 <= self.player.center_y <= 2205:
            collision_x()
        elif 2048 <= self.player.center_x <= 2560 and 3010 <= self.player.center_y <= 3020:
            collision_x2()
        elif 2560 <= self.player.center_x <= 3200 and 3040 <= self.player.center_y <= 3050:
            collision_x2()

        # Ordenadas
        # Primer Tramo
        if 55 <= self.player.center_x <= 61 and 145 <= self.player.center_y <= 196:
            collision_y()
        elif self.player.center_x == 1280 and 120 <= self.player.center_y <= 582:
            collision_y()
        elif self.player.center_x == 1375 and 120 <= self.player.center_y <= 1335:
            collision_y2()
        elif self.player.center_x == 2175 and 120 <= self.player.center_y <= 455:
            collision_y()
        elif self.player.center_x == 2270 and 120 <= self.player.center_y <= 390:
            collision_y2()
        elif self.player.center_x == 3040 and 0 <= self.player.center_y <= 130:
            collision_y2()

        # Segundo Tramo
        elif self.player.center_x == 1280 and 599 <= self.player.center_y <= 1287:
            collision_y()
        elif self.player.center_x == 700 and 600 <= self.player.center_y <= 1287:
            collision_y2()
        elif self.player.center_x == 100 and 584 <= self.player.center_y <= 1861:
            collision_y()
        elif self.player.center_x == 190 and 600 <= self.player.center_y <= 1894:
            collision_y2()
        elif self.player.center_x == 610 and 600 <= self.player.center_y <= 1370:
            collision_y()
        elif self.player.center_x == 1955 and 450 <= self.player.center_y <= 1638:
            collision_y()
        elif self.player.center_x == 3005 and 390 <= self.player.center_y <= 1720:
            collision_y2()
        elif self.player.center_x == 2915 and 470 <= self.player.center_y <= 903:
            collision_y()
        elif self.player.center_x == 2045 and 470 <= self.player.center_y <= 903:
            collision_y2()

        # Tercer Tramo
        elif self.player.center_x == 800 and 1671 <= self.player.center_y <= 1894:
            collision_y()
        elif self.player.center_x == 895 and 1720 <= self.player.center_y <= 1944:
            collision_y2()
        elif self.player.center_x == 1055 and 1367 <= self.player.center_y <= 1672:
            collision_y()
        elif self.player.center_x == 2915 and 982 <= self.player.center_y <= 1638:
            collision_y()
        elif self.player.center_x == 2045 and 982 <= self.player.center_y <= 1638:
            collision_y2()

        # Tramo final
        elif self.player.center_x == 3105 and 0 <= self.player.center_y <= 2118:
            collision_y()
        elif self.player.center_x == 3165 and 0 <= self.player.center_y <= 2935:
            collision_y2()

        # Siguiente nivel
        if 3105 <= self.player.center_x <= 3175 and self.player.center_y == 16:
            print("Game Over")
            self.player.center_x = 391
            self.player.center_y = 415
            finale = GameFinale(self)
            self.window.show_view(finale)

    # Casos donde se presiona alguna tecla
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:  # 65307
            self.window.set_mouse_visible(True)
            pause = PauseView(self)
            self.window.show_view(pause)
            print(f"Pressed {key}")
        if key == arcade.key.W or key == arcade.key.UP:  # 119 and 65362
            self.player.change_y = MOVEMENT_SPEED
            print(f"Pressed {key}")
        if key == arcade.key.A or key == arcade.key.LEFT:  # 97 and 65361
            self.player.change_x = -MOVEMENT_SPEED
            print(f"Pressed {key}")
        if key == arcade.key.S or key == arcade.key.DOWN:  # 115 and 65364
            self.player.change_y = -MOVEMENT_SPEED
            print(f"Pressed {key}")
        elif key == arcade.key.D or key == arcade.key.RIGHT:  # 100 and 65363
            self.player.change_x = MOVEMENT_SPEED
            print(f"Pressed {key}")

    # Casos donde se libera alguna tecla
    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
            print(f"Released {key}")
        elif key == arcade.key.A or key == arcade.key.D or key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
            print(f"Released {key}")


# Finale
class GameFinale(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        print("The end.")
        self.window.set_mouse_visible(True)
        self.background = None
        self.player = arcade.Sprite()
        arcade.set_background_color(arcade.color.YELLOW)
        self.game_view = game_view
        self.setup()

    def setup(self):
        self.background = arcade.load_texture('resources/images/finale.png')

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(2745, -395, s_width, s_height, self.background)

    def on_mouse_press(self, x, y, button, modifiers):
        # Volver al menú principal
        if button == arcade.MOUSE_BUTTON_LEFT and 207 <= x <= 587 and 277 <= y <= 328:
            quit()


# Tutorial Parte 1 - Descripción
class TutorialView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)
        print("Now in Tutorial, part 1.")

    def setup(self):
        self.background = arcade.load_texture("resources/images/tutorial_screen.jpg")

    # Instrucciones para el tutorial
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, s_width, s_height, self.background)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            tutorial2 = TutorialContinueView()
            tutorial2.setup()
            self.window.show_view(tutorial2)


# Tutorial Parte 2 - Controles
class TutorialContinueView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)
        print("Now in Tutorial, part 2.")

    def setup(self):
        self.background = arcade.load_texture("resources/images/tutorial_screen2.jpg")

    # Mostrar el background y generar el texto en pantalla
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, s_width, s_height, self.background)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            main_game_view = GameView1()
            main_game_view.setup()
            self.window.show_view(main_game_view)


# Pantalla de ajustes
class Settings(arcade.View):
    def __init__(self):
        super().__init__()
        print("Now in settings.")
        self.background = None
        arcade.set_background_color(arcade.color.AMBER)

    def setup(self):
        self.background = arcade.load_texture("resources/images/settings_screen.jpg")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, s_width, s_height, self.background)

    def on_mouse_press(self, x, y, button, modifiers):
        # Volver al menú principal
        if button == arcade.MOUSE_BUTTON_LEFT and 208 <= x <= 564 and 100 <= y <= 158:
            main_menu_view = MainMenu()
            main_menu_view.setup()
            self.window.show_view(main_menu_view)

        # Abrir GitHub
        elif button == arcade.MOUSE_BUTTON_LEFT and 223 <= x <= 561 and 200 <= y <= 258:
            print("GitHub opened.")

            def github():
                url = "https://github.com/"
                webbrowser.register('chrome',
                                    None,
                                    webbrowser.BackgroundBrowser(
                                        'C://Program Files (x86)//Google//Chrome//Application//chrome.exe'))
                webbrowser.get('chrome').open_new(url)

            github()

        # Ver los créditos
        elif button == arcade.MOUSE_BUTTON_LEFT and 280 <= x <= 491 and 296 <= y <= 353:
            credits_view = CreditsView()
            credits_view.setup()
            self.window.show_view(credits_view)


# Pantalla de pausa
class PauseView(arcade.View):  # Pausa
    def __init__(self, game_view):
        print("Pause summoned.")
        super().__init__()
        self.player = arcade.Sprite()
        self.background = arcade.load_texture("resources/images/pause_view.jpg")
        self.game_view = game_view

    def on_draw(self):
        arcade.start_render()

        player_sprite = self.game_view.player
        player_sprite.draw()

        arcade.draw_lrwh_rectangle_textured(self.game_view.player.center_x - 391, self.game_view.player.center_y - 415,
                                            s_width, s_height, self.background)

    def on_key_press(self, key, modifiers):
        # Alternativa a hacer click en pantalla para volver al juego
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and 197 <= x <= 576 and 300 <= y <= 355:
            self.window.show_view(self.game_view)
        elif button == arcade.MOUSE_BUTTON_LEFT and 200 <= x <= 560 and 176 <= y <= 232:
            main_menu = MainMenu()
            main_menu.setup()
            self.window.show_view(main_menu)


# Créditos
class CreditsView(arcade.View):
    def __init__(self):
        super().__init__()
        print("Now in Credits.")
        self.background = None
        arcade.set_background_color(arcade.color.BONDI_BLUE)

    def setup(self):
        self.background = arcade.load_texture("resources/images/creditsview.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, s_width, s_height, self.background)
        arcade.draw_text("Integrantes", s_width / 2, 525, arcade.color.BLACK, font_size=30,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text("", 227, 440, arcade.color.BLACK, font_size=20,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text("", 227, 330, arcade.color.BLACK, font_size=20,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text("", 560, 440, arcade.color.BLACK, font_size=20,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text("", 560, 330, arcade.color.BLACK, font_size=20,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text("Programado en Python 3.8 y Python 3.9", s_width / 2 - 2.5, 220, arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text("IDE: PyCharm Community Edition", s_width / 2 - 2.5, 200, arcade.color.BLACK, font_size=15,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text("Versiones 2020.1.2 y 2021.1", s_width / 2 - 2.5, 180, arcade.color.BLACK, font_size=15,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text(f"Versión del juego: {version}", s_width / 2 - 2.5, 140, arcade.color.BLACK, font_size=15,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text("Código fuente disponible en GitHub.", s_width / 2 - 2.5, 100, arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center", font_name="Arial")
        arcade.draw_text("Volver atrás", 720, 37.5, arcade.color.BLACK, font_size=15,
                         anchor_x="center", font_name="Arial")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and 663 <= x <= 797 and 0 <= y <= 93:
            settings_view = Settings()
            settings_view.setup()
            self.window.show_view(settings_view)


# Función para la ejecución del videojuego
def main():
    print("Hello! You're not supposed to see this, 'cause here is where we debug.")
    exe_time = time.time()
    print(f"Executed: {time.ctime()}\n")
    window = arcade.Window(s_width, s_height, "Space Scape")  # Características de la ventana
    main_menu = MainMenu()
    main_menu.setup()
    window.show_view(main_menu)  # Mostrar la vista del menú
    arcade.run()  # Comenzar el ciclo del juego
    play_time = time.time() - exe_time  # Tiempo de juego
    print(f"\nGame Closed: {time.ctime()}")
    if play_time <= 60:
        print(f"Playtime: {play_time:.2f} seconds.")
    else:
        print(f"Playtime: {play_time / 60:.2f} minutes")


# Ejecución del juego
if __name__ == "__main__":
    main()
