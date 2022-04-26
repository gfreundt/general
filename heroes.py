from copy import deepcopy as copy


def is_possible(database: dict) -> bool:
    database = {i: j for i, j in database.items() if len(j) > 0}
    day1, day2 = [], []
    while len(day1) + len(day2) < len(database):
        for hero in database:
            if not (hero in day1 or hero in day2):
                must_be_in_day1 = [i for i in database[hero] if i in day2]
                must_be_in_day2 = [i for i in database[hero] if i in day1]
                if must_be_in_day1 and must_be_in_day2:
                    return False
                elif must_be_in_day1:
                    day1.append(hero)
                elif must_be_in_day2:
                    day2.append(hero)
                else:
                    day1.append(hero)
    return True


def is_possible2(database: dict) -> bool:
    database = {i: j for i, j in database.items() if len(j) > 0}
    db = copy(database)
    # day1, day2 = [0], database[0]
    day1, day2 = [], []

    while len(day1) + len(day2) < len(db):
        d, e = next(iter(database.items()))
        day1.append(d)
        day2 += e
        change = True
        while change:
            change = False
            for hero in db:
                if not (hero in day1 or hero in day2):
                    must_be_in_day1 = [i for i in database[hero] if i in day2]
                    must_be_in_day2 = [i for i in database[hero] if i in day1]
                    if must_be_in_day1 and must_be_in_day2:
                        return False
                    elif must_be_in_day1:
                        day1.append(hero)
                        del database[hero]
                        change = True
                    elif must_be_in_day2:
                        day2.append(hero)
                        del database[hero]
                        change = True
            print(day1, day2)
    return True


s = {0: [2], 1: [3], 2: [0, 5], 3: [1], 4: [8], 5: [2], 6: [7], 7: [6], 8: [4]}
# s = {
#     0: [6, 5],
#     1: [6],
#     2: [7, 8, 4],
#     3: [8, 4],
#     4: [3, 2],
#     5: [9, 8, 7, 0],
#     6: [0, 1, 7],
#     7: [2, 5, 6],
#     8: [2, 3, 5],
#     9: [5],
# }

print(is_possible2(s))
