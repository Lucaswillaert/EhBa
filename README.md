# EhBa

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Node.js Version](https://img.shields.io/badge/node.js-22.0.0-green.svg)](https://nodejs.org/en/download/)
[![Docker Compose](https://img.shields.io/badge/docker%20compose-3.12-blue)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

EhBa is a school project developed for the 'AI Essentials' course at Erasmushogeschool Brussel. The project leverages the power of Azure's OpenAI model to answer questions about Erasmushogeschool Brussel. It does this by indexing data from the EhB website and processing requests through an Azure Function App.

---

## Table of Contents

- [Contributors](#contributors)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

---

## Contributors

This project was created by:

- Gill Mertens - [gill.mertens@student.ehb.be](mailto:gill.mertens@student.ehb.be)
- Lucas Willaert - [lucas.willaert@student.ehb.be](mailto:lucas.willaert@student.ehb.be)

---

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of Node.js and Python.
* You have a `<Windows/Linux/Mac>` machine. State which OS is supported/which is not.

---

## Environment Variables

This project uses environment variables for configuration. These are stored in a `.env` file. For security reasons, this file is not included in the repository.

To obtain the `.env` file or its contents, please contact us at:

- Gill Mertens - [gill.mertens@student.ehb.be](mailto:gill.mertens@student.ehb.be)
- Lucas Willaert - [lucas.willaert@student.ehb.be](mailto:lucas.willaert@student.ehb.be)

---

## Installation

To install EhBa, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Lucaswillaert/EhBa.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ./EhBa
    ```

3. Install the required Node.js packages:
    ```bash
    npm install
    ```

4. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

To use EhBa, follow these steps:

1. Build the Tailwind CSS file:
    ```bash
    npx tailwindcss -i ./static/src/input.scss -o ./static/dist/css/output.css --watch
    ```

2. Build and start the Docker containers:
    ```bash
    docker compose up --build -d
    ```

---

## Contact

If you want to contact us you can reach us at `lucas.willaert@student.ehb.be` or `gill.mertens@student.ehb.be`.