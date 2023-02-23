import math
import os
import random
import json
from datetime import datetime as dt
from datetime import timedelta as td
import pygame
from pygame.locals import *

pygame.init()

# TODO: runway numbers
# TODO: up/down arrow on altitude
# TODO: change color when To hasnt been reached
# TODO: include airspeed in tags
# TODO: fix air tags
# TODO: begin caoture text


class Environment:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BG = (25, 72, 80)
    BG_CONTROLS = (0, 102, 102)
    INV_COLORS = [(44, 93, 118), (74, 148, 186)]
    FONT14 = pygame.font.Font("roboto.ttf", 14)
    FONT12 = pygame.font.Font("roboto.ttf", 12)
    SCALE = 90

    def __init__(self, *args) -> None:

        self.allMovingSprites = pygame.sprite.Group()

        # load plane tech spec data from json file
        with open("atc-airplanes.json", mode="r") as json_file:
            self.airplaneData = json.loads(json_file.read())
        self.activeAirplanes = []

        self.init_pygame()
        self.init_load_airspace()
        self.init_load_console()

    def init_pygame(self):
        # pygame init
        os.environ["SDL_VIDEO_WINDOW_POS"] = "7, 28"
        self.DISPLAY_WIDTH = pygame.display.Info().current_w
        self.DISPLAY_HEIGHT = pygame.display.Info().current_h // 1.07
        self.RADAR_WIDTH = int(self.DISPLAY_WIDTH * 0.75)
        self.RADAR_HEIGHT = self.DISPLAY_HEIGHT
        self.CONTROLS_WIDTH = int(self.DISPLAY_WIDTH * 0.25)
        self.MESSAGE_HEIGHT = int(self.DISPLAY_HEIGHT * 0.1)
        self.INVENTORY_HEIGHT = int(self.DISPLAY_HEIGHT * 0.4)
        self.INPUT_HEIGHT = int(self.DISPLAY_HEIGHT * 0.1)
        self.CONSOLE_HEIGHT = int(self.DISPLAY_HEIGHT * 0.2)
        self.WEATHER_HEIGHT = int(self.DISPLAY_HEIGHT * 0.2)

        self.displaySurface = pygame.display.set_mode(
            (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
        )
        pygame.display.set_caption("ATC Simulator")

    def init_load_airspace(self):
        with open("atc-airspace.json", mode="r") as json_file:
            self.airspaceInfo = json.loads(json_file.read())
        # create VOR shape entities
        triangle = pygame.Surface((10, 10))
        triangle.fill(self.BG)
        pygame.draw.polygon(triangle, self.WHITE, ((5, 0), (0, 9), (9, 9)), True)
        circles = pygame.Surface((10, 10))
        circles.fill(self.BG)
        pygame.draw.circle(circles, self.WHITE, (5, 5), 5, True)
        pygame.draw.circle(circles, self.WHITE, (5, 5), 3, True)
        star = pygame.Surface((10, 10))
        star.fill(self.BG)
        _s = ((5, 1), (7, 4), (9, 5), (7, 6), (5, 9), (3, 6), (1, 5), (3, 4), (5, 1))
        pygame.draw.polygon(star, self.WHITE, _s, True)
        symbols = {"TRIANGLE": triangle, "CIRCLES": circles, "STAR": star}

        # create Radar main and background surfaces
        self.radarSurface = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.radarSurface.fill(self.BG)
        self.radarBG = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.radarBG.fill(self.BG)
        # add VOR entities to Radar background surface
        for vor in self.airspaceInfo["VOR"]:
            self.radarBG.blit(source=symbols[vor["symbol"]], dest=(vor["xy"]))
            self.radarBG.blit(
                source=self.FONT14.render(
                    vor["name"],
                    True,
                    self.WHITE,
                    self.BG,
                ),
                dest=(vor["xy"][0] + 14, vor["xy"][1] - 3),
            )
        # add Runway entities to Radar background surface
        for runway in self.airspaceInfo["runways"]:
            pygame.draw.line(
                self.radarBG,
                self.WHITE,
                runway["from"]["xy"],
                runway["to"]["xy"],
                width=4,
            )
            for d in ("from", "to"):
                self.radarBG.blit(
                    source=self.FONT14.render(
                        runway[d]["tag"], True, self.WHITE, self.BG
                    ),
                    dest=runway[d]["xy"],
                )

    def init_load_console(self):
        # add Controls - Message background
        self.messageSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.MESSAGE_HEIGHT - 2)
        )
        self.messageSurface.fill((self.BG_CONTROLS))
        self.messageBG = pygame.Surface((self.CONTROLS_WIDTH, self.MESSAGE_HEIGHT - 2))
        self.messageSurface.fill((self.BG_CONTROLS))
        self.messageText = []

        # add Controls - Inventory background
        self.inventorySurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.INVENTORY_HEIGHT - 2)
        )
        self.inventorySurface.fill(self.BLACK)
        self.inventoryBG = pygame.Surface(
            (self.CONTROLS_WIDTH, self.INVENTORY_HEIGHT - 2)
        )
        self.inventoryBG.fill(self.BLACK)

        # add Controls - Input background
        self.inputSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.INVENTORY_HEIGHT - 2)
        )
        self.inputSurface.fill((self.WHITE))
        self.inputBG = pygame.Surface((self.CONTROLS_WIDTH, self.INVENTORY_HEIGHT - 2))
        self.inputBG.fill((self.WHITE))

        # add Controls - Console background
        self.consoleSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.CONSOLE_HEIGHT - 2)
        )
        self.consoleSurface.fill((self.BG_CONTROLS))
        self.consoleBG = pygame.Surface((self.CONTROLS_WIDTH, self.CONSOLE_HEIGHT - 2))
        self.consoleBG.fill((self.BG_CONTROLS))

        # add Controls - Weather background
        self.weatherSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.WEATHER_HEIGHT - 2)
        )
        self.weatherSurface.fill((self.BG_CONTROLS))
        self.weatherBG = pygame.Surface((self.CONTROLS_WIDTH, self.WEATHER_HEIGHT - 2))
        self.weatherBG.fill((self.BG_CONTROLS))
        img = pygame.transform.scale(
            pygame.image.load("atc_compass.png"),
            (self.WEATHER_HEIGHT, self.WEATHER_HEIGHT),
        )
        self.weatherBG.blit(source=img, dest=(self.CONTROLS_WIDTH // 2, 0))

        self.allLevel2Surfaces = [
            [self.radarSurface, self.radarBG, (0, 0)],
            [self.messageSurface, self.messageBG, (self.RADAR_WIDTH + 5, 0)],
            [
                self.inventorySurface,
                self.inventoryBG,
                (self.RADAR_WIDTH + 5, self.MESSAGE_HEIGHT + 2),
            ],
            [
                self.inputSurface,
                self.inputBG,
                (self.RADAR_WIDTH + 5, self.MESSAGE_HEIGHT + self.INVENTORY_HEIGHT + 2),
            ],
            [
                self.consoleSurface,
                self.consoleBG,
                (
                    self.RADAR_WIDTH + 5,
                    self.MESSAGE_HEIGHT + self.INVENTORY_HEIGHT + self.INPUT_HEIGHT + 2,
                ),
            ],
            [
                self.weatherSurface,
                self.weatherBG,
                (
                    self.RADAR_WIDTH + 5,
                    self.MESSAGE_HEIGHT
                    + self.INVENTORY_HEIGHT
                    + self.INPUT_HEIGHT
                    + +self.CONSOLE_HEIGHT
                    + 2,
                ),
            ],
        ]

    def load_new_plane(self, selected, inbound):
        callSign = random.choice(ATC.airspaceInfo["callsigns"]) + str(
            random.randint(1000, 9999)
        )  # replace with available call signs at airport
        if inbound:
            # coordinates -- must appear from edge of airspace
            _h = float(random.randint(5, self.RADAR_WIDTH - 5))
            _v = float(random.randint(5, self.DISPLAY_HEIGHT - 5))
            if random.randint(0, 1) < 0.5:
                x, y = (
                    _h,
                    15.0 if random.randint(0, 1) < 0.5 else self.RADAR_HEIGHT - 15,
                )
            else:
                x, y = (
                    15.0 if random.randint(0, 1) < 0.5 else self.RADAR_WIDTH - 15,
                    _v,
                )
            # heading -- must be pointing in general direction of runway
            if x < self.RADAR_WIDTH / 2 and y < self.RADAR_HEIGHT / 2:
                h = 90
            elif x < self.RADAR_WIDTH / 2 and y > self.RADAR_HEIGHT / 2:
                h = 0
            elif x > self.RADAR_WIDTH / 2 and y < self.RADAR_HEIGHT / 2:
                h = 180
            else:
                h = 270
            heading = random.randint(h, h + 90)
            # altitude
            altitude = random.randint(30000, 80000)
            # speed
            speed = random.randint(200, 500)
            # status
            isGround = False
        else:
            # coordinates
            x, y = 100.0, 100.0  # replace with runway header
            # heading
            heading = 200  # replace with runway heading
            # altitude
            altitude = 680  # replace with runway altitude
            # speed
            speed = 0
            # status
            isGround = True
        # add airplane instance to active planes
        _p = Airplane(
            aircraft=selected,
            callSign=callSign,
            fixedInfo=self.airplaneData[selected],
            x=x,
            y=y,
            heading=heading,
            altitude=altitude,
            speed=speed,
            climb=0,
            turn=0,
            isLanding=False,
            isInbound=inbound,
            isGround=isGround,
        )
        self.activeAirplanes.append(_p)
        # add sprite to pygame framework
        self.allMovingSprites.add(_p)
        # announce new plane in message box
        ATC.messageText.append(
            (
                f"| {dt.strftime(dt.now(), '%H:%M:%S')} | {callSign} {'Arriving' if inbound else 'Departing'}",
                dt.now(),
            )
        )

    def next_frame(self):
        # process messages
        if ATC.messageText and dt.now() - ATC.messageText[0][1] > td(seconds=10):
            ATC.messageText.pop(0)
        # process planes
        for seq, plane in enumerate(self.activeAirplanes):
            # sequential number
            plane.sequence = seq
            # calculate new x,y coordinates
            plane.x += (plane.speed / ATC.SCALE) * math.sin(math.radians(plane.heading))
            plane.y -= (plane.speed / ATC.SCALE) * math.cos(math.radians(plane.heading))
            # altitude change
            if plane.altitude < plane.altitudeTo:
                plane.altitude = min(
                    (plane.altitude + plane.ascentRate), plane.altitudeTo
                )
            elif plane.altitude > plane.altitudeTo:
                plane.altitude = max(
                    (plane.altitude + plane.descentRate), plane.altitudeTo
                )
            # speed change
            if plane.speed < plane.speedTo:
                plane.speed = min((plane.speed + plane.accelAir), plane.speedTo)
            elif plane.speed > plane.speedTo:
                plane.speed = max((plane.speed + plane.decelAir), plane.speedTo)
            # heading change
            clockwise = (plane.headingTo - plane.heading + 360) % 360
            anticlockwise = (plane.heading - plane.headingTo + 360) % 360
            if clockwise < anticlockwise:  # clockwise turn
                plane.heading = (plane.heading + plane.turnRate + 360) % 360
            elif anticlockwise < clockwise:  # anticlockwise turn
                plane.heading = (plane.heading - plane.turnRate + 360) % 360
            if min(clockwise, anticlockwise) <= plane.turnRate:
                plane.heading = plane.headingTo
            # update pygame moving entities info - Radar screen
            plane.boxPosition = (plane.x, plane.y)
            plane.tailPosition0 = (plane.x + 3, plane.y + 3)
            plane.tailPosition1 = (
                plane.x
                + plane.tailLength * math.sin(math.radians(plane.heading + 180)),
                plane.y
                - plane.tailLength * math.cos(math.radians(plane.heading + 180)),
            )
            plane.tagText0 = ATC.FONT12.render(plane.callSign, True, ATC.WHITE, ATC.BG)
            plane.tagText1 = ATC.FONT12.render(
                f"{(plane.altitude // 1000):03}={plane.speed}", True, ATC.WHITE, ATC.BG
            )
            plane.tagPosition0 = (plane.x + 20, plane.y + 20)
            plane.tagPosition1 = (plane.x + 20, plane.y + 33)
            # update inventory item
            plane.inventoryText = pygame.Surface((ATC.CONTROLS_WIDTH - 15, 40))
            plane.inventoryText.fill(ATC.INV_COLORS[seq % 2])
            plane.inventoryText.blit(
                ATC.FONT12.render(
                    f"{plane.callSign}  {plane.headingTo}°  {plane.altitudeTo}=",
                    True,
                    ATC.WHITE,
                    ATC.INV_COLORS[seq % 2],
                ),
                dest=(5, 5),
            )
            plane.inventoryText.blit(
                ATC.FONT12.render(
                    f"{plane.aircraft}  {'Arrival' if plane.isInbound else 'Departure'}",
                    True,
                    ATC.WHITE,
                    ATC.INV_COLORS[seq % 2],
                ),
                dest=(5, 20),
            )
            plane.inventoryPosition = (5, seq * 42 + 2)
            plane.inventoryColor = self.INV_COLORS[seq % 2]


class Airplane(pygame.sprite.Sprite):
    def __init__(self, **kw):
        super().__init__()
        # airplance fixed characteristics
        self.aircraft = kw["aircraft"]
        self.callSign = kw["callSign"]
        self.speedMin = kw["fixedInfo"]["speed"]["min"]
        self.speedMax = kw["fixedInfo"]["speed"]["max"]
        self.speedLand = kw["fixedInfo"]["speed"]["landing"]
        self.speedTakeoff = kw["fixedInfo"]["speed"]["takeoff"]
        self.ascentRate = kw["fixedInfo"]["ascentRate"]
        self.descentRate = kw["fixedInfo"]["descentRate"]
        self.turnRate = kw["fixedInfo"]["turnRate"]
        self.accelGround = kw["fixedInfo"]["acceleration"]["ground"]
        self.accelAir = kw["fixedInfo"]["acceleration"]["air"]
        self.decelGround = kw["fixedInfo"]["deceleration"]["ground"]
        self.decelAir = kw["fixedInfo"]["deceleration"]["air"]
        # airplane position
        self.x = kw["x"]
        self.y = kw["y"]
        self.heading = kw["heading"]
        self.altitude = kw["altitude"]
        # airplane position change
        self.speed = kw["speed"]
        self.climb = kw["climb"]
        self.turn = kw["turn"]
        # airplane destination
        self.speedTo = self.speed
        self.altitudeTo = self.altitude
        self.headingTo = self.heading
        # airplane status
        self.isLanding = kw["isLanding"]
        self.isInbound = kw["isInbound"]
        self.isGround = kw["isGround"]
        # create pygame entity - airplane box
        self.boxSurface = pygame.Surface((6, 6))
        self.boxSurface.fill(ATC.WHITE)
        self.boxPosition = (self.x, self.y)
        # create pygame entity - airplane tail
        self.tailLength = 16
        self.tailPosition0 = (self.x + 3, self.y + 3)
        self.tailPosition1 = (self.x, self.y)
        # create pygame entity - airplane tag (dummy data)
        self.tagText0 = self.tagText1 = self.inventoryText = ATC.FONT12.render(
            " ",
            True,
            ATC.WHITE,
            ATC.BG,
        )
        self.tagPosition0 = self.tagPosition1 = self.inventoryPosition = (
            self.x + 20,
            self.y + 20,
        )
        self.inventoryColor = (0, 0, 0)


def update_pygame_display():

    # reload all level-2 background surfaces
    for surfaces in ATC.allLevel2Surfaces:
        surfaces[0].blit(source=surfaces[1], dest=(0, 0))

    # load Radar main surface + Inventory main surface
    for entity in ATC.allMovingSprites:
        ATC.radarSurface.blit(source=entity.boxSurface, dest=entity.boxPosition)
        pygame.draw.line(
            ATC.radarSurface, ATC.RED, entity.tailPosition0, entity.tailPosition1
        )
        ATC.radarSurface.blit(source=entity.tagText0, dest=entity.tagPosition0)
        ATC.radarSurface.blit(source=entity.tagText1, dest=entity.tagPosition1)
        ATC.inventorySurface.blit(
            source=entity.inventoryText, dest=entity.inventoryPosition
        )

    # load Message main surface
    for y, text_line in enumerate(ATC.messageText):
        text = ATC.FONT14.render(text_line[0], True, ATC.WHITE, ATC.BLACK)
        ATC.messageSurface.blit(
            source=text,
            dest=(5, y * 15 + 4),
        )

    # load Weather main surface
    text = ATC.FONT14.render(
        f"GMT: {dt.strftime(dt.now(),'%H:%M:%S')}", True, ATC.BLACK, ATC.BG
    )
    ATC.weatherSurface.blit(
        source=text,
        dest=(10, 25),
    )

    # reload all level-2 main surfaces
    for surfaces in ATC.allLevel2Surfaces:
        ATC.displaySurface.blit(source=surfaces[0], dest=surfaces[2])

    pygame.display.update()


def main():
    k = 0
    while True and k < 200:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    ATC.activeAirplanes[2].headingTo = 10
                elif event.key == K_RIGHT:
                    ATC.activeAirplanes[3].altitudeTo = 10000
        update_pygame_display()

        # chance of loading new plane
        if random.randint(0, 100) <= 15 and len(ATC.activeAirplanes) < 7:
            ATC.load_new_plane(
                selected="B747", inbound=True
            )  # if random.randint(0, 1) <= 0.5 else False)

        ATC.next_frame()
        pygame.time.delay(1000)

        k += 1


ATC = Environment()
# for _ in range(6):
#     ATC.load_new_plane("A320", ATC.airplaneData["A320"], inbound=True)

main()
