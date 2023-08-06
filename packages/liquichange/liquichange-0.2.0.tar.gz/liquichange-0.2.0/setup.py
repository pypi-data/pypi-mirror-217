# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['liquichange']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'liquichange',
    'version': '0.2.0',
    'description': 'Build and modify Liquibase changelogs in Python.',
    'long_description': '# liquichange\nBuild and modify Liquibase changelogs in Python.\n\n## Installation\n\n```bash\n$ pip install liquichange\n```\n\n## Usage\n\n`liquichange` can be used to generate Liquibase XML changelogs as follows:\n\n```python\nfrom liquichange.changelog import Changelog, Changeset, CypherChange\n\n# instantiate Changelog\nchangelog = Changelog()\n\n# add Changeset with change_type neo4j:cypher to Changelog\nchangeset = Changeset(\n  id="42",\n  author="Nelson",\n  change_type=CypherChange(\n    text="MERGE (:property {handle: \'fastq_name\', model: \'GDC\'})"\n  )\n)\nchangelog.add_changeset(changeset)\n\n# write changelog to XML file\nfile_path = "path/to/file.xml"\nchangelog.save_to_file(\n  file_path=file_path,\n  encoding="UTF-8"\n)\n```\n\n## License\n\n`liquichange` is licensed under the terms of the the Apache 2.0 license.\n\nLIQUIBASE is a registered trademark of Liquibase, INC. Liquibase Open Source is released under the Apache 2.0 license.\n',
    'author': 'Nelson Moore',
    'author_email': 'nelson.moore@essential-soft.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
