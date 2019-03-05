#!/usr/bin/env python
import re
import sys
from git import Repo


ROLE_REGEX = r'^[a-zA-Z][\.\-a-zA-Z0-9]+$'

role = '{{ cookiecutter.role }}'

if not re.match(ROLE_REGEX, role):
    print('ERROR: %s is not an approved role name!' % role)

    # exits with status 1 to indicate failure
    sys.exit(1)

# repo = Repo(self.rorepo.working_tree_dir)
# assert not repo.bare
