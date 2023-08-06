from setuptools import setup, find_packages

setup(
    name='studentProfile',
    version='0.0.4',
    description='Database entry for student profile',
    author='Sonarjit',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create_table=studentProfile.create_table:create_table',
            'delete_values=studentProfile.delete:delete_values',
            'display_values=studentProfile.display:display_values',
            'drop_table=studentProfile.drop_table:drop_table',
            'insert_values=studentProfile.insert:insert_values',
            'update_values=studentProfile.update:update_values',

        ],
    }
)
