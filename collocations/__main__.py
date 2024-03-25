from collocations.collocations import collocate
from collocations.patterns import LANGUAGES_PATTERNS

for language, pattern in LANGUAGES_PATTERNS.items():
    if pattern:
        collocate(language, pattern)