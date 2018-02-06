from setuptools import setup, find_packages
import maccabistats_web

setup(
    name='maccabistats_web',
    version=maccabistats_web.version,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Maccabi tel-aviv football team statistics manipulation web-site',
    python_requires='>=3',
    install_requires=["maccabistats==1.3.0",
                      "flask==0.12.2",
                      "python-dateutil==2.6.1"]
)
