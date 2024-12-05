from collections import defaultdict


def parse():
    with open('p5.input.txt') as f:
        rules = defaultdict(list)
        in_rules = True

        middles_total = 0
        for line in f.readlines():
            line = line.strip()
            if in_rules:
                if not line:
                    in_rules = False
                    continue
                first, second = [int(x) for x in line.split('|')]
                rules[first].append((first, second))
                rules[second].append((first, second))
                continue

            update = [int(x) for x in line.split(',')]
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

            for page in update:
                if not valid_by_rules(page):
                    break
            else:
                middles_total += middle
        return middles_total


if __name__ == "__main__":
    print(parse())