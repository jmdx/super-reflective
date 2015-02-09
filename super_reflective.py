import re


# TODO organize these classes better
class GroupType:
    """A class for holding the regexes that start and end a group
    In super-reflective there are two top-level types of groups:
        - Regular groups, marked by [], which can be permuted, and
        - Fillable groups, marked by <>, for which a permutation only acts on the data attached to the group, but
          in the process turns the fillable group into a regular one.
    Note that neither of these types are recursive, so groups cannot contain groups.
    Here the word 'group' is used in the looser informal sense, not in the algebraic sense.
    """

    def __init__(self, opening, closing, name):
        self.opening = opening
        self.closing = closing
        self.name = name

GROUP_TYPES = [
    GroupType(r'\[', r'\]', 'regular'),
    GroupType('<', '>', 'fillable')
]


class RelativePermutation:
    """A permutation on some subset of the integers
    This is represented in cycle notation (see http://en.wikipedia.org/wiki/Cycle_notation)
    For example, the permutation:
        -2 -> -1
        -1 -> 2
        0 -> -2
        1 -> 1
        2 -> 0
        4 -> 5
        5 -> 4
    is represented as (-2-1+2+0)(+4+5).
    Note that signs are mandatory, and redundant components in this notation are illegal, e.g. (+1+2+1), while still a
    valid permutation, but will hit a snag when checking for bijectivity.
    """
    def __init__(self, cycle_notation):
        cycle_matcher = (
            r'\('  # Start with a parenthesis
            r'('
            r'[^\(\)]+'  # Find groups containing non-parenthesis characters
            r')'
            r'\)'  # And end with a closing parenthesis
        )
        self.cycle_notation = cycle_notation
        cycles = re.findall(cycle_matcher, cycle_notation)
        self.permutation_map = {}
        self.cycle_pattern = re.compile(r'[\+-][^\+-]+')
        for cycle in cycles:
            self.add_from_cycle(cycle)

    def add_from_cycle(self, cycle):
        try:
            cycle_ints = list(map(int, self.cycle_pattern.findall(cycle)))
            for index, cycle_component in enumerate(cycle_ints):
                # In cycle notation, each token is mapped to the next consecutive token in the cycle, wrapping around
                # at the end.  For each step, we'll call this next token the 'destination'
                destination = cycle_ints[(index + 1) % len(cycle_ints)]
                if cycle_component in self.permutation_map.keys() or destination in self.permutation_map.values():
                    # If we want to put a key or value in the map that's already there, then that means we hit something
                    # that makes this mapping not bijective, which means it's not really a permutation.
                    raise Exception('Non-bijective or redundant cycle notation: {}'.format(self.cycle_notation))
                self.permutation_map[cycle_component] = destination
        except ValueError:
            raise Exception('Bad cycle notation: ({})'.format(cycle))

    def domain(self):
        return self.permutation_map.keys()

    def __getitem__(self, item):
        return self.permutation_map[item]


class Group:
    def __init__(self, content, group_type):
        self.group_type = group_type
        self.data, remaining_content = Group.split_data_from(content)
        self.operator, remaining_content = Group.split_operator_from(remaining_content)
        self.permutation = RelativePermutation(remaining_content)

    def __str__(self):
        return (
            self.group_type.opening
            + self.data
            + self.operator
            + self.permutation.cycle_notation
            + self.group_type.closing
        )

    @staticmethod
    def split_data_from(content):
        sign = 1
        if content[0] in '+-':
            content = content[1:]
            if content[0] == '-':
                sign = -1
        num_chars = set('0123456789')
        first_nonint_index = 0
        while first_nonint_index < len(content) and content[first_nonint_index] in num_chars:
            first_nonint_index += 1
        data_str = content[:first_nonint_index]
        remaining_content = content[first_nonint_index:]
        if len(data_str) == 0:
            return 0, remaining_content
        return sign * int(content[:first_nonint_index]), remaining_content

    @staticmethod
    def split_operator_from(content):
        operator_chars = set('+-*/|&^')
        if content[0] in operator_chars:
            return content[0], content[1:]
        return None, content


def run_sr(sr_code):
    group_pattern = (
        '(?:{0}'  # A group should begin with the opening brace ({0}),
        '(?P<{2}>[^{0}{1}]*)'  # then contain a bunch of non-brace characters,
        '{1})'  # and end with a closing brace (({1}))
    )
    group_matchers = [group_pattern.format(group_type.opening, group_type.closing, group_type.name)
                      for group_type in GROUP_TYPES]
    general_matcher = re.compile('|'.join(group_matchers))
    # TODO use these matches to create groups.
    # TODO add actual execution.
    return general_matcher.findall(sr_code)