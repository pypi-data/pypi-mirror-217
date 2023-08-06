class GradeDetails:
    def __init__(self, data: dict):
        self.grade: int = None
        self.id: int = None
        self.score_earned: int = None
        self.raw_time_played: int = None
        self.time_played_seconds: float = None
        self.time_played_minutes: float = None
        self.time_played_hours: float = None
        if data:
            self.grade: int = data['grade']+1
            self.id: int = data['id']
            self.score_earned: int = data['scoreEarned']
            # timePlayed returns time in ms
            self.raw_time_played: int = data['timePlayed']
            self.time_played_seconds: float = data['timePlayed']/1000
            self.time_played_minutes: float = data['timePlayed']/60000
            self.time_played_hours: float = data['timePlayed']/3600000