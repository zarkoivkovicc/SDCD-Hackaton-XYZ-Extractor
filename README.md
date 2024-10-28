# SDCD-Hackaton-XYZ-Extractor

Tool to extract XYZ tables from the chem papers in PDF format. Currently it relies on text parsing and regexp. Idea is to extract any XYZ coordinates information form the paper. Does not provide any validation for the extracted coordinates.

### Project structure:
   * `/src` - original playground where all the main functionality was/is developed
   * `/app` - Node.js app (since it was a hackaton project, a flashy app was needed :D )
     * `/app/src/` - place where the app lives
       * `/app/src/backend` - python code which does the parsing and handles API calls
       * `/app/src/uploads` - Where uploaded PDFs are going 
       * `/app/src/processed` - storage for XYZ parsed files
       * `/app/src/App.js` - main app page
       * `/app/src/App.css` - main styles file

## Start the app
Web app utilizes Node.js server, React as front-end and Flask as back-end.

### Installation
After cloning the repo is to install the npm modules, so go to `/app` and execute `npm install`.

### Running the app
To run the application execute the following commands
```
# to start backend as a background process
python3 app/src/backend/app.py &

# to start the web-app
npm start --prefix app
```

To stop the app, simply Ctrl+C npm command and kill python process by doing following commands:
```
# to bring the background process back to CLI
fg

# to stop it
Ctrl+C
```
Backend is running on port 5000 and front (Node.js) on port 3000. For dependencies list, please refer to setup.cfg

#### Note on the app
`processed` and `uploads` directories should be cleaned regularly (manually) or some mechanism should be created to clean them up automatically. Otherwise they will accumulate a lot of files.