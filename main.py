import pygame
import pygame_menu
from pygame_menu.examples import create_example_window


from random import randrange
from typing import Tuple, Any, Optional, List

ABOUT = [f'pygame-menu {pygame_menu.__version__}',
         f'Author: {pygame_menu.__author__}',
         f'Email: {pygame_menu.__email__}']
DIFFICULTY = ['EASY']
FPS = 60
WINDOW_SIZE = (640, 480)

clock: Optional['pygame.time.Clock'] = None
main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None


def change_difficulty(value: Tuple[Any, int], difficulty: str) -> None:

    selected, index = value
    print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')
    DIFFICULTY[0] = difficulty


def random_color() -> Tuple[int, int, int]:

    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(difficulty: List, font: 'pygame.font.Font', test: bool = False) -> None:

    assert isinstance(difficulty, list)
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    global main_menu
    global clock

    if difficulty == 'EASY':
        f = font.render('Playing as a Yuragi (easy)', True, (255, 255, 255))
    elif difficulty == 'MEDIUM':
        f = font.render('Playing as a Ramzes (medium)', True, (255, 255, 255))
    elif difficulty == 'HARD':
        f = font.render('Playing as a Daxao (hard)', True, (255, 255, 255))
    else:
        raise ValueError(f'unknown difficulty {difficulty}')
    f_esc = font.render('Press ESC to open the menu', True, (255, 255, 255))
    bg_color = "#fffff"
    main_menu.full_reset()
    frame = 0
    while True:

        clock.tick(60)
        frame += 1

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    main_menu.enable()

                    return

        if main_menu.is_enabled():
            main_menu.update(events)

        surface.fill(bg_color)
        surface.blit(f, (int((WINDOW_SIZE[0] - f.get_width()) / 2),
                         int(WINDOW_SIZE[1] / 2 - f.get_height())))
        surface.blit(f_esc, (int((WINDOW_SIZE[0] - f_esc.get_width()) / 2),
                             int(WINDOW_SIZE[1] / 2 + f_esc.get_height())))
        pygame.display.flip()

        if test and frame == 2:
            break


def main_background() -> None:

    global surface
    surface.fill((128, 0, 128))


def main(test: bool = False) -> None:

    global clock
    global main_menu
    global surface

    surface = create_example_window('Game Selector', WINDOW_SIZE)
    clock = pygame.time.Clock()

    play_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        title='Play Menu',
        width=WINDOW_SIZE[0] * 0.75
    )

    submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    submenu_theme.widget_font_size = 15
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=submenu_theme,
        title='Submenu',
        width=WINDOW_SIZE[0] * 0.7
    )
    for i in range(30):
        play_submenu.add.button(f'Back {i}', pygame_menu.events.BACK)
    play_submenu.add.button('Return to main menu', pygame_menu.events.RESET)

    play_menu.add.button('Start',
                         play_function,
                         DIFFICULTY,
                         pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
    play_menu.add.selector('Select difficulty ',
                           [('1 - Easy', 'EASY'),
                            ('2 - Medium', 'MEDIUM'),
                            ('3 - Hard', 'HARD')],
                           onchange=change_difficulty,
                           selector_id='select_difficulty')
    play_menu.add.button('Another menu', play_submenu)
    play_menu.add.button('Return to main menu', pygame_menu.events.BACK)
    about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=about_theme,
        title='About',
        width=WINDOW_SIZE[0] * 0.6
    )

    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    about_menu.add.vertical_margin(30)
    about_menu.add.button('Return to menu', pygame_menu.events.BACK)
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=main_theme,
        title='Main Menu',
        width=WINDOW_SIZE[0] * 0.6
    )

    main_menu.add.button('Play', play_menu)
    main_menu.add.button('About', about_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:

        # Tick
        clock.tick(FPS)

        main_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        pygame.display.flip()

        if test:
            break

