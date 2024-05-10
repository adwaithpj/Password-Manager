# Password Manager 💻🔐

## Overview
This Python-Flutter based password manager, developed with Flet python, provides a secure and user-friendly way to generate, save, and manage passwords. It includes features for password generation, local storage, and search functionality.

## Features 🚀
- **Password Generation:** Easily generate strong and secure passwords with customizable lengths.
- **Save Passwords:** Store website details, including the website name, email/username, and password.
- **Search Functionality:** Quickly find saved passwords by entering the website name.
- **Local Storage:** Passwords are locally stored in a JSON file for easy retrieval.

## Prerequisites 🛠️
- Python 3.x
- Flet Framework


## Download the Executable App 📥
- **Windows Users:** [Download Password Manager for Windows](https://github.com/adwaithpj/Password-Manager/releases/tag/Windows)
- **Linux Users:** 
-   For Linux Users:        

    **Build the application in Linux platform and contirbute :}**
      

## GitHub Setup 🌐
For development purposes, follow these GitHub-related steps:

1. **Fork the Repository:**
   - Click on the "Fork" button at the top right of the GitHub repository page.
  
2. **Clone Your Fork:**
   - Clone your forked repository to your local machine:
     ```bash
     git clone https://github.com/adwaithpj/Password-Manager.git
     ```

3. **Create a Virtual Environment:**
   - Create a virtual environment to isolate project dependencies:
     ```bash
     python -m venv venv
     ```

4. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
     On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies:**
   - Install the required dependencies from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

6. **Build the Application:**
     ```flet
     flet build linux
     ```

## Additional Notes ℹ️
- The code includes commented-out sections related to Google Sheets integration. Uncomment these sections and provide the necessary credentials to enable this feature.
- There is jsondic.py file which has all the functionalities of Reading,Writing and Updating the JSON file.


## Acknowledgments 🙌
This password manager was developed as a simple project and can be extended for additional features and security enhancements.

Feel free to contribute or provide feedback! 🌟



