from setuptools import setup, find_packages

description = 'My first Python package'

setup(
	name="datapeachcli_2",
	version="0.0.1",
	author="GeeksforGeeks",
	author_email="contact@gfg.com",
	 packages=find_packages(),
	description="A sample test package",
	long_description=description,
	long_description_content_type="text/markdown",
	url="https://github.com/gituser/test-tackage",
	license='MIT',
	python_requires='>=3.8',
	install_requires=[]
)
