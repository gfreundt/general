import math
import os
import random
import json
import pygame
from pygame.locals import *

pygame.init()


class Environment:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BG = (25, 72, 80)
    BG_CONTROLS = (0, 102, 102)
    FONT14 = pygame.font.Font("roboto.ttf", 14)
    FONT12 = pygame.font.Font("roboto.ttf", 12)
    SCALE = 3

    def __init__(self, *args) -> None:
        # pygame init
        os.environ["SDL_VIDEO_WINDOW_POS"] = "7, 28"
        self.DISPLAY_WIDTH = pygame.display.Info().current_w
        self.DISPLAY_HEIGHT = pygame.display.Info().current_h // 1.1
        self.RADAR_WIDTH = int(self.DISPLAY_WIDTH * 0.75)
        self.RADAR_HEIGHT = self.DISPLAY_HEIGHT
        self.CONTROLS_WIDTH = int(self.DISPLAY_WIDTH * 0.25)
        self.MESSAGE_HEIGHT = int(self.DISPLAY_WIDTH * 0.1)
        self.INVENTORY_HEIGHT = int(self.DISPLAY_HEIGHT * 0.5)
        self.CONSOLE_HEIGHT = int(self.DISPLAY_HEIGHT * 0.2)
        self.WEATHER_HEIGHT = int(self.DISPLAY_HEIGHT * 0.2)

        self.displaySurface = pygame.display.set_mode(
            (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
        )
        pygame.display.set_caption("ATC Simulator")
        self.FramePerSec = pygame.time.Clock()
        # load moving plane information
        self.allMovingSprites = pygame.sprite.Group()
        with open("atc-airplanes.json", mode="r") as json_file:
            self.airplaneInfo = json.loads(json_file.read())
        self.activeAirplanes = []
        # load fixed airspace information
        self.allFixedSprites = pygame.sprite.Group()
        with open("atc-airspace.json", mode="r") as json_file:
            self.airspaceInfo = json.loads(json_file.read())
        self.init_load_airspace()

    def init_load_airspace(self):
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
        # create background surface
        self.bgSurface = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.bgSurface.fill(self.BG)
        # add VOR entities to background surface
        for vor in self.airspaceInfo["VOR"]:
            self.bgSurface.blit(source=symbols[vor["symbol"]], dest=(vor["xy"]))
            self.bgSurface.blit(
                source=self.FONT14.render(
                    vor["name"],
                    True,
                    self.WHITE,
                    self.BG,
                ),
                dest=(vor["xy"][0] + 14, vor["xy"][1] - 3),
            )
        # add Runway entities to background surface
        for runway in self.airspaceInfo["runways"]:
            pygame.draw.line(
                self.bgSurface,
                self.WHITE,
                runway["from"]["xy"],
                runway["to"]["xy"],
                width=4,
            )
            for d in ("from", "to"):
                self.bgSurface.blit(
                    source=self.FONT14.render(
                        runway[d]["tag"], True, self.WHITE, self.BG
                    ),
                    dest=runway[d]["xy"],
                )
        # add Controls background
        self.controlSurface = pygame.Surface((self.CONTROLS_WIDTH, self.DISPLAY_HEIGHT))
        self.controlSurface.fill((self.BLACK))

        # add Controls - Message background
        self.messageSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.MESSAGE_HEIGHT - 2)
        )
        self.messageSurface.fill((self.BG_CONTROLS))

        self.controlSurface.blit(
            source=self.messageSurface,
            dest=(0, 0),
        )
        # add Controls - Inventory background
        self.inventorySurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.INVENTORY_HEIGHT - 2)
        )
        self.inventorySurface.fill((30, 130, 60))

        self.controlSurface.blit(
            source=self.inventorySurface,
            dest=(0, 0),
        )

        # add Controls - Console background
        self.consoleSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.CONSOLE_HEIGHT - 2)
        )
        self.consoleSurface.fill((self.BG_CONTROLS))
        self.controlSurface.blit(
            source=self.consoleSurface,
            dest=(0, self.INVENTORY_HEIGHT),
        )
        # add Controls - Weather background
        self.weatherSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.WEATHER_HEIGHT - 2)
        )
        self.weatherSurface.fill((self.BG_CONTROLS))
        img = pygame.transform.scale(
            pygame.image.load("atc_compass.png"),
            (self.WEATHER_HEIGHT, self.WEATHER_HEIGHT),
        )
        self.weatherSurface.blit(
            source=img, dest=((self.CONTROLS_WIDTH - self.WEATHER_HEIGHT) // 1.2, 0)
        )
        self.controlSurface.blit(
            source=self.weatherSurface,
            dest=(0, self.INVENTORY_HEIGHT + self.CONSOLE_HEIGHT),
        )
        # consolidate Controls
        self.bgSurface.blit(
            source=self.controlSurface,
            dest=(self.DISPLAY_WIDTH - self.CONTROLS_WIDTH, 0),
        )

    def load_new_plane(self, selected, fixedInfo, inbound):
        callSign = "AA" + str(
            random.randint(100, 999)
        )  # replace with available call signs at airport
        if inbound:
            # coordinates -- must appear from edge of airspace
            _h = float(random.randint(5, self.RADAR_WIDTH - 5))
            _v = float(random.randint(5, self.DISPLAY_HEIGHT - 5))
            if random.randint(0, 1) < 0.5:
                x, y = (
                    _h,
                    5.0 if random.randint(0, 1) < 0.5 else self.RADAR_HEIGHT - 5,
                )
            else:
                x, y = (
                    5.0 if random.randint(0, 1) < 0.5 else self.RADAR_WIDTH - 5,
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
            altitude = random.randint(20000, 40000)
            # speed
            speed = random.randint(12, 40)
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
            fixedInfo=fixedInfo,
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

    def next_frame(self):
        """
        print(
            f"{'Arrival' if self.activeAirplanes[2].isInbound else 'Departure'} | {self.activeAirplanes[2].callSign} | coordinates: {self.activeAirplanes[2].x:.2f},{self.activeAirplanes[2].y:.2f} | heading: {self.activeAirplanes[2].heading} | altitude: {self.activeAirplanes[2].altitude}| speed: {self.activeAirplanes[2].speed}"
        )
        """
        for plane in self.activeAirplanes:
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
            # create inventory item
            plane.inventoryText0 = (
                f"{plane.callSign}  {plane.heading}°  {plane.altitude}="
            )
            plane.inventoryText1 = (
                f"{plane.aircraft}  {'Arrival' if plane.isInbound else 'Departure'}"
            )


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
        # create pygame entity - airplane tag
        self.tagText0 = self.tagText1 = ATC.FONT12.render(
            " ",
            True,
            ATC.WHITE,
            ATC.BG,
        )
        self.tagPosition0 = self.tagPosition1 = (self.x + 20, self.y + 20)


ATC = Environment()

for _ in range(6):
    ATC.load_new_plane("A320", ATC.airplaneInfo["A320"], inbound=True)


k = 0
while True and k < 20:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            ATC.activeAirplanes[2].headingTo = 10
    # refresh screen with fixed background
    ATC.displaySurface.blit(source=ATC.bgSurface, dest=(0, 0))
    # render all moving pieces of pygame image
    for entity in ATC.allMovingSprites:
        ATC.displaySurface.blit(source=entity.boxSurface, dest=entity.boxPosition)
        pygame.draw.line(
            ATC.displaySurface, ATC.RED, entity.tailPosition0, entity.tailPosition1
        )
        ATC.displaySurface.blit(source=entity.tagText0, dest=entity.tagPosition0)
        ATC.displaySurface.blit(source=entity.tagText1, dest=entity.tagPosition1)
    pygame.display.update()
    # recalculate position of all airplanes and pause
    ATC.next_frame()
    pygame.time.delay(1000)

    k += 1
