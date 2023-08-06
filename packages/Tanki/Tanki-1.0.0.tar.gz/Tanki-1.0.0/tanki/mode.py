class Mode:
    def __init__(self, data: dict):
        self.name: str = data['name']
        self.score_earned: int = data['scoreEarned']
        self.type: str = data['type']
        # timePlayed returns time in ms
        self.raw_time_played: int = data['timePlayed']
        self.time_played_seconds: float = data['timePlayed']/1000
        self.time_played_minutes: float = data['timePlayed']/60000
        self.time_played_hours: float = data['timePlayed']/3600000
