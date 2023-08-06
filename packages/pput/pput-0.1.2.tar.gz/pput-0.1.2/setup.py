from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

# with open('requirements.txt', 'r') as f:
#     requirements = f.readlines()
requirements = [
    'tyro~=0.5.3',
    'setuptools~=68.0.0'
]


setup(
    name='pput',
    version='0.1.2',
    license='GPLv3',
    author='jhzg',
    author_email='jhzg02200059@163.com',
    description='Test how to use setup.py.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='pput',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    packages=['pput'],
    package_data={'': ['py.typed', 'README.md', 'LICENSE', 'requirements.txt']},
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pput = pput.main:main',
        ],
    }
)
