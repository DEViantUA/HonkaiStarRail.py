from collections import defaultdict
from .modal import Gacha


async def get_result(records):

    cycles = 0
    new_items = []
    name = set()
    item_count = defaultdict(int)
    rank_count = defaultdict(int)
    rank_reset = {
        '4': 1,
        '5': 1
    }

    for record in reversed(records):
        cycles += 1
        if not record.type in name:
            name.add(record.type)

        item_count[record.type] += 1
        rank_count[record.rank] += 1

        if record.rank == '4':
            record.dropped = rank_reset['4']
            new_items.insert(0,record)
            rank_reset['4'] = 0
        else:
            rank_reset['4'] += 1

        if record.rank== '5':
            record.dropped = rank_reset['5']
            new_items.insert(0,record)
            rank_reset['5'] = 0
        else:
            rank_reset['5'] += 1

    result = {"total": cycles, 
        "total_rank_four": rank_count['4'],
        "total_rank_five": rank_count['5'],
        "next_four_garant": 11-rank_reset['4'],
        "next_five_garant": 91-rank_reset['5'],
        "total_type_one":  [{"name": name1, "count": item_count[name1]} for name1 in name], 
        "history":new_items
    }

    result = Gacha(**result)

    return result