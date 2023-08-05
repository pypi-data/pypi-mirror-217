from setuptools import setup

setup(
   name='agentlayer',
   version='0.1',
   description='Agent Layer',
   author='Delip Rao',
   author_email='deliprao@gmail.com',
   packages=['agentlayer'],  #same as name
   install_requires=['openai'], # External packages as dependencies
)
