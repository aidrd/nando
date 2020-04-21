"""
設定
"""
from pathlib import Path


class Config(object):
    def __init__(self):
        self.DATA_DIR = Path('data/')
        self.RESULTS_DIR = Path('results/')

        # use all synonym
        self.ALLOW_EXACT = True  # use exact synonym when map nando to mondo
        self.ALLOW_BROAD = True  # use broad synonym when map nando to mondo
        self.ALLOW_NARROW = True  # use narrow synonym when map nando to mondo
        self.ALLOW_RELATED = True  # use related synonym when map nando to mondo

        self.ALLOW_DEPRECATED = False  # use deprecated mondo when map nando to mondo
        
        self.NANDO_FRONT_PATH = self.DATA_DIR / 'nando_front.ttl'

