from setuptools import setup, find_packages

setup(
    name='redashsync',
    version='0.0.7',
    description='A tool integrating Redash with Slack',
    author='Yun',
    author_email='ysjhmtb@gmail.com',
    url='',
    install_requires=['PyYAML', 'requests', 'seaborn', 'slack_sdk', 'cron_converter'],
    packages=find_packages(exclude=[]),
    keywords=['Redash', 'Slack'],
    python_requires='>=3.11',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.11'
    ]
)