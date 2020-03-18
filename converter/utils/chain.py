import re
from typing import List, Union

from cnorm.chain import Chain
from cnorm.rule import Rule, Greek2Alpha, Lower


class RemovePatterns(Rule):
    def __init__(self, patterns: List[Union[str, re.Pattern]]):
        super(RemovePatterns, self).__init__()
        self.patterns = patterns

    def apply(self, text: str):
        for pattern in self.patterns:
            if type(pattern) == str:
                text = text.replace(pattern, '')
            elif type(pattern) == re.Pattern:
                text = pattern.sub('', text)
            else:
                raise TypeError('patterns should be list of str or re.Pattern')
        return text


class ReplacePatterns(Rule):
    # TODO: 要修正
    def __init__(self, patterns: List[Union[str, re.Pattern]]):
        super(ReplacePatterns, self).__init__()
        self.patterns = patterns

    def apply(self, text: str):
        for before, after in self.patterns:
            if type(before) == str:
                text = text.replace(before, after)
            elif type(before) == re.Pattern:
                text = before.sub(after, text)
            else:
                raise TypeError('patterns should be list of str or re.Pattern')
        return text


special_spaces = [
    ['\xa0', ' '],
    ['\u3000', ' ']
]
rule_replace_special_spaces = ReplacePatterns(special_spaces)

rule_replace_greek = Greek2Alpha()

roman_nums = [
    ['VIII', '8'],
    ['VII', '7'],
    ['VI', '6'],
    ['IV', '4'],
    ['V', '5'],
    ['IX', '9'],
    ['X', '10'],
    ['III', '3'],
    ['II', '2'],
    ['I', '1'],
]
rule_replace_roman = ReplacePatterns(roman_nums)

rule_lower = Lower()


posesses = ["'s"]
rule_remove_posesses = RemovePatterns(posesses)

stop_words = [
    'types', 'type', 'diseases', 'disease', 'syndromes', 'syndrome', 'disorders', 'disorder',
    'of', 'with', 'at', 'from', 'in', 'among', 'upon', 'to', 'in', 'for', 'on', 'by', 'and',
]
rule_remove_stop_words = RemovePatterns(stop_words)

re_alunum = [re.compile('\W+')]
rule_remove_expect_alnum = RemovePatterns(re_alunum)

chain = Chain([
    rule_replace_special_spaces,
    rule_replace_greek,
    rule_replace_roman,
    rule_lower,
    rule_remove_posesses,
    rule_remove_stop_words,
    rule_remove_expect_alnum,
])
