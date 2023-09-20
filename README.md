
# Audio-feature-visualization

The web application allows users to visualize and compare various music recording parameters from multiple recordings simultaneously. There are currently no similar web-based applications available. Users can customize each visualization according to their preferences, and all changes are automatically saved to the database.


## Tech Stack

**Client:** 
<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg" height="40" alt="vuejs logo"  />
   <img width="12" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/1/1c/Pinialogo.svg" height="40" alt="vscode logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" height="40" alt="javascript logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height="40" alt="html5 logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" height="40" alt="css3 logo"  />
  <img width="12" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Tailwind_CSS_Logo.svg" height="40" alt="tailwindcss logo"  />
   <img width="12" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/f/f1/Vitejs-logo.svg" height="40" alt="vscode logo"  />
</div>

###

**Server:** 

###

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" height="40" alt="flask logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" height="40" alt="postgresql logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlalchemy/sqlalchemy-original.svg" height="40" alt="sqlalchemy logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" height="40" alt="numpy logo"  />

</div>

###



## Demo

https://audio-feature-visualization.onrender.com/

## Documentation

[Documentation](https://drive.google.com/file/d/10ewwWTRCiWncaQMfoQy4w9VBdOK00oJ3/view)

## YouTube
https://youtu.be/oowly3jtM-Y

## Screenshots

Registration is available for users on the platform, and their information is securely stored in the database. After a successful login, a JSON Web Token (JWT) is generated on the server and sent to the user for subsequent request validation. The form enables validation of input data.

![App Screenshot](https://github.com/MartinKlimes/Audio-feature-visualization-webapp/assets/107542941/de3a3aaf-569d-4bcd-9f14-ac9eb9a457cd)

The user can upload recordings, music notation files, and MIDI files to the application, and all data is saved on the server. Recordings can be added via drag-and-drop, renamed, or deleted. The user also has the option in the settings panel to switch the application from Czech to English language.

![App Screenshot](https://github.com/MartinKlimes/MartinKlimes/assets/107542941/feadfff7-7341-4ae4-84d6-080263cec98b)

This is the main page of the application. It consists of multiple components that effortlessly exchange data using the Pinia store and enable communication with the server through RestAPI.

![App Screenshot](https://github.com/MartinKlimes/MartinKlimes/assets/107542941/e64c9a71-1fb7-4d6b-a74d-a65cce532363)

Users have the flexibility to visualize multiple parameters from an unlimited number of recordings. Moreover, they can export all visualizations as needed. Each visualization comes with a dedicated settings panel on the right, allowing users to customize their display preferences.

![App Screenshot](https://github.com/MartinKlimes/MartinKlimes/assets/107542941/4c351ef8-e90d-42d7-ace7-37be312f9334)



## Run Locally

Clone the project

```bash
  git clone https://github.com/MartinKlimes/Audio-feature-visualization-webapp.git
```

Go to the project directory

```bash
  cd frontend
```

Install dependencies

```bash
  npm install
```

Build the application

```bash
  npm run build
```
#### Setting up the Flask Server and Database

To run the Flask development server locally, you need to perform the following steps:

1. Open the file backend/run.py.

2. Ensure that the correct Database URI is set in  backend/mos_backend/init.py.

3. To set up the required database tables, execute the script create_tables.py (this only needs to be done once).

4. After configuring the database, you can use the application to register and log in.
