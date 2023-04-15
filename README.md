# thread-lurker
Did you know that, exactly nine years ago today, on March 8, 2014, Malaysia Airlines Flight 370 disappeared without a trace while flying from Kuala Lumpur

# Running the Code Locally
To run the "thread-lurker" code on a local machine, follow these steps:

### Prerequisites:

1. Python 3 installed on the local machine
2. MongoDB database installed and running on the local machine
3. Required Python packages installed (requirements.txt)

### Instructions:

1. Clone the "thread-lurker" repository from GitHub using the following command:
```bash
git clone https://github.com/fadhlanmr/thread-lurker.git
```
2. Change to the "thread-lurker" directory:
```bash
cd thread-lurker
```
3. Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```
4. Update the MongoDB connection details in the .env file to match your local MongoDB configuration.
5. Run the "function.py" script using Python:
```bash
python function.py
```


# Vulnerabilities
The "thread-lurker" code may have the following vulnerabilities:

1. Injection Vulnerability: The code directly constructs URLs for making HTTP requests without proper validation and sanitization of user-supplied input. This can potentially allow for URL injection attacks or other malicious activities.

2. Data Validation Vulnerability: The code does not perform thorough validation and sanitization of the data fetched from the 4chan catalog API before storing it in the MongoDB database. This can lead to storing of invalid or malicious data in the database.

3. Exception Handling Vulnerability: Although the code includes basic exception handling using try-except blocks, the error messages are printed to the console without proper handling or logging. This can expose sensitive information or make debugging difficult in a production environment.

4. Authentication and Authorization Vulnerability: The code does not include any authentication or authorization mechanisms for accessing the MongoDB database, which can potentially allow unauthorized access to the database.

It is recommended to thoroughly review and update the code to address these vulnerabilities before deploying it in a production environment. This may include implementing proper input validation, error handling, authentication, and authorization mechanisms to ensure the security and integrity of the application and its data.
