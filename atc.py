import math
import time
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
    FONT14 = pygame.font.Font("roboto.ttf", 14)
    FONT12 = pygame.font.Font("roboto.ttf", 12)
    SCALE = 3

    def __init__(self, *args) -> None:
        # pygame init
        self.FRAME = (
            min(pygame.display.Info().current_h, pygame.display.Info().current_w) // 1.1
        )
        # self.FRAME = 800
        self.displaySurface = pygame.display.set_mode((self.FRAME, self.FRAME))
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
        self.load_airspace()

    def load_airspace(self):

        # create VOR entities
        TRIANGLE = pygame.Surface((10, 10))
        TRIANGLE.fill(self.BG)
        pygame.draw.polygon(TRIANGLE, self.WHITE, ((5, 0), (0, 9), (9, 9)), True)
        CIRCLES = pygame.Surface((10, 10))
        CIRCLES.fill(self.BG)
        pygame.draw.circle(CIRCLES, self.WHITE, (5, 5), 5, True)
        pygame.draw.circle(CIRCLES, self.WHITE, (5, 5), 3, True)
        symbols = {"TRIANGLE": TRIANGLE, "CIRCLES": CIRCLES}

        # create bckground surface
        self.bgSurface = pygame.Surface((self.FRAME, self.FRAME))
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
                dest=(vor["xy"][0] - 10, vor["xy"][1] + 15),
            )
        # add Runway entities to background surface
        for runway in self.airspaceInfo["runways"]:
            pygame.draw.line(
                self.bgSurface,
                self.WHITE,
                runway["from"]["xy"],
                runway["to"]["xy"],
                width=5,
            )
            for d in ("from", "to"):
                self.bgSurface.blit(
                    source=self.FONT14.render(
                        runway[d]["tag"], True, self.WHITE, self.BG
                    ),
                    dest=runway[d]["xy"],
                )

    def load_new_plane(self, selected, fixedInfo, inbound):
        callSign = "AA" + str(
            random.randint(100, 999)
        )  # replace with available call signs at airport
        if inbound:
            # coordinates -- must appear from edge of airspace
            _a = float(random.randint(5, self.FRAME - 5))
            _b = 5.0 if random.randint(0, 1) < 0.5 else self.FRAME - 5
            x, y = (_a, _b) if random.randint(0, 1) < 0.5 else (_b, _a)
            # heading -- must be pointing in general direction of runway
            if x < self.FRAME / 2 and y < self.FRAME / 2:
                h = 90
            elif x < self.FRAME / 2 and y > self.FRAME / 2:
                h = 0
            elif x > self.FRAME / 2 and y < self.FRAME / 2:
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
            turn=5,
            isLanding=False,
            isInbound=inbound,
            isGround=isGround,
        )
        self.activeAirplanes.append(_p)
        # add sprite to pygame framework
        self.allMovingSprites.add(_p)

    def next_frame(self):
        for plane in self.activeAirplanes:
            plane.move_one_tick()
            # print(
            #     f"{'Arrival' if plane.isInbound else 'Departure'} | {plane.callSign} | coordinates: {plane.x},{plane.y} | heading: {plane.heading} | altitude: {plane.altitude}"
            # )


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
        self.speedTo = None
        self.altitudeTo = None
        self.headingTo = None
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

    def move_one_tick(self):
        # calculate new position
        self.x += (self.speed / ATC.SCALE) * math.sin(math.radians(self.heading))
        self.y -= (self.speed / ATC.SCALE) * math.cos(math.radians(self.heading))
        self.altitude += self.climb
        new_heading = (self.heading + self.turn) % 360
        self.heading = new_heading if new_heading >= 0 else (360 + new_heading)
        # update pygame coordinates
        self.boxPosition = (self.x, self.y)
        self.tailPosition0 = (self.x + 3, self.y + 3)
        self.tailPosition1 = (
            self.x + self.tailLength * math.sin(math.radians(self.heading + 180)),
            self.y - self.tailLength * math.cos(math.radians(self.heading + 180)),
        )
        self.tagText0 = ATC.FONT12.render(self.callSign, True, ATC.WHITE, ATC.BG)
        text1 = f"{(self.altitude // 1000):03}={self.speed}"
        self.tagText1 = ATC.FONT12.render(text1, True, ATC.WHITE, ATC.BG)
        self.tagPosition0 = (self.x + 20, self.y + 20)
        self.tagPosition1 = (self.x + 20, self.y + 33)


ATC = Environment()


for _ in range(6):
    ATC.load_new_plane("A320", ATC.airplaneInfo["A320"], inbound=True)


k = 0
while True and k < 50:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    # clear screen with background color
    ATC.displaySurface.fill(ATC.BG)
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

    # ATC.FramePerSec.tick(60)
    ATC.next_frame()
    time.sleep(0.5)

    k += 1
