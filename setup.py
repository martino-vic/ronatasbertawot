from setuptools import setup


setup(
    name='cldfbench_ronatasbertawot',
    py_modules=['cldfbench_ronatasbertawot'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'ronatasbertawot=cldfbench_ronatasbertawot:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
