from setuptools import setup, find_packages

version = '0.1.1'

setup(
    name='callllm',
    version=version,
    description='Asynchronous, concurrent requests to the LLM REST APIs.',
    long_description='Asynchronous, concurrent requests to the LLM REST APIs, that respect their rate limits, using gevent and requests.',
    author='Zhensu Sun',
    author_email='zhensuuu@gmail.com',
    url='https://github.com/v587su/CallLLM',
    packages=find_packages(),
    install_requires=['gevent==0.13.7', 'greenlet==0.4.0', 'requests==0.13.7'],
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
    keywords=['requests', 'python-requests', 'gevent', 'llm'],
    zip_safe=False,
)