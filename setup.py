from setuptools import setup, find_packages

setup(
    name="library-api",
    version="1.0.0",
    author="Library API Developer",
    description="A FastAPI-based library management system",
    packages=find_packages(include=['src', 'src.*']),
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "sqlalchemy>=1.4.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
        "alembic>=1.7.7",
        "python-dotenv>=0.19.0",
        "email-validator>=1.1.3",
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.5',
            'pytest-cov>=2.12.0',
            'black>=21.5b2',
            'isort>=5.9.1',
        ]
    },
)
