from setuptools import setup, find_packages
import os


VERSION = __import__("sites_ext").__version__

setup(
    name="django-sites-ext",
    description="Utilities to make administration of content belonging to different sites easier.",
    long_description=open(os.path.join(os.path.dirname(__file__), 
        'README.rst')).read(),
    version=VERSION,
    author="Bojan Mihelac",
    author_email="bmihelac@mihelac.org",
    url="https://github.com/bmihelac/django-sites-ext",
    license = 'BSD',
    install_requires = [
        'Django>=1.3',
    ],
    classifiers = ['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   "Topic :: Internet :: WWW/HTTP"
                   ],
    packages=find_packages(exclude=["example", "example.*"]),
)

