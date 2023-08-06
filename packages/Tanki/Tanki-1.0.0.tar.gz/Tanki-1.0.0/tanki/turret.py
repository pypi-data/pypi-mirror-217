from .grades import Grades

class Turret:
    def __str__(self) -> str:
        return self.name

    def __init__(self, data: dict):
        self.grade: int = max([item['grade'] for item in data])+1
        self.image_url: str = data[0]['imageUrl']
        self.name: str = data[0]['name']
        self.score_earned: int = sum([item['scoreEarned'] for item in data])
        # timePlayed returns time in ms
        self.raw_time_played: int = sum([item['timePlayed'] for item in data])
        self.time_played_seconds: float = self.raw_time_played/1000
        self.time_played_minutes: float = self.raw_time_played/60000
        self.time_played_hours: float = self.raw_time_played/3600000

        self.grades: Grades = Grades(data)