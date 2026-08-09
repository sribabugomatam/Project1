# Chapter 6: Testing and Debugging the Application

Testing is one of the most important parts of software development. It helps you confirm that your API works as expected.

## Why testing matters

Testing allows you to:

- Catch bugs early
- Verify CRUD behavior
- Protect your app from regressions
- Build confidence in your changes

## Test tools used in this project

The project uses pytest for backend testing.

## Example test file

The tests are in:

- backend/tests/test_api_crud.py

Example test:

```python
def test_full_crud_and_relationships(client):
    response = client.post(
        "/api/flats",
        json={"flat_number": "999", "floor_number": 9, "status": "Owner Occupied"},
    )
    assert response.status_code == 201
```

This test checks that creating a flat through the API works.

## How to run tests

From the backend folder:

```bash
cd backend
. venv/bin/activate
python -m pytest -q
```

## Debugging tips

When something breaks:

1. Read the error carefully.
2. Check the request payload.
3. Confirm the route and method.
4. Verify the database state.
5. Review the relevant model or schema.

## Common issues

### 422 validation error

This usually means the request body does not match the expected schema.

Example:

```json
{
  "flat_number": "101",
  "floor_number": 1,
  "status": "Owner Occupied"
}
```

If your payload shape is wrong, FastAPI will return a validation error.

### 404 not found

This usually means the endpoint path is incorrect or the resource ID does not exist.

## Summary

Testing and debugging are essential skills. You should learn to:

- Write small tests for important routes
- Reproduce issues
- Fix one problem at a time

## Next chapter

Next, we will learn Git and GitHub basics for managing the project.
