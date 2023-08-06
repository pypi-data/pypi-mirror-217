class SupplyUsages:
    def __init__(self, data: dict):
        self.mines: Supply = Supply(data[0])
        self.gold_boxes: Supply = Supply(data[1])
        self.nuclear_energies: Supply = Supply(data[2])
        self.boosted_damages: Supply = Supply(data[3])
        self.speed_boosts: Supply = Supply(data[4])
        self.boosted_armors: Supply = Supply(data[5])
        self.repair_kits: Supply = Supply(data[6])


class Supply:
    def __str__(self) -> str:
        return self.name

    def __init__(self, data: dict):
        self.id: int = data['id']
        self.image_url: str = data['imageUrl']
        self.name: str = data['name']
        self.usages: int = data['usages']