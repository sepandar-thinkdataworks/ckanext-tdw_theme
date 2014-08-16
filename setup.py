from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-tdw_theme',
    version=version,
    description="",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.tdw_theme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        # myplugin=ckanext.tdw_theme.plugin:PluginClass
	tdw_theme = ckanext.tdw_theme.plugin:TDWThemePlugin
	tdw_theme_extra_pages=ckanext.tdw_theme.plugin:TDWThemeExtraPagesPlugin
    ''',
)
