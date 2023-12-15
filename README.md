# CatChat
The Purpose of CatChat is to provide a simple chat application that symbolizes some basic chat functionality
while also providing secure communcation and authentication for each user.

## Description
CatChat was designed to be a groundwork for additional work in the future to provide a more robust chat application.
This application features encryption and decryption of messages using symmetric encryption via room join, 
symbolizing the use of session keys. The application also features authentication via a username and password 
using various concepts like a salt and a hash to keep the passwords secure in the database and a bloom filter
to showcase how a server can check if a username is banned or already in use. The application is modularized
and compartmentalized to allow for easy expansion and modification of the application. Additionally, the application
features the use of SQLite to store user information and chat history for each room in a lightweight manner, allowing
for a more feature rich database to be implemented in the future.

## Dependencies
* Python 3.6+
* Node.js 14.15.4+
* npm 6.14.10+
* pip 20.3.3+
* git 2.25.1+
* run `pip install -r requirements.txt` to install all dependencies for the application in the backend directory.

## Installation
* Navigate [here](https://github.com/Kbpatel3/CatChat) to clone the repository.
* Navigate the green "Code" button and copy the https link.
* Open a terminal and navigate to the directory you want to clone the repository to.
* Type `git clone <https_link>` to clone the repository to your local machine.
* Now the repository should be cloned to your local machine.
* Additionally, the repository can be cloned in an IDE like PyCharm or Visual Studio Code by navigating 
* to the VCS tab and selecting "Get from Version Control" and pasting the https link into the URL field.

## Execution
* create two terminals, one for the frontend and one for the backend.
* in the backend terminal, navigate to the backend folder and then the app folder using `cd <directory_name>`.
* If on windows, type the following into the backend terminal: `python app.py` to start the backend server.
* If on linux or mac, type the following into the backend terminal: `python3 app.py` to start the backend server.
* in the frontend terminal, navigate to the frontend folder and then the app folder using `cd <directory_name>`.
* Type the following into the frontend terminal: `npm start` to start the frontend server.
* The application should now be running on `localhost:5000`.
* A new tab will open up in your default browser for the landing page of the application.
* To stop the application, press `ctrl + c` in both terminals.

## Authors 
* [Kaushal Patel](https://github.com/Kbpatel3)
* [Michael Imerman](https://github.com/michael-imerman)

## Version History
* 1.0
    * Initial Release

## License
This project has a General Public License (GNU) v3.0 License - see the LICENSE.md file for details

## Acknowledgments
* [SQLite](https://docs.python.org/3/library/sqlite3.html)
* [SocketIO](https://flask-socketio.readthedocs.io/en/latest/)
* [React](https://react.dev/)
* [W3 Schools](https://www.w3schools.com/react/react_useeffect.asp)