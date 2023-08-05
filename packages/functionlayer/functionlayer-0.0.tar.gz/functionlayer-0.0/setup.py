from setuptools import setup

setup(
   name='functionlayer',
   version='0.0',
   description='Agent Layer',
   author='Delip Rao',
   author_email='deliprao@gmail.com',
   packages=['functionlayer'],  #same as name
   install_requires=['openai'], # External packages as dependencies
)
