from setuptools import setup, Extension

setup(
    name='jerrymander',
    version='1.0',
    ext_modules=[Extension('jerry', ['src/kruskal.cpp'])],
    options={
        'bdist_wheel': {'universal': True}
    }
)
