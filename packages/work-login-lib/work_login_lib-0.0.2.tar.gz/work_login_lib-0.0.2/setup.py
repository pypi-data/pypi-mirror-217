from setuptools import setup, find_packages


setup(
    name="work_login_lib",
    author="shubham",
    author_email="something@test.com",
    maintainer="shubham",
    version="0.0.2",
    packages=find_packages(),
    install_requires=["pynput==1.7.6", "pytest"],
    entry_points={
        "console_scripts":[
            "wl = work_login_lib.__main__:main"]
        },
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
