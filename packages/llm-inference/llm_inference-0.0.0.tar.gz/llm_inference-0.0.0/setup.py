from setuptools import setup


def get_requirements(file):
    with open(file) as f:
        required = f.read().splitlines()
    return required


required = get_requirements("requirements/requirements.txt")
chatbot_required = get_requirements("requirements/chatbot.txt")
extras = {"chatbot": chatbot_required}

setup(install_requires=required, extras_require=extras)
