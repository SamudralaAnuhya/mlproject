from setuptools import setup, find_packages

def get_requirements(file_path: str) -> list[str]:  # function to read requirements.txt and return as list
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]  # every new line will have \n
        if "-e ." in requirements:
            requirements.remove("-e .")  # removing -e . from requirements
    return requirements


setup(
    name='mlproject',
    version='0.0.1',  # Add a version to your project
    packages=find_packages(),
    author='Anu',
    author_email='sgn.anuhya@gmail.com',
    install_requires=get_requirements('requirements.txt')  # Uncomment this to automatically load dependencies
)
