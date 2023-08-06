
from setuptools import setup, find_packages


setup(name='chatglm-cli',
    version='0.2.1',
    description='chatglm llm cli',
    url='https://github.com/xxx',
    author='auth',
    author_email='xxx@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    # extras_require={
    #     "all": [
    #         # 'sentence_transformers',
    #         # 'tensorboard',
    #         # "protobuf",
    #         # "fschat==0.2.2",
    #         # "cpm_kernels",
    #         # "mdtex2html",
    #         # "sentencepiece",
    #         # "accelerate",
    #         # "scikit-learn",
    #         # 'torch',    
    #         # 'transformers',
    #     ],
    # },
    install_requires=[
        # 'requests',
        # 'termcolor',
        # 'tqdm',
        # 'gptcache',
        # 'numpy',
        # 'pypdf',
        # "scikit-learn",
        # 'langchain',
        # 'websockets',
        # 'websocket-client',
        'gradio',
        'chatglm-llm>=1.4.4',
        # 'unstructured',
        # 'aiowebsocket',
        ],
    entry_points={
        'console_scripts': [
            'ai-cli=chatglmcli.cmd:main',
        ]
    },

)
