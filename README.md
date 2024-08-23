# Recommender System for Cryptocurrencies

## Usage

### 1. Clone the Project
Clone the repository using the following command:
```sh
git clone https://github.com/moshtava/rekommender-sistem.git


2. Create Virtual Environment
Create a virtual environment using the following command:

python.exe -m venv venv

3. Activate the Virtual Environment
Activate the virtual environment using the appropriate command for your operating system:

•  On Windows:

.\venv\Scripts\activate

•  On macOS/Linux:

source venv/bin/activate

4. Install Required Packages
Install the necessary packages using the following command:

pip install -r requirements.txt

5. Run Database Migrations
Run the following commands to apply database migrations:

python manage.py makemigrations
python manage.py migrate

6. Insert Initial Data and Train the Model
Insert initial data and train the model using the following command:

python manage.py insert_data

7. Run the Development Server
Start the development server using the following command:

python manage.py runserver

8. Access the API
Open your browser and go to:

http://127.0.0.1:8000/api/recommend/<user_id>/

http://127.0.0.1:8000/api/transactions/
