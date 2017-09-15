from foremast.runner import ForemastRunner
from foremast import consts
import gogoutils

class RunnerApi(ForemastRunner):
    def __init__(self, **kwargs):
        """Setup the Runner for all Foremast modules."""
        self.email = kwargs.get('email')
        self.group = kwargs.get('group')
        self.repo = kwargs.get("repo")
        self.runway_dir = kwargs.get("runway_dir")

        self.git_project = "{}/{}".format(self.group, self.repo)
        parsed = gogoutils.Parser(self.git_project)
        generated = gogoutils.Generator(*parsed.parse_url(), formats=consts.APP_FORMATS)

        self.app = generated.app_name()
        self.trigger_job = generated.jenkins()['name']
        self.git_short = generated.gitlab()['main']

        self.raw_path = "/tmp/raw.properties"
        self.json_path = self.raw_path + ".json"
        self.configs = None