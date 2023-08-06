from setuptools import setup, find_packages

setup(
    name='sebastian_test',
    version='0.1.0',
    description='Description of your package',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'sebastian_test': [
		'SwissArmyTransformer.tar.gz',
		'GLM-130B.tar.gz',
                'ice_text.model'
	],
    },
)
