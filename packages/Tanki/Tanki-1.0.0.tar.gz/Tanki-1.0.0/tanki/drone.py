class Drone:
    def __str__(self) -> str:
        return self.name

    def __init__(self, data: dict):
        # grade for drones are -1 because they upgrade by 'step' according to the wiki
        self.grade: int = data['grade']
        self.id: int = data['id']
        self.image_url: str = data['imageUrl']
        self.name: str = data['name']
        # self.properties (Not really sure what this does? It appears as null for everyone so far)
        self.score_earned: int = data['scoreEarned']
        # timePlayed returns time in ms
        self.raw_time_played: int = data['timePlayed']
        self.time_played_seconds: float = data['timePlayed']/1000
        self.time_played_minutes: float = data['timePlayed']/60000
        self.time_played_hours: float = data['timePlayed']/3600000