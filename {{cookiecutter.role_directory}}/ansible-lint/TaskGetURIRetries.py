from ansiblelint import AnsibleLintRule


class TaskGetURIRetries(AnsibleLintRule):
    id = 'SHAKEY0001'
    shortdesc = 'All get_uri tasks should use the retries option'
    description = 'All get_uri tasks should use the retries option'
    tags = ['reliability']

    def matchtask(self, file, task):
        if task['action']['__ansible_module__'] == 'get_url':
            if 'retries' not in task:
                return True
        else:
            return False
