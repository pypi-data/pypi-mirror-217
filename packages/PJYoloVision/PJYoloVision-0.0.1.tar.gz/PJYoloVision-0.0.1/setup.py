from setuptools import setup, find_packages

setup(
    name='PJYoloVision',
    version='0.0.1',
    author='Erfan Zare Chavoshi',
    author_email='erfanzare82@eyahoo.com',
    description="""
    The object detection models in PJYoloVision can detect and locate objects in real-time images and video streams. 
    These models can be trained to detect specific types of objects, such as cars, people, animals,
     or any other object of interest. The YOLO models are known for being fast and accurate, 
     making them a good choice for real-time applications.
     PJYoloVision Implement this algorithm in Jax/Flax/Pytorch""",
    url='https://github.com/erfanzar/PJYoloVision',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='machine learning, deep learning, pytorch',
    install_requires=[
        'torch>=1.13.0',
        # add any other required dependencies here
    ],
    python_requires='>=3.8',
)
