from foremast.runner import ForemastRunner
from foremast import consts
import gogoutils

class RunnerApi(ForemastRunner):
    def __init__(self, **kwargs):
        """Setup the Runner for all Foremast modules."""
        self.email = kwargs.get('owner_email')
        self.group = kwargs.get('group')
        self.repo = kwargs.get("repo")
        self.runway_dir = kwargs.get("runway_dir")
        self.env = kwargs.get("env")
        self.region = kwargs.get("region")
        self.artifact_path = kwargs.get("artifacts_path")
        self.artifact_version = kwargs.get("artifact_version")
        self.promote_stage = kwargs.get("promote_stage", "latest")

        self.git_project = "{}/{}".format(self.group, self.repo)
        parsed = gogoutils.Parser(self.git_project)
        generated = gogoutils.Generator(*parsed.parse_url(), formats=consts.APP_FORMATS)

        self.app = generated.app_name()
        self.trigger_job = generated.jenkins()['name']
        self.git_short = generated.gitlab()['main']

        self.raw_path = "/tmp/raw.properties"
        self.json_path = self.raw_path + ".json"
        self.configs = None