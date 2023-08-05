from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='redashsync',
    version='0.0.8',
    description='A tool integrating Redash with Slack',
    long_description = long_description,
    long_description_content_type='text/markdown',
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