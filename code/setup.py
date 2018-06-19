import setuptools

__version__ = '0.1'

config = {
    'name': 'places',
    'author': 'Mekan ALLABERDIYEV <mekan.allaberdi@gmail.com>',
    'author_email': 'mekan.allaberdi@gmail.com',
    'version': __version__,
    'install_requires': ['flask', 'requests', 'flask_restful'],
    'tests_require': ['nose'],
    'include_package_data': True,
    'zip_safe': False,
    'scripts': [],
    'entry_points': {
        'console_scripts': [
            'main=places_api.app:run_app',
        ]
    }
}

print('Places Version: %s' % __version__)

packages = setuptools.find_packages()
config['packages'] = packages
setuptools.setup(**config)
