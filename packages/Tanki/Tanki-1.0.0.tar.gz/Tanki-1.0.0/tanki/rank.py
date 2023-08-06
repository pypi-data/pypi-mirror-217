class Rank:
    def __str__(self) -> str:
        return self.rank_name

    def __init__(self, data: int):
        # recruit is rank 1, indexs returned by tanki start at 1
        self.rank_value: int = data
        self.rank_name: str = [
            'Recruit',
            'Private',
            'Gefreiter',
            'Corporal',
            'Master Corporal',
            'Sergeant',
            'Staff Sergeant',
            'Master Sergeant',
            'First Sergeant',
            'Sergeant Major',
            'Warrant Officer 1',
            'Warrant Officer 2',
            'Warrant Officer 3',
            'Warrant Officer 4',
            'Warrant Officer 5',
            'Third Lieutenant',
            'Second Lieutenant',
            'First Lieutenant',
            'Captain',
            'Major',
            'Lieutenant Colonel',
            'Colonel',
            'Brigadier',
            'Major General',
            'Lieutenant General',
            'General',
            'Marshal',
            'Fieldmarshal',
            'Commander',
            'Generalissimo',
            'Legend'
        ][data-1]
