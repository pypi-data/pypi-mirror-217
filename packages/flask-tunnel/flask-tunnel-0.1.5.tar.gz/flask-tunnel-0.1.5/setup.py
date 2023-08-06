from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='flask-tunnel',
    version='0.1.5',
    description='Configurable ngrok tunneling for Flask apps.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Taj Jethwani-Keyser',
    url='https://github.com/Wolfiej-k/flask-tunnel',
    py_modules=['flask_tunnel'],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=['pyngrok'],
    license='MIT'
)