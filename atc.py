import math
import random
import json, os
from datetime import datetime as dt
from datetime import timedelta as td
import pygame
from pygame.locals import *
from gtts import gTTS


pygame.init()


# TODO: go around
# TODO: click on radar airplane to select
# TODO: select any runway to land


class Environment:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BG = (25, 72, 80)
    BG_CONTROLS = (0, 102, 102)
    INV_COLORS = [(44, 93, 118), (74, 148, 186)]

    FONT12 = pygame.font.Font("seguisym.ttf", 12)
    FONT14 = pygame.font.Font("seguisym.ttf", 14)
    FONT20 = pygame.font.Font("roboto.ttf", 20)
    SCALE = 90
    SPEED = 1
    FPS = 60

    MAX_AIRPLANES = 9
    MESSAGE_DISPLAY_TIME = 20  # seconds
    ILS_ANGLE = 20  # degrees
    ILS_HEADING = 30  # degrees
    ERRORS = ["*VOID*", "Last Command Not Understood", "Unable to Comply"]
    audioOn = False
    score = 0


class Airspace:
    def __init__(self, *args) -> None:
        # load plane tech spec data from json file
        with open("atc-airplanes.json", mode="r") as json_file:
            self.airplaneData = json.loads(json_file.read())
        self.activeAirplanes = []

        self.init_pygame()
        self.init_load_airspace()
        self.init_load_console()

    def init_pygame(self):
        # pygame init
        # os.environ["SDL_VIDEO_WINDOW_POS"] = "7, 28"
        self.DISPLAY_WIDTH = pygame.display.Info().current_w
        self.DISPLAY_HEIGHT = pygame.display.Info().current_h // 1.07
        self.RADAR_WIDTH = int(self.DISPLAY_WIDTH * 0.75)
        self.RADAR_HEIGHT = self.DISPLAY_HEIGHT
        self.CONTROLS_WIDTH = int(self.DISPLAY_WIDTH * 0.25)
        self.MESSAGE_HEIGHT = int(self.DISPLAY_HEIGHT * 0.1)
        self.INVENTORY_HEIGHT = int(self.DISPLAY_HEIGHT * 0.45)
        self.INPUT_HEIGHT = int(self.DISPLAY_HEIGHT * 0.05)
        self.CONSOLE_HEIGHT = int(self.DISPLAY_HEIGHT * 0.2)
        self.WEATHER_HEIGHT = int(self.DISPLAY_HEIGHT * 0.2)

        self.displaySurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("ATC Simulator")

    def init_load_airspace(self):
        with open("atc-airspace.json", mode="r") as json_file:
            self.airspaceInfo = json.loads(json_file.read())
        # create VOR shape entities
        triangle = pygame.Surface((10, 10))
        triangle.fill(ENV.BG)
        pygame.draw.polygon(triangle, ENV.WHITE, ((5, 0), (0, 9), (9, 9)), True)
        circles = pygame.Surface((10, 10))
        circles.fill(ENV.BG)
        pygame.draw.circle(circles, ENV.WHITE, (5, 5), 5, True)
        pygame.draw.circle(circles, ENV.WHITE, (5, 5), 3, True)
        star = pygame.Surface((10, 10))
        star.fill(ENV.BG)
        _s = ((5, 1), (7, 4), (9, 5), (7, 6), (5, 9), (3, 6), (1, 5), (3, 4), (5, 1))
        pygame.draw.polygon(star, ENV.WHITE, _s, True)
        symbols = {"TRIANGLE": triangle, "CIRCLES": circles, "STAR": star}

        # create Radar main and background surfaces
        self.radarSurface = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.radarSurface.fill(ENV.BG)
        self.radarBG = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.radarBG.fill(ENV.BG)
        # add VOR entities to Radar background surface
        for vor in self.airspaceInfo["VOR"]:
            self.radarBG.blit(
                source=symbols[vor["symbol"]], dest=((vor["x"], vor["y"]))
            )
            self.radarBG.blit(
                source=ENV.FONT14.render(
                    vor["name"],
                    True,
                    ENV.WHITE,
                    ENV.BG,
                ),
                dest=(vor["x"] + 14, vor["y"] - 3),
            )
        # add Runway entities to Radar background surface
        for runway in self.airspaceInfo["runways"]:
            pygame.draw.line(
                self.radarBG,
                ENV.WHITE,
                (runway["headL"]["x"], runway["headL"]["y"]),
                (runway["headR"]["x"], runway["headR"]["y"]),
                width=runway["width"],
            )
            for d in ("headL", "headR"):
                self.radarBG.blit(
                    source=ENV.FONT14.render(
                        runway[d]["tag"]["text"], True, ENV.WHITE, ENV.BG
                    ),
                    dest=runway[d]["tag"]["xy"],
                )

    def init_load_console(self):
        # add Controls - Message background
        self.messageSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.MESSAGE_HEIGHT - 2)
        )
        self.messageBG = pygame.Surface.copy(self.messageSurface)
        self.messageSurface.fill((ENV.BLACK))
        self.messageText = []

        # add Controls - Inventory background
        self.inventorySurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.INVENTORY_HEIGHT - 2)
        )
        self.inventorySurface.fill(ENV.BLACK)
        self.inventoryBG = pygame.Surface.copy(self.inventorySurface)

        # add Controls - Input background
        self.inputSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.INVENTORY_HEIGHT - 2)
        )
        self.inputSurface.fill((ENV.WHITE))
        self.inputBG = pygame.Surface.copy(self.inputSurface)
        self.commandText = ""

        # add Controls - Console background
        self.consoleSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.CONSOLE_HEIGHT - 2)
        )
        self.consoleSurface.fill((ENV.BG_CONTROLS))
        self.consoleBG = pygame.Surface.copy(self.inventorySurface)

        # add Controls - Weather background
        self.weatherSurface = pygame.Surface(
            (self.CONTROLS_WIDTH, self.WEATHER_HEIGHT - 2)
        )
        self.weatherSurface.fill((ENV.BG_CONTROLS))
        self.weatherBG = pygame.Surface.copy(self.weatherSurface)
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
        )
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
            heading = (
                ATC.calc_heading(
                    x,
                    y,
                    ATC.airspaceInfo["runways"][0]["headL"]["x"],
                    ATC.airspaceInfo["runways"][0]["headL"]["y"],
                )
                + random.randint(-30, 30)
            )
            altitude = random.randint(5000, 8000)
            speed = random.randint(200, 500)
            isGround = False
            finalDestination = ""
        else:
            # select random runway
            runway = random.choice(ATC.airspaceInfo["runways"])
            # select random head (later update with wind direction)
            heads = [runway["headL"], runway["headR"]]
            random.shuffle(heads)
            x, y = (heads[0]["x"], heads[0]["y"])
            heading = self.calc_heading(x, y, heads[1]["x"], heads[1]["y"])
            # altitude
            altitude = 680  # replace with runway altitude
            # speed
            speed = 0
            # status
            isGround = True
            # random destination
            finalDestination = random.choice(ATC.airspaceInfo["VOR"])
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
            finalDestination=finalDestination,
        )
        self.activeAirplanes.append(_p)
        # announce new plane in message box
        text = f"{callSign} {'Arriving' if inbound else 'Departing from Runway '+heads[0]['tag']['text']+' to '+finalDestination['name']}"
        ATC.messageText.append(
            (
                f"| {dt.strftime(dt.now(), '%H:%M:%S')} | {text}",
                dt.now(),
            )
        )
        ATC.play_audio_message(text)

    def calc_heading(self, x0, y0, x1, y1):
        a = abs(math.degrees(math.atan((y1 - y0) / (x1 - x0))))
        if x0 > x1 and y0 < y1:
            return int(270 - a)
        elif x0 < x1 and y0 < y1:
            return int(90 + a)
        elif x0 > x1 and y0 > y1:
            return int(270 + a)
        else:
            return int(90 - a)

    def play_audio_message(self, message):
        if ENV.audioOn == False:
            return
        gTTS(
            text=message,
            lang="en",
            slow=False,
        ).save("temp.wav")
        os.system("start temp.wav")

    def next_frame(self):
        # process messages
        if ATC.messageText and dt.now() - ATC.messageText[0][1] > td(
            seconds=ENV.MESSAGE_DISPLAY_TIME
        ):
            ATC.messageText.pop(0)
        # process planes
        for seq, plane in enumerate(self.activeAirplanes):
            # sequential number
            plane.sequence = seq
            # calculate new x,y coordinates
            plane.x += (plane.speed / ENV.SCALE) * math.sin(math.radians(plane.heading))
            plane.y -= (plane.speed / ENV.SCALE) * math.cos(math.radians(plane.heading))
            # speed change
            if plane.speed < plane.speedTo:
                plane.speed = min(
                    (
                        plane.speed + plane.accelGround
                        if plane.isGround
                        else plane.speed + plane.accelAir
                    ),
                    plane.speedTo,
                )
            elif plane.speed > plane.speedTo:
                plane.speed = max(
                    (
                        plane.speed + plane.decelGround
                        if plane.isGround
                        else plane.decelAir
                    ),
                    plane.speedTo,
                )
            # only change altitude and heading if plane is airborne
            left_right = "="
            if not plane.isTakeoff and plane.onRadar and not plane.isGround:
                # altitude change
                if plane.altitude < plane.altitudeTo:
                    plane.altitude = int(
                        min((plane.altitude + plane.ascentRate), plane.altitudeTo)
                    )
                elif plane.altitude > plane.altitudeTo:
                    plane.altitude = int(
                        max((plane.altitude + plane.descentRate), plane.altitudeTo)
                    )
                # recalculate headingTo if fixed point as destination (VOR, runway head)
                if plane.goToFixed:
                    plane.headingTo = ATC.calc_heading(
                        plane.x, plane.y, plane.goToFixed[0], plane.goToFixed[1]
                    )
                # heading change
                clockwise = (plane.headingTo - plane.heading + 360) % 360
                anticlockwise = (plane.heading - plane.headingTo + 360) % 360
                if clockwise < anticlockwise:  # clockwise turn
                    plane.heading = (plane.heading + plane.turnRate + 360) % 360
                    left_right = ">"
                elif anticlockwise < clockwise:  # anticlockwise turn
                    plane.heading = (plane.heading - plane.turnRate + 360) % 360
                    left_right = "<"
                if min(clockwise, anticlockwise) <= plane.turnRate:
                    plane.heading = plane.headingTo
            # check for end of takeoff conditions
            if plane.isTakeoff and plane.speed >= plane.speedTakeoff:
                plane.isTakeoff = False
                plane.isGround = False

            # recalculate descent rate if plane is landing
            if plane.isLanding and not plane.isGround:
                s = math.sqrt(
                    (plane.x - plane.goToFixed[0]) ** 2
                    + (plane.y - plane.goToFixed[1]) ** 2
                )

                # plane cannot descent faster than max descent rate
                plane.descentRate = max(
                    plane.descentRate,
                    -(plane.altitude - plane.altitudeTo)
                    / (s / (plane.speed / ENV.SCALE)),
                )

                # check if touchdown
                x, y = plane.goToFixed[0], plane.goToFixed[1]
                if (
                    x - 2 <= int(plane.x) <= x + 2
                    and y - 2 <= int(plane.y) <= y + 2
                    and plane.altitude == plane.altitudeTo
                    and plane.isLanding
                ):
                    x, y = (
                        ATC.airspaceInfo["runways"][0]["headR"]["x"],
                        ATC.airspaceInfo["runways"][0]["headR"]["y"],
                    )
                    plane.heading = ATC.calc_heading(plane.x, plane.y, x, y)
                    plane.speedTo = 0
                    plane.isGround = True

            # update pygame moving entities info - Radar screen
            plane.boxPosition = plane.boxSurface.get_rect(center=(plane.x, plane.y))
            plane.tailPosition0 = (plane.x, plane.y)
            plane.tailPosition1 = (
                plane.x
                + plane.tailLength * math.sin(math.radians(plane.heading + 180)),
                plane.y
                - plane.tailLength * math.cos(math.radians(plane.heading + 180)),
            )
            up_down = (
                chr(8593)
                if plane.altitude < plane.altitudeTo
                else chr(8595)
                if plane.altitude > plane.altitudeTo
                else "="
            )
            plane.tagText0 = ENV.FONT12.render(plane.callSign, True, ENV.WHITE, ENV.BG)
            plane.tagText1 = ENV.FONT12.render(
                f"{(plane.altitude // 1000):03}{up_down}{plane.speed//10}",
                True,
                ENV.WHITE,
                ENV.BG,
            )
            plane.tagPosition0 = (plane.x + 20, plane.y + 20)
            plane.tagPosition1 = (plane.x + 20, plane.y + 33)
            # update inventory item
            plane.inventoryText = pygame.Surface((ATC.CONTROLS_WIDTH - 15, 40))
            color = ENV.INV_COLORS[0 if plane.isInbound else 1]
            plane.inventoryText.fill(color)
            accel = (
                chr(8593)
                if plane.speed < plane.speedTo
                else chr(8595)
                if plane.speed > plane.speedTo
                else "="
            )
            plane.inventoryText.blit(
                ENV.FONT12.render(
                    f"{plane.callSign}  {f'{plane.headingTo:03}°' if not plane.goToFixed else plane.goToFixedName}{left_right}  {plane.altitudeTo} {up_down}  {plane.speedTo} {accel}",
                    True,
                    ENV.WHITE,
                    color,
                ),
                dest=(5, 5),
            )
            plane.inventoryText.blit(
                ENV.FONT12.render(
                    f"{plane.aircraft}  {'Arrival' if plane.isInbound else f'Departure --> '+plane.finalDestination['name']}",
                    True,
                    ENV.WHITE,
                    color,
                ),
                dest=(5, 20),
            )
            plane.inventoryPosition = (5, seq * 42 + 2)
            plane.inventoryClickArea = pygame.Rect(
                self.RADAR_WIDTH,
                self.MESSAGE_HEIGHT + seq * 42 + 2,
                self.CONTROLS_WIDTH,
                40,
            )
            plane.inventoryColor = ENV.INV_COLORS[0 if plane.isInbound else 1]
            # check if plane has finised trip
            if plane.isInbound:
                if plane.isGround and plane.speed == 0:
                    plane.onRadar = False
                    ATC.activeAirplanes.remove(plane)
                    ENV.score += 1
            else:
                x, y = plane.finalDestination["x"], plane.finalDestination["y"]
                if (
                    x - 10 <= int(plane.x) <= x + 10
                    and y - 10 <= int(plane.y) <= y + 10
                    and plane.altitude >= ATC.airspaceInfo["altitudes"]["handOff"]
                ):
                    plane.onRadar = False
                    ATC.activeAirplanes.remove(plane)
                    ENV.score += 1


class Airplane(pygame.sprite.Sprite):
    def __init__(self, **kw):
        super().__init__()
        # airplance fixed characteristics
        self.aircraft = kw["aircraft"]
        self.callSign = kw["callSign"]
        self.speedMin = kw["fixedInfo"]["speed"]["min"]
        self.speedMax = kw["fixedInfo"]["speed"]["max"]
        self.speedCruise = kw["fixedInfo"]["speed"]["cruising"]
        self.speedLanding = kw["fixedInfo"]["speed"]["landing"]
        self.speedTakeoff = kw["fixedInfo"]["speed"]["takeoff"]
        self.ascentRate = kw["fixedInfo"]["ascentRate"]
        self.descentRate = kw["fixedInfo"]["descentRate"]
        self.turnRate = kw["fixedInfo"]["turnRate"]
        self.accelGround = kw["fixedInfo"]["acceleration"]["ground"]
        self.accelAir = kw["fixedInfo"]["acceleration"]["air"]
        self.decelGround = kw["fixedInfo"]["deceleration"]["ground"]
        self.decelAir = kw["fixedInfo"]["deceleration"]["air"]
        self.altitudeApproach = kw["fixedInfo"]["altitude"]["approach_max"]
        self.altitudeMax = kw["fixedInfo"]["altitude"]["ceiling"]
        self.altitudeMin = kw["fixedInfo"]["altitude"]["floor"]
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
        self.goToFixed = False
        self.finalDestination = kw["finalDestination"]
        # airplane status
        self.isLanding = kw["isLanding"]
        self.isInbound = kw["isInbound"]
        self.isGround = kw["isGround"]
        self.onRadar = True if self.isInbound else False
        self.isTakeoff = False
        # create pygame entity - airplane box
        self.boxSurface = pygame.Surface((9, 9))
        pygame.draw.rect(self.boxSurface, ENV.WHITE, (0, 0, 8, 8), width=1)
        self.boxPosition = (-10, -10)  # dummy data
        # create pygame entity - airplane tail
        self.tailLength = 16
        self.tailPosition0 = (0, 0)
        self.tailPosition1 = (0, 0)
        # create pygame entities (dummy data)
        self.tagText0 = self.tagText1 = self.inventoryText = ENV.FONT12.render(
            " ",
            True,
            ENV.WHITE,
            ENV.BG,
        )
        self.tagPosition0 = self.tagPosition1 = self.inventoryPosition = (
            self.x + 20,
            self.y + 20,
        )
        self.inventoryColor = (0, 0, 0)
        self.inventoryClickArea = pygame.Rect(0, 0, 0, 0)


def process_click(pos):
    for plane in ATC.activeAirplanes:
        if plane.inventoryClickArea.collidepoint(pos):
            ATC.commandText = plane.callSign + " "
            return


def process_keydown(key):
    if key == 27:
        quit()
    if ATC.commandText in ENV.ERRORS:
        ATC.commandText = ""
    if 97 <= key <= 122 or 48 <= key <= 57 or key == K_SPACE:  # A - Z + 0 - 9
        ATC.commandText += chr(key).upper()
    elif key == K_BACKSPACE:
        ATC.commandText = ATC.commandText[:-1]
    elif key in (K_KP_ENTER, K_RETURN, K_BACKSLASH):
        process_command()
    elif key == K_TAB:
        ENV.SPEED = 5 if ENV.SPEED == 1 else 1


def process_command():
    if not ATC.commandText or not ATC.activeAirplanes:
        return
    # parse command
    flt, *cmd = ATC.commandText.split(" ")
    # check if flight number exists
    plane = [i for i in ATC.activeAirplanes if i.callSign == flt]
    if plane:
        plane = plane[0]
    else:
        ATC.commandText = ""
        return
    text = "NOTHING"
    error = False
    # check if format is right (2 or 3 blocks of commands)
    if len(cmd) == 1:
        if cmd[0] == "H":
            # go to runway head
            if not plane.onRadar:
                plane.onRadar = True
                text = "Proceed to runway and await clearance."
            else:
                error = 2

        elif cmd[0] == "T":
            # full takeoff
            if not plane.onRadar or (plane.onRadar and plane.speed == 0):
                plane.onRadar = True
                plane.speedTo = (
                    plane.speedCruise if not plane.speedTo else plane.speedTo
                )
                plane.isTakeoff = True
                plane.altitudeTo = max(plane.altitudeTo, plane.altitudeMin)
                text = "Cleared for Takeoff"
            else:
                error = 2
        else:
            error = 1
    elif len(cmd) == 2:
        if cmd[0] == "C":  # change heading to fixed number or VOR
            if cmd[1].isdigit():  # chose fixed heading
                plane.headingTo = int(cmd[1])
                plane.goToFixed = False
                text = f"New heading {int(cmd[1])}"
            else:  # chose VOR
                if cmd[1] in [i["name"] for i in ATC.airspaceInfo["VOR"]]:
                    VORxy = [
                        (i["x"], i["y"])
                        for i in ATC.airspaceInfo["VOR"]
                        if i["name"] == cmd[1]
                    ][0]
                    plane.goToFixed = (VORxy[0], VORxy[1])
                    plane.goToFixedName = cmd[1].strip()
                    text = f"Head to {plane.goToFixedName}"
                else:
                    error = 2
        elif cmd[0] == "A":  # change altitude
            new = int(cmd[1])
            if plane.altitudeMin < new * 1000 < plane.altitudeMax:
                plane.altitudeTo = new * 1000
                text = f"New altitude {new*1000}"
            else:
                error = 2
        elif cmd[0] == "S":  # change speed
            new = int(cmd[1])
            if plane.speedMin < new < plane.speedMax:
                plane.speedTo = int(cmd[1])
                text = f"New speed {int(cmd[1])}"
            else:
                error = 2

        elif cmd[0] == "L":
            runways = []
            for i in ("headL", "headR"):
                for s in ATC.airspaceInfo["runways"]:
                    runways.append(s[i]["tag"])

            selected_runway = [
                (i["xy"], i["heading"]) for i in runways if i["text"] == cmd[1]
            ]

            print("xxxxxxxx", selected_runway)

            if selected_runway:
                # landing condition: must be at or below approach altitude
                altitude_check = plane.altitude <= plane.altitudeApproach
                x, y = (selected_runway[0][0][0], selected_runway[0][0][1])
                # landing condition: must be heading within certain degress from runqay headinng
                delta_heading = abs(plane.heading - selected_runway[0][1])
                delta_heading = (
                    360 - delta_heading if delta_heading > 180 else delta_heading
                )
                heading_check = delta_heading <= ENV.ILS_HEADING
                # landing condition: must be inside ILS triangle (within angle of center line)
                delta_heading = abs(
                    ATC.calc_heading(plane.x, plane.y, x, y) - selected_runway[0][1]
                )
                delta_heading = (
                    360 - delta_heading if delta_heading > 180 else delta_heading
                )
                ILSTriangle_check = delta_heading <= ENV.ILS_ANGLE

                if all(
                    [altitude_check, heading_check, ILSTriangle_check, plane.isInbound]
                ):
                    # new heading to fixed point (runway head)
                    plane.goToFixed = (x, y)
                    plane.goToFixedName = f"Runway {cmd[1]}"
                    # new speed set to landing speed
                    plane.speedTo = plane.speedLanding
                    plane.isLanding = True
                    # new altitude is runway head altitude
                    plane.altitudeTo = ATC.airspaceInfo["altitudes"]["groundLevel"]
                else:
                    error = 2
            else:
                error = 1
        else:
            error = 1
    else:
        error = 1

    if error:
        ATC.commandText = ENV.ERRORS[error]
    else:
        ATC.messageText.append(
            (
                f"| {dt.strftime(dt.now(), '%H:%M:%S')} | Tower to {flt}: {text}",
                dt.now(),
            )
        )
        ATC.play_audio_message(text)
        ATC.commandText = ""


def update_pygame_display():
    # load all level-2 background surfaces
    for surfaces in ATC.allLevel2Surfaces:
        surfaces[0].blit(source=surfaces[1], dest=(0, 0))
    # load Radar main surface + Inventory main surface
    for entity in ATC.activeAirplanes:
        if entity.onRadar:
            ATC.radarSurface.blit(source=entity.boxSurface, dest=entity.boxPosition)
            pygame.draw.line(
                ATC.radarSurface, ENV.RED, entity.tailPosition0, entity.tailPosition1
            )
            ATC.radarSurface.blit(source=entity.tagText0, dest=entity.tagPosition0)
            ATC.radarSurface.blit(source=entity.tagText1, dest=entity.tagPosition1)
        ATC.inventorySurface.blit(
            source=entity.inventoryText, dest=entity.inventoryPosition
        )
    # load Message main surface
    for y, text_line in enumerate(ATC.messageText):
        text = ENV.FONT12.render(text_line[0], True, ENV.WHITE, ENV.BLACK)
        ATC.messageSurface.blit(
            source=text,
            dest=(5, y * 15 + 4),
        )
    # load Input Command main surface
    text = ENV.FONT20.render(ATC.commandText, True, ENV.BLACK, ENV.WHITE)
    ATC.inputSurface.blit(
        source=text,
        dest=(5, 5),
    )
    # load Weather main surface
    text = ENV.FONT14.render(
        f"GMT: {dt.strftime(dt.now(),'%H:%M:%S')}", True, ENV.WHITE, ENV.BLACK
    )
    ATC.weatherSurface.blit(
        source=text,
        dest=(10, 25),
    )
    # load Console main surface
    text = ENV.FONT14.render(f"Score: {ENV.score}", True, ENV.WHITE, ENV.BLACK)
    ATC.consoleSurface.blit(source=text, dest=(10, 10))
    # load all level-2 main surfaces
    for surfaces in ATC.allLevel2Surfaces:
        ATC.displaySurface.blit(source=surfaces[0], dest=surfaces[2])

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    delay = ENV.FPS // ENV.SPEED
    while True:
        clock.tick(ENV.FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                process_keydown(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                process_click(pos=pygame.mouse.get_pos())
        update_pygame_display()
        # actions happen with regulated frequency
        delay -= 1
        if delay == 0:
            ATC.next_frame()
            delay = ENV.FPS // ENV.SPEED
            # chance of loading new plane
            if (
                random.randint(0, 100) <= 15
                and len(ATC.activeAirplanes) < ENV.MAX_AIRPLANES
            ):
                ATC.load_new_plane(
                    selected="B747",
                    inbound=True if random.randint(0, 1) <= 0.8 else False,
                )


ENV = Environment()
ATC = Airspace()

main()
