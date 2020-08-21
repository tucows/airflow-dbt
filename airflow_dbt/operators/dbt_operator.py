from airflow_dbt.hooks.dbt_hook import DbtCliHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DbtBaseOperator(BaseOperator):
    """
    Base dbt operator
    All other dbt operators are derived from this operator.

    :param profiles_dir: If set, passed as the `--profiles-dir` argument to the `dbt` command
    :type profiles_dir: str
    :param target: If set, passed as the `--target` argument to the `dbt` command
    :type dir: str
    :param dir: The directory to run the CLI in
    :type vars: str
    :param vars: If set, passed as the `--vars` argument to the `dbt` command
    :type vars: dict
    :param full_refresh: If `True`, will fully-refresh incremental models.
    :type full_refresh: bool
    :param models: If set, passed as the `--models` argument to the `dbt` command
    :type models: str
    :param exclude: If set, passed as the `--exclude` argument to the `dbt` command
    :type exclude: str
    :param dbt_bin: The `dbt` CLI. Defaults to `dbt`, so assumes it's on your `PATH`
    :type dbt_bin: str
    :param verbose: The operator will log verbosely to the Airflow logs
    :type verbose: bool
    """

    ui_color = '#d6522a'

    template_fields = ['vars']

    @apply_defaults
    def __init__(self,
                 profiles_dir=None,
                 target=None,
                 dir='.',
                 vars=None,
                 models=None,
                 exclude=None,
                 dbt_bin='dbt',
                 verbose=True,
                 full_refresh=False,
                 data_test=False,
                 schema_test=False,
                 *args,
                 **kwargs):
        super(DbtBaseOperator, self).__init__(*args, **kwargs)

        self.profiles_dir = profiles_dir
        self.target = target
        self.dir = dir
        self.vars = vars
        self.models = models
        self.full_refresh = full_refresh
        self.data_test = data_test
        self.schema_test = schema_test
        self.exclude = exclude
        self.dbt_bin = dbt_bin
        self.verbose = verbose
        self.create_hook()

    def create_hook(self):
        self.hook = DbtCliHook(
            profiles_dir=self.profiles_dir,
            target=self.target,
            dir=self.dir,
            vars=self.vars,
            full_refresh=self.full_refresh,
            data_test=self.data_test,
            schema_test=self.schema_test,
            models=self.models,
            exclude=self.exclude,
            dbt_bin=self.dbt_bin,
            verbose=self.verbose)

        return self.hook


class DbtRunOperator(DbtBaseOperator):
    @apply_defaults
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtRunOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)

    def execute(self, context):
        self.create_hook().run_cli('run')


class DbtTestOperator(DbtBaseOperator):
    @apply_defaults
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtTestOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)

    def execute(self, context):
        self.create_hook().run_cli('test')


class DbtDocsGenerateOperator(DbtBaseOperator):
    @apply_defaults
    def __init__(self, profiles_dir=None, target=None, *args, **kwargs):
        super(DbtDocsGenerateOperator, self).__init__(profiles_dir=profiles_dir, target=target, *args, **kwargs)
        
    def execute(self, context):
        self.create_hook().run_cli('docs', 'generate')