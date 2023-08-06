class Rating:
    def __init__(self, data: dict):
        self.crystals: RatingObject = RatingObject(data['crystals'])
        self.efficiency: RatingObject = RatingObject(data['efficiency'])
        self.golds: RatingObject = RatingObject(data['golds'])
        self.score: RatingObject = RatingObject(data['score'])


class RatingObject:
    def __init__(self, data: dict):
        self.position: int = None
        self.value: int = None
        if data:
            self.position: int = data['position']
            self.value: int = data['value']
