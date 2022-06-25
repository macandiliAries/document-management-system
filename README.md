# Document Management System
- This is a library-like system written in Python as a practice in learning the Flask framework.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)

## Overview
- The system is composed of four modules:
    - **Login**
        - Contains the login page which contains the logic related to user authentication.
        - There are two types of user role:
            - Admin
            - Super Admin
    - **Users**
        - This is a page where:
            - Admins can:
                - Update their own personal details.
                - Search for any user.
                - Filter users based on user role.
                - Reset passwords for any user.
            - Super Admins can:
                - Perform all privileges granted to Admins.
                - Create a new user.
                - Edit personal details of other users.
                - Deactivate a user account.
    - **Documents**
        - This is a page where:
            - Admins can:
                - Search for documents.
                - Filter documents based on:
                    - Document Type
                    - Document Status
                - Create/edit documents _(using a WYSIWYG editor)_.
                - View existing documents.
                - Submit a document for approval of Super Admins.
                - Revise an outdated document.
                - View a document's revision history.
            - Super Admins can:
                - Perform all privileges granted to Admins.
                - Delete a document.
                - Approve/reject a submitted document for approval.
                - Tag an approved document as outdated _(for revision)_.
    - **E-mailing**
        - An email will automatically be sent to the Admins if a document is submitted for:
            - For Review
            - For Revision Review
        - An email will automatically be sent to the Users if a document previously submitted is:
            - Approved
            - Denied
            - Tagged for Revision

## Features
- Bootstrap
- FontAwesome
- jQuery
- Popper
- jQuery DataTables
- jQuery Validate
- SweetAlert2
- Moment.js
- Summernote _(a WYSIWYG editor)_
- Backend CSRF Protection
- Password Encryption/Decryption
- MySQL
- E-mail Sending

## Getting Started
- Clone the repository.
- Execute `cd` on the directory containing the cloned repository.
- Execute the following commands to create a virtual environment:
    - For Windows:
        -  ```
           $ py -3 -m venv venv
           $ venv\Scripts\activate
           ```
    - For Linux/macOS:
        - ```
          $ python -3 -m venv venv
          $ . venv/bin/activate
          ```
- Install the following packages via `pip`:
    - python-dotenv
    - Flask
    - Flask-WTF
    - mysql-connector-python
    - cryptography
    - bleach
    - wtforms_json
    - email_validator
    - flask_mail
- Import the SQL file stored inside the /sql directory.
- Start the Flask app via `flask run` command.