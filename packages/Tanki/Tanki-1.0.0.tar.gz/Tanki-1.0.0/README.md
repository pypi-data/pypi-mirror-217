# Tanki 

Tanki is an API wrapper for Tanki Online's rating API. Allows you to easily search for users and get information about them. To get started, create a new `Profile` object using `tanki.Profile('username')`

**Notes**
- `raw_time_played` returns time in milliseconds
- If you don't own the grade of a hull, module, or turret, it'll return `None` for all attributes

**Quick Start**
```py
import tanki

# initialize a object
profile = tanki.Profile('walker38552')

# get kills and deaths
print(f'Kills: {profile.kills}, Deaths: {profile.deaths}')

# get k/d ratio
print(f'K/D: {profile.kd}')

# get rank
print(profile.get_rank())
print(profile.get_rank().rank_name)

# get drone data
for drone in profile.get_drones_played():
    print(drone.name, drone.score_earned, drone.time_played_hours)

# get hull data
for hull in profile.get_hulls_played():
    print(hull.name, hull.time_played_hours)
    # show statistics for each grade of the hull
    print(hull.grades.mk1.score_earned)
    print(hull.grades.mk2.score_earned)
    print(hull.grades.mk3.score_earned)
    print(hull.grades.mk4.score_earned)
    print(hull.grades.mk5.score_earned)
    print(hull.grades.mk6.score_earned)
    print(hull.grades.mk7.score_earned)
```