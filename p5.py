from collections import defaultdict


def parse():
    with open("p5.input.txt") as f:
        rules = defaultdict(list)
        in_rules = True

        middles_total = 0
        new_middles_total = 0
        for line in f.readlines():
            line = line.strip()
            if in_rules:
                if not line:
                    in_rules = False
                    continue
                first, second = [int(x) for x in line.split("|")]
                rules[first].append((first, second))
                rules[second].append((first, second))
                continue

            update = [int(x) for x in line.split(",")]
            indexes = {page: index for index, page in enumerate(update)}
            middle = update[len(update) // 2]

            def valid_by_rules(page):
                rules_for_page = rules[page]
                for rule in rules_for_page:
                    earlier, later = rule
                    if earlier not in indexes or later not in indexes:
                        continue
                    if page == earlier and not (indexes[page] < indexes[later]):
                        return False
                    if page == later and not (indexes[earlier] < indexes[page]):
                        return False
                return True

            def fix_by_rules():
                relevant_rules = set()
                for page in indexes:
                    for rule in rules.get(page, []):
                        earlier, later = rule
                        if earlier in indexes and later in indexes:
                            relevant_rules.add(rule)
                new_update = []
                while len(new_update) < len(update):
                    candidates = set(indexes.keys()) - set(new_update)
                    if len(candidates) == 1:
                        new_update.append(candidates.pop())
                        break
                    for rule in relevant_rules:
                        earlier, later = rule
                        candidates.discard(later)
                        if len(candidates) == 1:
                            added_item = candidates.pop()
                            new_update.append(added_item)
                            relevant_rules = set(
                                filter(lambda r: r[0] != added_item, relevant_rules)
                            )
                            break
                new_middle = new_update[len(new_update) // 2]
                return new_middle

            for page in update:
                if not valid_by_rules(page):
                    new_middles_total += fix_by_rules()
                    break
            else:
                middles_total += middle
        return middles_total, new_middles_total


if __name__ == "__main__":
    print(*parse(), sep="\n")
