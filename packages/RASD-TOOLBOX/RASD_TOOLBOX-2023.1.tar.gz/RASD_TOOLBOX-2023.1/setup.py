from setuptools import setup

setup(
    	name = 'RASD_TOOLBOX',
    	version = '2023.1',
        description = 'The RASDpy is an easy-to-use environment for applying probabilistic modeling.',
    	license = 'Apache License',
        author = ['Wanderlei Malaquias Pereira Junior', 'Donizetti Aparecido de Souza Junior', 'Romes Antônio Borges'],
    	author_email = 'wanderlei_junior@ufcat.edu.br',
    	packages = ['RASD_TOOLBOX'],
    	classifiers = ["Programming Language :: Python","Topic :: Scientific/Engineering :: Mathematics", "Topic :: Scientific/Engineering"],
    	install_requires = ["numpy", "scipy", "json", "time", "pandas"]
     )

