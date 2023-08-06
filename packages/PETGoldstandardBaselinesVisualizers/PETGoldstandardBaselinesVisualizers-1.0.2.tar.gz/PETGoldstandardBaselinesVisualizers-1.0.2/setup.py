from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
        name='PETGoldstandardBaselinesVisualizers',
        version='1.0.2',
        packages=['Visualizers'],
        url='https://huggingface.co/datasets/patriziobellan/PET',
        license='MIT',
        author='Patrizio Bellan',
        author_email='patrizio.bellan@gmail.com',
        description='Visualizers of the PET dataset goldstandard data and baselines prediction',
install_requires=['numpy~=1.25.0',
'PETAnnotationDataset~=0.0.1a3',
'Pillow~=10.0.0',
'matplotlib~=3.7.1',
'requests~=2.31.0'],
long_description=long_description,
    long_description_content_type='text/markdown'
)
