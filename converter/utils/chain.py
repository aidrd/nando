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
    [re.compile('^VIII$'), '8'],
    [re.compile('^VII$'), '7'],
    [re.compile('^VI$'), '6'],
    [re.compile('^IV$'), '4'],
    [re.compile('^V$'), '5'],
    [re.compile('^IX$'), '9'],
    [re.compile('^X$'), '10'],
    [re.compile('^III$'), '3'],
    [re.compile('^II$'), '2'],
    [re.compile('^I$'), '1'],
]
rule_replace_roman = ReplacePatterns(roman_nums)

rule_lower = Lower()


posesses = ["'s"]
rule_remove_posesses = RemovePatterns(posesses)

stop_words = [
    re.compile('^types$'), 
    re.compile('^type$'),
    re.compile('^diseases$'),
    re.compile('^disease$'),
    re.compile('^syndromes$'),
    re.compile('^syndrome$'),
    re.compile('^disorders$'),
    re.compile('^disorder$'),
    re.compile('^of$'),
    re.compile('^with$'),
    re.compile('^at$'),
    re.compile('^from$'),
    re.compile('^in$'),
    re.compile('^among$'),
    re.compile('^upon$'),
    re.compile('^to$'),
    re.compile('^in$'),
    re.compile('^for$'),
    re.compile('^on$'),
    re.compile('^by$'),
    re.compile('^and$'),
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
