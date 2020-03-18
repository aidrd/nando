"""
設定
"""
from pathlib import Path


class Config(object):
    def __init__(self):
        self.DATA_DIR = Path('data/')
        self.RESULTS_DIR = Path('results/')

        # not use synonym
        # self.ALLOW_EXACT = False  # use exact synonym when map nando to mondo
        # self.ALLOW_BROAD = False  # use broad synonym when map nando to mondo
        # self.ALLOW_NARROW = False  # use narrow synonym when map nando to mondo
        # self.ALLOW_RELATED = False  # use related synonym when map nando to mondo

        # use only exact synonym
        # self.ALLOW_EXACT = True
        # self.ALLOW_BROAD = False
        # self.ALLOW_NARROW = False
        # self.ALLOW_RELATED = False

        # use all synonym
        self.ALLOW_EXACT = True  # use exact synonym when map nando to mondo
        self.ALLOW_BROAD = True  # use broad synonym when map nando to mondo
        self.ALLOW_NARROW = True  # use narrow synonym when map nando to mondo
        self.ALLOW_RELATED = True  # use related synonym when map nando to mondo

        self.ALLOW_DEPRECATED = False  # use deprecated mondo when map nando to mondo
        
        self.NANDO_FRONT_PATH = self.DATA_DIR / 'nando_front.ttl'

