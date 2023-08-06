# from setuptools import setup

# setup(
#     name='ailola',
#     version=1.0,
#     license='MIT',
#     author="Elhay Efrat",
#     author_email="elhayefrat@gmail.com"
#     packages=['v'],
#     install_requires=['click', 'requests' ,'openai'],
#     entry_points={'console_scripts': ['ailola = ailola:apis']}
# )



from setuptools import setup, find_packages


setup(
    name='ailola',
    version='0.8.2',
    license='MIT',
    author="Elhay Efrat",
    author_email='elhayefrat@gmail.com',
    # packages=find_packages('ailola'),
    # package_dir={'': 'ailola'},
    package_dir = {'': 'ailola'},
    url='https://github.com/lola-pola/ailola',
    keywords='lola cli terraform ai',
    install_requires=['click', 'requests' ,'openai'],
    entry_points={'console_scripts': ['ailola = ailola:cli']}

)