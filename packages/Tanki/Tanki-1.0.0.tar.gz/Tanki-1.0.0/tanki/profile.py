from .exceptions import ProfileNotFoundError
from .supplies_usage import SupplyUsages
from .exceptions import RateLimitError
from .turret import Turret
from .module import Module
from .rating import Rating
from .drone import Drone
from .paint import Paint
from .rank import Rank
from .hull import Hull
from .mode import Mode
import requests
import json

class Profile:
  def __str__(self) -> str:
    return self.__raw_data['name']

  def __init__(self, username: str):
    self.__raw_request = requests.get(f'https://ratings.tankionline.com/api/eu/profile/?user={username}&lang=en')
    try:
      if self.__raw_request.json()['response']:
        self.__raw_data: dict = self.__raw_request.json()['response']
        # self.__raw_data = json.loads(open('data.json', 'r').read())['response']

        self.caught_golds: int = self.__raw_data['caughtGolds']
        self.deaths: int = self.__raw_data['deaths']
        self.earned_crystals: int = self.__raw_data['earnedCrystals']
        self.gear_score: int = self.__raw_data['gearScore']
        self.has_premium: bool = self.__raw_data['hasPremium']
        self.kills: int = self.__raw_data['kills']
        self.name: str = self.__raw_data['name']
        self.score: int = self.__raw_data['score']
        self.score_base: int = self.__raw_data['scoreBase']
        self.score_next: int = self.__raw_data['scoreNext']
        self.kd: float = self.kills/self.deaths
        self.total_supplies: int = sum([item['usages'] for item in self.__raw_data['suppliesUsage']])
      else:
        raise ProfileNotFoundError('Profile does not exist')
    except requests.exceptions.JSONDecodeError:
      raise RateLimitError('Access has been denied to the API')

  def get_raw_response(self) -> requests.Response:
    return self.__raw_request

  def get_raw_data(self) -> dict:
    return self.__raw_data

  def get_rank(self) -> Rank:
    return Rank(self.__raw_data['rank'])

  def get_drones_played(self) -> list[Drone]:
    return [Drone(item) for item in self.__raw_data['dronesPlayed']]

  def get_hulls_played(self) -> list[Hull]:
    raw_hulls = {}
    for hull in self.__raw_data['hullsPlayed']:
      if hull['name'] in raw_hulls:
        raw_hulls[hull['name']].append(hull)
      else:
        raw_hulls[hull['name']] = [hull]

    return [Hull(raw_hulls[item]) for item in raw_hulls]

  def get_modes_played(self) -> list[Mode]:
    return [Mode(item) for item in self.__raw_data['modesPlayed']]

  def get_paints_played(self) -> list[Paint]:
    return [Paint(item) for item in self.__raw_data['paintsPlayed']]

  def get_previous_rating(self) -> Rating:
    return Rating(self.__raw_data['previousRating'])

  def get_rating(self) -> Rating:
    return Rating(self.__raw_data['rating'])

  def get_resistance_modules(self) -> list[Module]:
    raw_modules = {}
    for module in self.__raw_data['resistanceModules']:
      if module['name'] in raw_modules:
        raw_modules[module['name']].append(module)
      else:
        raw_modules[module['name']] = [module]

    return [Module(raw_modules[item]) for item in raw_modules]

  def get_supplies_usage(self) -> SupplyUsages:
    return SupplyUsages(self.__raw_data['suppliesUsage'])

  def get_turrets_played(self) -> list[Turret]:
    raw_turrets = {}
    for turret in self.__raw_data['turretsPlayed']:
      if turret['name'] in raw_turrets:
        raw_turrets[turret['name']].append(turret)
      else:
        raw_turrets[turret['name']] = [turret]

    return [Turret(raw_turrets[item]) for item in raw_turrets]