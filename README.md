<h3 align="center">Gmail Scripts</h3>

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Gmail scripts for automating mailbox actions
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Deployment](#deployment)
- [Built Using](#built_using)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

Automation scripts for handling mailbox actions
Script currently available:
- Auto read mailboxes

## 🏁 Getting Started <a name = "getting_started"></a>

Create a .env and pass the following variables in it:
- ```ROLE_ARN```
- ```SESSION_NAME```
- ```SECRET_NAME```
- ```IMAGE_NAME```
- ```AWS_ACCOUNT```

See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.

- ```Docker```
- ```Python```
- ```Pipenv for local```

### Installing

A step by step series of examples that tell you how to get a development env running.

Say what the step will be

```pipenv install```

## 🎈 Usage <a name="usage"></a>

```pipenv run python gmail_read_all_emails.py```

## 🚀 Deployment <a name = "deployment"></a>

Add additional notes about how to deploy this on a live system.

```make deploy```

This will push the image to the AWS ECR and auto deploy the code/configuration to a lambda.

## ✍️ Authors <a name = "authors"></a>

- [@ZisisKostakakis](https://github.com/ZisisKostakakis) - Idea & Initial work