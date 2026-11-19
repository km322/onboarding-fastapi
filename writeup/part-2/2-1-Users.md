# 2.1. Add User objects

Let's add a simple "user account" system so we can implement task assignments later. This will be an extremely basic user implementation for the purpose of this guide.

## New schema: `User`

### Specification

The `User` schema should have the following fields:

- `name`: string, required (and not empty)
- `profilePictureURL`: string, optional

**Note:** In a real application, we would probably want some kind of image- or file-hosting service to store user profile pictures (such as Firebase Cloud Storage or AWS S3). For this guide, we'll just directly paste URLs when creating users.

### Walkthrough

1. Create a new folder `backend/src/user` for everything related to users, next to `backend/src/task`. Add an empty `__init__.py` file to it, just like `task/__init__.py`, so that Python treats the folder as a [package](https://docs.python.org/3/tutorial/modules.html#packages) and you can import from it.
2. Create a new file `backend/src/user/schemas.py`.
3. Use `task/schemas.py` as a guide to define three [Pydantic models](https://pydantic.dev/docs/validation/latest/concepts/models/) for the `User` schema:
   1. `UserBase`, with the `name` and `profilePictureURL` fields from the specification. Use `Field(min_length=1)` to make sure the name isn't empty, like `title` in `TaskBase`.
   2. `UserCreate`, which inherits from `UserBase` and describes the body of a request to create a User. It doesn't need any extra fields.
   3. `UserResponse`, which inherits from `UserBase` and describes a User returned by the API. It has an extra `id` field with the alias `"_id"`, like `TaskResponse`.
   <details>
   <summary><strong>🤔 For new developers: Domain folders</strong></summary>

   _Our backend is organized by "domain": each kind of object gets its own folder with the same set of files (`router.py`, `schemas.py`, `service.py`, `exceptions.py`). This keeps everything about users in one place, so you always know where to look. Domains can import from each other, but keep the imports going in one direction only. In this guide, the task domain will use the user domain, so nothing in `src/user` should ever import from `src/task`; otherwise, Python fails with a "circular import" error when the backend starts._
   </details>

4. Create a new file `frontend/src/api/users.ts`.
5. Use `api/tasks.ts` as a guide to define and export a `User` interface matching the `User` schema. (Remember to include the `_id` field.)
   1. Since User objects are simple enough to be directly encoded as JSON, we don't need to define a separate `UserJSON` interface and `parseUser` function.

## New API route: `POST /api/user`

### Specification

Creates a new User object in the database with the fields provided in the request body, then returns the new User. If the request body doesn't contain valid User data, returns a 422 error.

**Example request:**

`POST /api/user`

```json
{
  "name": "John Doe",
  "profilePictureURL": null
}
```

**Example response:**

201

```json
{
  "name": "John Doe",
  "profilePictureURL": null,
  "_id": "64ebc766fa1e11e2d987a8e9"
}
```

### Walkthrough

1. Create a new file `backend/src/user/service.py`.
2. Use `task/service.py` as a guide to write the PyMongo query that creates a User. Your users should go in a new collection named `"users"`, and you'll need a `_to_response` function that converts a user document from MongoDB into a `UserResponse`.
   ```python
   async def create(database: AsyncDatabase[dict[str, Any]], data: UserCreate) -> UserResponse:
       ...
   ```
3. Create a new file `backend/src/user/router.py`.
4. Use `task/router.py` as a guide to create a new `APIRouter` for user-related requests and add a route function `create_user`. Use `create_task` as a guide for the route function.

   ```python
   router = APIRouter(prefix="/api", tags=["users"])


   @router.post("/user", status_code=status.HTTP_201_CREATED)
   async def create_user(data: UserCreate, database: Database) -> UserResponse:
       ...
   ```

   Notice that there's no separate validation step to write. Because `data` has the type `UserCreate`, FastAPI checks the request body against your schema before calling `create_user`, and responds with a 422 error by itself if it's not valid.

5. Modify `backend/src/main.py` to import the router you just created and include it in the app with [`app.include_router`](https://fastapi.tiangolo.com/tutorial/bigger-applications/), just like `task_router`.
   <details>
   <summary><strong>❓ Hint: 404 "Not Found" errors</strong></summary>

   _If every request to `/api/user` gives a 404 error with the body `{"detail":"Not Found"}`, FastAPI doesn't know about your route yet. Check that you included your router in `main.py` and that the path in the decorator is `"/user"` (the `"/api"` prefix comes from the router)._
   </details>

6. Test your implementation by using Postman, the interactive API docs at http://localhost:3001/docs, or running the following command a few times with different values:

   ```shell
   curl -X "POST" http://127.0.0.1:3001/api/user \
     -H "Content-Type: application/json" \
     -d '{"name":"<Some name>","profilePictureURL":"<Some URL to an image>"}'
   ```

   Feel free to use the example profile pictures that we've provided in the `frontend/public` folder. The URLs for these would be, for example, `/profile1.png` (including the leading slash).

   Also try some invalid requests, such as one without a `name` or with `"name":""`. You should get a 422 error that explains what's wrong, for example:

   ```json
   {
     "detail": [
       {
         "type": "missing",
         "loc": ["body", "name"],
         "msg": "Field required",
         "input": { "profilePictureURL": "/profile1.png" }
       }
     ]
   }
   ```

   You should be able to see your new users in mongosh:

   ```
   use todoList
   db.users.find()
   ```

**Note:** We won't implement user creation in the frontend, so there's no need for an API client function in `frontend/src/api/users.ts` which corresponds to this route.

## New API route: `GET /api/user/{user_id}`

### Specification

Returns the User object with the provided ID. If no such User exists in the database, returns a 404 error.

**Example request:**

`GET /api/user/64ebc766fa1e11e2d987a8e9`

**Example response:**

200

```json
{
  "name": "John Doe",
  "profilePictureURL": null,
  "_id": "64ebc766fa1e11e2d987a8e9"
}
```

### Walkthrough

1. In `backend/src/user/service.py`, add a function `get_by_id` that returns the User with the given ID, or `None` if there isn't one. Use `get_by_id` from `task/service.py` as a guide. Don't forget the [`ObjectId.is_valid`](https://pymongo.readthedocs.io/en/stable/api/bson/objectid.html#bson.objectid.ObjectId.is_valid) check; without it, an ID like `abc` would crash the route function and give a 500 error instead of a 404.
2. Create a new file `backend/src/user/exceptions.py` and define a `UserNotFound` exception with the message `"User not found"`. Use `task/exceptions.py` as a guide.
3. In `backend/src/user/router.py`, add another route function `get_user`. Use `get_task` from `task/router.py` as a guide.
4. Test your implementation by using Postman, the interactive API docs, or running the following command with some different IDs:
   ```shell
   curl http://127.0.0.1:3001/api/user/<id>
   ```
   Try a couple User IDs that you got from mongosh, as well as some Task IDs, some nonexistent IDs, and something that isn't an ID at all (like `abc`). Everything except the User IDs should give a 404 error with `{"detail":"User not found"}`.
5. In `frontend/src/api/users.ts`, add an API client function that makes requests to this route. Use `getTask` from `api/tasks.ts` as a guide.

## Update to schema: `Task`

### Specification

The `Task` schema should have the following additional fields:

- `assignee`: ObjectId, optional, the ID of a User document
  - In request bodies, `assignee` is the User's ID as a string. A missing assignee, `null`, and the empty string `""` all mean that nobody is assigned to the task. If `assignee` is any other string that isn't a valid ObjectId, the backend returns a 422 error.
  - In the database, `assignee` is stored as an ObjectId (or `null`), the same type as the `_id` of a User.
  - In responses, `assignee` is the whole User object, or `null` if nobody is assigned or no User has that ID.
  - For simplicity, we don't need to check whether the ID belongs to an existing User object.

### Walkthrough

1. In `backend/src/task/schemas.py`, add an `assignee` field of type `str | None` with a default of `None` to `TaskCreate`. Since `TaskUpdate` inherits from `TaskCreate`, it gets the new field too.
2. In the same class, add a [field validator](https://pydantic.dev/docs/validation/latest/concepts/validators/#field-validators) for `assignee` that returns `None` if the assignee is empty, raises a `ValueError` if it isn't a valid ObjectId (use [`ObjectId.is_valid`](https://pymongo.readthedocs.io/en/stable/api/bson/objectid.html#bson.objectid.ObjectId.is_valid)), and otherwise returns it unchanged.

   ```python
   @field_validator("assignee")
   @classmethod
   def check_assignee(cls, assignee: str | None) -> str | None:
       ...
   ```

   Pydantic turns the `ValueError` into a validation error, adding `"Value error, "` to the start of your message, and FastAPI responds with a 422 error.
   <details open>
   <summary><strong>⚠️ Caution: Empty assignees</strong></summary>

   _The `TaskForm` we'll update in [Part 2.3](./2-3-Task-assignment.md) sends `"assignee": ""` when its assignee field is left blank. If your validator rejects the empty string instead of turning it into `None`, nobody will be able to save a task without an assignee. Also, don't skip the `ObjectId.is_valid` check: `ObjectId("abc")` raises an error, so without the check, an assignee like `abc` would give a 500 error instead of a 422._
   </details>

3. Add an `assignee` field of type `UserResponse | None` with a default of `None` to `TaskResponse`, importing `UserResponse` from `src.user.schemas`.
4. In `backend/src/task/service.py`, store the assignee as an ObjectId instead of a string whenever you turn a `TaskCreate` or `TaskUpdate` into a task document, both in `create` and in `update`. When there's no assignee, store `None` instead (careful: `ObjectId(None)` doesn't fail, it generates a brand new random ID). Consider writing a small helper function so you don't repeat this in both places.
   <details>
   <summary><strong>🤔 For new developers: Why store an ObjectId?</strong></summary>

   _Storing the plain string would seem to work for now, but the `_id` of each User is an ObjectId, and MongoDB doesn't consider a string equal to an ObjectId. Storing the same type keeps the data consistent, so queries that match tasks to users (like `db.tasks.find({ assignee: ObjectId("...") })` in mongosh) work as expected._
   </details>

5. Update all API routes that return a Task object to replace the assignee's ID with the corresponding User object, or `None` if no User has that ID. This is called _populating_ the field. PyMongo doesn't do it for us, so we'll write the extra query ourselves. Since every route that returns a Task goes through `_to_response` in `task/service.py`, that's the only place you need to do the lookup:
   1. Import the user service with `from src.user import service as user_service` and use `user_service.get_by_id` to find the assignee. It expects the ID as a string, so pass it `str(...)` of the stored ObjectId.
   2. Not every task document has an assignee: tasks you created before this change don't have the field at all, and unassigned tasks store `None`. Read it with `document.get("assignee")` instead of `document["assignee"]`, and only look up the User when it's set.
   3. Because the lookup is a database query, `_to_response` now needs the database as a parameter and has to be `async`. Update every call to `_to_response` in `create`, `get_all`, `get_by_id`, and `update` to pass in the database and `await` the result. (In `get_all`, you can use `await` inside the list comprehension.)

   <details open>
   <summary><strong>⚠️ Caution: Forgetting await</strong></summary>

   _Calling an `async` function without `await` doesn't run it; it just gives you a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutines) object, which can't be turned into a `TaskResponse` or `UserResponse`, so the request fails with a 500 error. Run `make lint-check` in `backend` after this step: mypy reports a missing `await` on `_to_response` with an error that mentions `Coroutine`, sometimes followed by the note `Maybe you forgot to use "await"?`. However, mypy can't catch a missing `await` on `user_service.get_by_id` inside `_to_response`, because the task document is a plain `dict` that accepts any value. Check that one yourself: if every task with an assignee gives a 500 error, that's the likely cause._
   </details>

   <details>
   <summary><strong>🤔 For new developers: Populating objects</strong></summary>

   _Populating sub-objects isn't always necessary; it depends on your specific needs for each API route. In our case, User objects are very small, so it's convenient to just always include the assigned User within a Task—then we won't need to send a separate request to retrieve the User itself._
   </details>

6. Test your changes with Postman, the interactive API docs, or curl. Create and update some tasks with a User ID as the `assignee` (for `PUT`, remember to include every field of the task). The response, and the response from `GET /api/tasks`, should include the whole User object. Tasks without an assignee should have `"assignee": null`. In mongosh, `db.tasks.find()` should show the assignee as `ObjectId('...')`.
7. In `frontend/src/api/tasks.ts`, add the following field to both the `Task` and `TaskJSON` interfaces:
   ```typescript
   assignee?: User;
   ```
   where `User` is imported from `api/users.ts`. (The backend actually sends `null` instead of leaving out the field when nobody is assigned, so make sure any code that uses `assignee` checks for both `null` and `undefined`. Optional chaining like `task.assignee?._id` handles both.)
8. In the same file, add the following field to `CreateTaskRequest` and `UpdateTaskRequest`:
   ```typescript
   assignee?: string;
   ```
   This is a string instead of a `User` because we only want to send the ID, not the entire User object.
9. Update the `parseTask` function to include the assignee.

<details open>
<summary><strong>⚠️ Caution: Checking off assigned tasks</strong></summary>

_After these changes, TypeScript will report an error in `TaskItem.tsx`, because the task we send to `updateTask` when checking it off has a `User` as its `assignee`, but `UpdateTaskRequest` expects a string. Fix it by passing `assignee: task.assignee?._id` to `updateTask`. Don't fix it by leaving the assignee out: `PUT` replaces the whole task, so a missing assignee would silently unassign the task every time it's checked off._

</details>

<details open>
<summary><strong>⚠️ Caution: Updating schemas</strong></summary>

_Whenever you add a field to an object, remember to update every schema that should include it: here, `TaskCreate` (and through it, `TaskUpdate`) for request bodies and `TaskResponse` for responses. Pydantic silently drops any request field that isn't in the schema, and FastAPI leaves out any response field that isn't in the response schema, so a forgotten schema doesn't cause an error. The field just never gets saved or never reaches the frontend. Don't forget to do this in your real projects!_

</details>

## Commit to Git

Remember to add, commit, and push your changes!

| Previous                                         | Up           | Next                                                        |
| ------------------------------------------------ | ------------ | ----------------------------------------------------------- |
| [2.0. Prepare for development](./2-0-Prepare.md) | [Part 2](./) | [2.2. Implement the task detail page](./2-2-Task-detail.md) |
