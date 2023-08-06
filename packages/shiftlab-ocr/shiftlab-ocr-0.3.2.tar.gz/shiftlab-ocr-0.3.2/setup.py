import setuptools


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='shiftlab-ocr',
    version='0.3.2',
    description='SHIFT OCR is a library for handwriting text segmentation and character recognition.',
    long_description=long_description,
    url='https://github.com/konverner/shiftlab_ocr',
    long_description_content_type="text/markdown",
    keywords="data,computer vision,handwriting,doc2text",
    author='Konstantin Verner',
    author_email='konst.verner@gmail.com',
    license='MIT',
    python_requires='>=3.6',
    package_dir={"": "src"},
    include_package_data=True,
    packages=setuptools.find_packages("src"),
    package_data={'generator': ['content/*.png', 'content/*.otf', 'content/*.ttf']},
    install_requires=['opencv-python',
                      'torch>=1.11.0',
                      'torchvision>=0.12.0',
                      'Pillow>=7.1.2',
                      'PyYAML>=6.0'
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)