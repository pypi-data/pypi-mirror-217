from setuptools import setup, find_packages
import os
version_list = []
data_list = ['resources/*']
for version in version_list:
    for dir_ in os.listdir(f'simulator/gate_sets/{version}/gates/'):
        if dir_[0] != '.':  # not adding .DS_store
            data_list.append(f'gate_sets/{version}/gates/{dir_}/*')

setup(
    include_package_data=True,
    version='1.0.0',
    name='skyrmions',
    install_requires=['numpy',
                      'matplotlib',
                      'opencv-python',
                      'graphviz',
                      ],
    packages=find_packages(),
    package_data={'': data_list}
)
# version 0.0.4: saved memory leak by removing the saved list of regions
# version 0.0.5: added junctionur and junctionul gates
# version 0.0.6 added piecewise simulation files
# version 0.0.7 added test and gate order functionality to helper.py
# version 0.0.8 bug fix: empty gate did set outputs as zero. It shouldn't it is fixed
# version 0.0.9 added gates version3 with 1200px size and 7ns transfer gate- added the piecewise scheduler
# version 1.0.0 added the version4 of gates with gate names consistent with the thesis terminology
