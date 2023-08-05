# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qwak_sdk',
 'qwak_sdk.commands',
 'qwak_sdk.commands.admin',
 'qwak_sdk.commands.admin.apikeys',
 'qwak_sdk.commands.admin.apikeys.generate',
 'qwak_sdk.commands.admin.apikeys.revoke',
 'qwak_sdk.commands.audience',
 'qwak_sdk.commands.audience._logic',
 'qwak_sdk.commands.audience._logic.config',
 'qwak_sdk.commands.audience._logic.config.v1',
 'qwak_sdk.commands.audience.create',
 'qwak_sdk.commands.audience.delete',
 'qwak_sdk.commands.audience.get',
 'qwak_sdk.commands.audience.list',
 'qwak_sdk.commands.audience.update',
 'qwak_sdk.commands.auto_scalling',
 'qwak_sdk.commands.auto_scalling._logic',
 'qwak_sdk.commands.auto_scalling._logic.config',
 'qwak_sdk.commands.auto_scalling.attach',
 'qwak_sdk.commands.automations',
 'qwak_sdk.commands.automations.delete',
 'qwak_sdk.commands.automations.executions',
 'qwak_sdk.commands.automations.executions.list',
 'qwak_sdk.commands.automations.list',
 'qwak_sdk.commands.automations.register',
 'qwak_sdk.commands.feature_store',
 'qwak_sdk.commands.feature_store.delete',
 'qwak_sdk.commands.feature_store.list',
 'qwak_sdk.commands.feature_store.pause',
 'qwak_sdk.commands.feature_store.register',
 'qwak_sdk.commands.feature_store.resume',
 'qwak_sdk.commands.feature_store.trigger',
 'qwak_sdk.commands.models',
 'qwak_sdk.commands.models._logic',
 'qwak_sdk.commands.models.build',
 'qwak_sdk.commands.models.build._logic',
 'qwak_sdk.commands.models.build._logic.client_logs',
 'qwak_sdk.commands.models.build._logic.config',
 'qwak_sdk.commands.models.build._logic.constant',
 'qwak_sdk.commands.models.build._logic.interface',
 'qwak_sdk.commands.models.build._logic.phase',
 'qwak_sdk.commands.models.build._logic.phase.a_fetch_model_code',
 'qwak_sdk.commands.models.build._logic.phase.a_fetch_model_code.fetch_model_step',
 'qwak_sdk.commands.models.build._logic.phase.a_fetch_model_code.fetch_model_step.fetch_strategy_manager',
 'qwak_sdk.commands.models.build._logic.phase.a_fetch_model_code.fetch_model_step.fetch_strategy_manager.strategy',
 'qwak_sdk.commands.models.build._logic.phase.a_fetch_model_code.fetch_model_step.fetch_strategy_manager.strategy.folder',
 'qwak_sdk.commands.models.build._logic.phase.a_fetch_model_code.fetch_model_step.fetch_strategy_manager.strategy.git',
 'qwak_sdk.commands.models.build._logic.phase.a_fetch_model_code.fetch_model_step.fetch_strategy_manager.strategy.zip',
 'qwak_sdk.commands.models.build._logic.phase.b_remote_register_qwak_build',
 'qwak_sdk.commands.models.build._logic.phase.c_deploy',
 'qwak_sdk.commands.models.build._logic.util',
 'qwak_sdk.commands.models.builds',
 'qwak_sdk.commands.models.builds.cancel',
 'qwak_sdk.commands.models.builds.logs',
 'qwak_sdk.commands.models.builds.status',
 'qwak_sdk.commands.models.create',
 'qwak_sdk.commands.models.delete',
 'qwak_sdk.commands.models.deployments',
 'qwak_sdk.commands.models.deployments.deploy',
 'qwak_sdk.commands.models.deployments.deploy._logic',
 'qwak_sdk.commands.models.deployments.deploy.batch',
 'qwak_sdk.commands.models.deployments.deploy.batch._logic',
 'qwak_sdk.commands.models.deployments.deploy.realtime',
 'qwak_sdk.commands.models.deployments.deploy.realtime._logic',
 'qwak_sdk.commands.models.deployments.deploy.streaming',
 'qwak_sdk.commands.models.deployments.deploy.streaming._logic',
 'qwak_sdk.commands.models.deployments.undeploy',
 'qwak_sdk.commands.models.deployments.undeploy._logic',
 'qwak_sdk.commands.models.executions',
 'qwak_sdk.commands.models.executions.cancel',
 'qwak_sdk.commands.models.executions.report',
 'qwak_sdk.commands.models.executions.start',
 'qwak_sdk.commands.models.executions.status',
 'qwak_sdk.commands.models.init',
 'qwak_sdk.commands.models.init._logic',
 'qwak_sdk.commands.models.init._logic.template',
 'qwak_sdk.commands.models.init._logic.template.churn',
 'qwak_sdk.commands.models.init._logic.template.churn.{{cookiecutter.model_directory}}',
 'qwak_sdk.commands.models.init._logic.template.churn.{{cookiecutter.model_directory}}.main',
 'qwak_sdk.commands.models.init._logic.template.churn.{{cookiecutter.model_directory}}.tests',
 'qwak_sdk.commands.models.init._logic.template.churn.{{cookiecutter.model_directory}}.tests.it',
 'qwak_sdk.commands.models.init._logic.template.credit_risk',
 'qwak_sdk.commands.models.init._logic.template.credit_risk.{{cookiecutter.model_directory}}',
 'qwak_sdk.commands.models.init._logic.template.credit_risk.{{cookiecutter.model_directory}}.main',
 'qwak_sdk.commands.models.init._logic.template.general',
 'qwak_sdk.commands.models.init._logic.template.general.{{cookiecutter.model_directory}}',
 'qwak_sdk.commands.models.init._logic.template.general.{{cookiecutter.model_directory}}.{{cookiecutter.main_directory}}',
 'qwak_sdk.commands.models.init._logic.template.general.{{cookiecutter.model_directory}}.{{cookiecutter.test_directory}}',
 'qwak_sdk.commands.models.init._logic.template.titanic',
 'qwak_sdk.commands.models.init._logic.template.titanic.{{cookiecutter.model_directory}}',
 'qwak_sdk.commands.models.init._logic.template.titanic.{{cookiecutter.model_directory}}.main',
 'qwak_sdk.commands.models.init._logic.template.titanic.{{cookiecutter.model_directory}}.tests',
 'qwak_sdk.commands.models.init._logic.template.titanic.{{cookiecutter.model_directory}}.tests.it',
 'qwak_sdk.commands.models.init._logic.template.titanic_poetry',
 'qwak_sdk.commands.models.init._logic.template.titanic_poetry.{{cookiecutter.model_directory}}',
 'qwak_sdk.commands.models.init._logic.template.titanic_poetry.{{cookiecutter.model_directory}}.main',
 'qwak_sdk.commands.models.init._logic.template.titanic_poetry.{{cookiecutter.model_directory}}.tests',
 'qwak_sdk.commands.models.init._logic.template.titanic_poetry.{{cookiecutter.model_directory}}.tests.it',
 'qwak_sdk.commands.models.list',
 'qwak_sdk.commands.models.runtime',
 'qwak_sdk.commands.models.runtime.feedback',
 'qwak_sdk.commands.models.runtime.logs',
 'qwak_sdk.commands.models.runtime.traffic_update',
 'qwak_sdk.commands.models.runtime.traffic_update._logic',
 'qwak_sdk.commands.models.runtime.update',
 'qwak_sdk.commands.projects',
 'qwak_sdk.commands.projects.create',
 'qwak_sdk.commands.projects.delete',
 'qwak_sdk.commands.projects.list',
 'qwak_sdk.commands.secrets',
 'qwak_sdk.commands.secrets.delete',
 'qwak_sdk.commands.secrets.get',
 'qwak_sdk.commands.secrets.set',
 'qwak_sdk.common',
 'qwak_sdk.common.run_config',
 'qwak_sdk.exceptions',
 'qwak_sdk.inner',
 'qwak_sdk.inner.tools',
 'qwak_sdk.inner.tools.logger',
 'qwak_sdk.tools']

package_data = \
{'': ['*']}

install_requires = \
['assertpy>=1.1,<2.0',
 'cookiecutter',
 'gitpython>=2.1.0',
 'pydantic<2',
 'python-json-logger>=2.0.2',
 'qwak-core==0.0.113',
 'qwak-inference==0.1.4',
 'tabulate>=0.8.0',
 'yaspin>=2.0.0']

extras_require = \
{'batch': ['boto3>=1.24.116,<2.0.0',
           'joblib>=1.1.0,<2.0.0',
           'pyarrow>=6.0.0,<11.0.0'],
 'batch:python_full_version >= "3.7.1" and python_version < "3.8"': ['pandas<1.4',
                                                                     'pandas<1.4'],
 'batch:python_version >= "3.8" and python_version < "3.10"': ['pandas>=1.4.3,<2.0.0',
                                                               'pandas>=1.4.3,<2.0.0'],
 'feedback': ['boto3>=1.24.116,<2.0.0', 'joblib>=1.1.0,<2.0.0'],
 'feedback:python_full_version >= "3.7.1" and python_version < "3.8"': ['pandas<1.4',
                                                                        'pandas<1.4'],
 'feedback:python_version >= "3.8" and python_version < "3.10"': ['pandas>=1.4.3,<2.0.0',
                                                                  'pandas>=1.4.3,<2.0.0']}

entry_points = \
{'console_scripts': ['qwak = qwak_sdk.main:qwak_cli']}

setup_kwargs = {
    'name': 'qwak-sdk',
    'version': '0.5.9',
    'description': 'Qwak SDK and CLI for qwak models',
    'long_description': '# Qwak SDK\n\nQwak is an end-to-end production ML platform designed to allow data scientists to build, deploy, and monitor their models in production with minimal engineering friction.\n',
    'author': 'Qwak',
    'author_email': 'info@qwak.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
