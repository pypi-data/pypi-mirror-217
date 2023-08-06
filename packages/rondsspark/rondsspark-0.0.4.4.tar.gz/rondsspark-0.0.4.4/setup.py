from setuptools import setup, find_packages

# noinspection SpellCheckingInspection
setup(
    name='rondsspark',
    version='0.0.4.4',
    description='ronds spark sdk',
    author='dongyunlong',
    author_email='yunlong.dong@ronds.com.cn',
    install_requires=['pyspark', 'cassandra-driver', 'pandas', 'pyYAML',
                      'schedule', 'wheel', 'findspark', 'importlib_resources'],
    package_data={
        '': ['logging_config.yml'],
    },
    packages=find_packages(),
    license='apache 3.0',
)
