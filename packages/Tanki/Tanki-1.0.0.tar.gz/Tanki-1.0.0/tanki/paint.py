class Paint:
    def __str__(self) -> str:
        return self.name

    def __init__(self, data: dict):
        # paints also return -1 as a grade
        self.grade: int = data['grade']
        self.id: int = data['id']
        self.image_url: str = data['imageUrl']
        self.name: str = data['name']
        self.score_earned: int = data['scoreEarned']
        # timePlayed returns time in ms
        self.raw_time_played: int = data['timePlayed']
        self.time_played_seconds: float = data['timePlayed']/1000
        self.time_played_minutes: float = data['timePlayed']/60000
        self.time_played_hours: float = data['timePlayed']/3600000
