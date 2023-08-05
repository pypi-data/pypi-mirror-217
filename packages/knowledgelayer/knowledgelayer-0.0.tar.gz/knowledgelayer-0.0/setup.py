from setuptools import setup

setup(
   name='knowledgelayer',
   version='0.0',
   description='Knowledge Layer',
   author='Delip Rao',
   author_email='deliprao@gmail.com',
   packages=['knowledgelayer'],  #same as name
   install_requires=['openai'], # External packages as dependencies
)
