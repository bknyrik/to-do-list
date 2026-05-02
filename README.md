# To-do list
___
## Description
This project helps user to store information about their tasks and assigned tags to them.
By the way users with permissions like admins or staff can:
- Create, update and delete tags;
- Create, update and delete users;

And finally anonymous users can register to use this application.
___
## Installation
1. Clone the repository:
```
git clone https://github.com/bknyrik/to-do-list.git
```
2. Create a virtual environment `python -m venv .venv`;
3. Activate the virtual environment:
    - Windows - `to-do-list\Scripts\activate`;
    - macOS/Linux - `source to-do-list/bin/activate`.
4. Install all dependencies `pip install -r requirements.txt`;
5. Apply migrations `python manage.py migrate`;
6. Run the server `python manage.py runserver`.
___
## Usage
Visit `http://127.0.0.1:8000/` in your browser to use the application. 

And also don't forget to create a superuser:
```python manage.py createsuperuser```
