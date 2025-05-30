from setuptools import setup, find_packages

setup(
    name="rgs-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "Flask-SQLAlchemy==3.0.5",
        "Flask-Migrate==4.0.5",
        "Flask-Login==0.6.3",
        "Flask-CORS==4.0.0",
        "Flask-JWT-Extended==4.5.3",
        "python-dotenv==1.0.0",
        "psycopg2-binary==2.9.7",
        "Werkzeug==2.3.7",
        "marshmallow==3.19.0",
        "flask-marshmallow==0.15.0",
        "marshmallow-sqlalchemy==0.29.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.2",
            "pytest-flask==1.2.0",
            "pytest-cov==4.1.0",
            "factory-boy==3.3.0",
            "python-decouple==3.8",
        ]
    },
    python_requires=">=3.11",
) 