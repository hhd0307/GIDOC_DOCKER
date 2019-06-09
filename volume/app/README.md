# GIDOC
### Requirements

* Node js
* Mongodb
* Postman (for testing API)
* Android Studio (for App)
* Python3

### Installation

1. Install node js and npm
https://nodejs.org/en/

2. Install mongodb
https://www.mongodb.com/	

3. Install Robo3T (GUI for handle mongodb server) (optional)
https://robomongo.org/

4. Install Postman (for testing the API) (optional)
https://www.getpostman.com/

5. Create database for mongodb
    * Open terminal
    ```
    chmod +x initialize_mongo.sh
    ./initialize_mongo.sh duc
    ```

6. Install package for python3
    ```
    pip3 install -r ./python/requirements.txt
    ```

7. Install dependency
    ```
    npm install
    ```

8. Grant permission
    ```
    chmod 0777 -R ./python/
    ```

### Running
```
sudo service mongod start
npm start
```




