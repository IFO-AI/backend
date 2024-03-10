# IFO backend

## Dependencies

- [flask](https://palletsprojects.com/p/flask/): Python server of choise

## Set Up

1. Check out the code
2. Install requirements
    ```
    pipenv install
    ```
3. Start the server with:
    ```
   python app.py
    ```

## Migrations

```
flask db init
flask db migrate -m "add comment here"

flask db upgrade

```