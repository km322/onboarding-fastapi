# 1.2. Implement task checkoff

Next, we'll add the ability to mark and unmark tasks as done.

## New API route: `PUT /api/task/{task_id}`

### Specification

Updates an existing Task by replacing all of its fields with the data from the request body, then returns the updated Task. If the request body is not a valid Task, returns a 422 error. If the ID in the request body doesn't match the ID in the URL, returns a 400 error. If no Task exists with the ID in the URL, returns a 404 error. FastAPI checks the request body before it calls our route function, so the 422 error always comes first, but the other two errors can be checked in either order.

**Example Task in database:**

```json
{
  "title": "Part 1.2 backend",
  "description": "Implement the PUT /api/task/{task_id} route",
  "isChecked": false,
  "_id": "64ebc766fa1e11e2d987a8e9",
  "dateCreated": "2023-09-02T01:49:32.621000Z"
}
```

**Example request:**

`PUT /api/task/64ebc766fa1e11e2d987a8e9`

```json
{
  "_id": "64ebc766fa1e11e2d987a8e9",
  "title": "Part 1.2 backend update",
  "description": "Implement the PUT /api/task/{task_id} route update",
  "isChecked": true,
  "dateCreated": "2023-09-02T01:49:32.621Z"
}
```

**Example response:**

200

```json
{
  "title": "Part 1.2 backend update",
  "description": "Implement the PUT /api/task/{task_id} route update",
  "isChecked": true,
  "_id": "64ebc766fa1e11e2d987a8e9",
  "dateCreated": "2023-09-02T01:49:32.621000Z"
}
```

**Example error response** (if the request body had a different `_id`):

400

```json
{
  "detail": "Task ID in the request body does not match the URL"
}
```

<details>
<summary><strong>🤔 For new developers: POST and PUT</strong></summary>

_Note that we use `POST` requests to create Tasks and `PUT` requests to update them. This isn't strictly necessary (we could, say, use `POST` for everything), but it's a standard industry practice because it follows the original HTTP specification more closely. The main difference between the two methods is "[idempotence](https://developer.mozilla.org/en-US/docs/Glossary/Idempotent)"—`PUT` actions are expected to be idempotent, while `POST` actions are not._

</details>

<details>
<summary><strong>✅ Good practice: Limit user-modifiable fields</strong></summary>

_Here we just replace the entire Task object with the provided data, even the `dateCreated` field. We do this for simplicity, but in a real project, it might be advisable to limit which fields can be modified by a user request._

</details>

### Walkthrough

1. Add an error for the 400 response to `backend/src/task/exceptions.py`, so that the file looks like this:

   ```python
   from src.exceptions import BadRequest, NotFound


   class TaskNotFound(NotFound):
       DETAIL = "Task not found"


   class TaskIdMismatch(BadRequest):
       DETAIL = "Task ID in the request body does not match the URL"
   ```

   Like `TaskNotFound`, `TaskIdMismatch` builds on one of the shared errors in `src/exceptions.py`. When a route function raises it, FastAPI stops the request and responds with a 400 status and a body like `{"detail": "Task ID in the request body does not match the URL"}`. ([FastAPI error handling docs](https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception))

2. Copy the skeleton code below into `backend/src/task/service.py`, under the `get_by_id` function. Also add `TaskUpdate` to the import from `src.task.schemas` at the top of the file.

   ```python
   async def update(
       database: AsyncDatabase[dict[str, Any]], task_id: str, data: TaskUpdate
   ) -> TaskResponse | None:
       """Replace the task with task_id and return it, or None if it does not exist."""
       # your code here
   ```

3. Use the [`find_one_and_replace()`](https://pymongo.readthedocs.io/en/stable/api/pymongo/asynchronous/collection.html#pymongo.asynchronous.collection.AsyncCollection.find_one_and_replace) PyMongo function to replace the Task in the database with the given ID. (Actually, there are several functions you can use; any approach that works is valid.) Refer to `get_by_id` in the same file for an example of a similar query, `find_one()`.
   1. Like `get_by_id`, start by checking `ObjectId.is_valid(task_id)`, and return `None` if the ID isn't valid. Otherwise, `ObjectId(task_id)` raises an error for IDs like `abc`, and the request fails with a 500 error instead of a 404.
   2. The first argument to `find_one_and_replace()` is a filter that selects which document to replace. Use the same filter as `get_by_id`. The second argument is the replacement document, which you can get by calling `data.model_dump()`. This converts the `TaskUpdate` into a Python `dict` containing its `title`, `description`, `isChecked`, and `dateCreated`.
   3. Also pass the keyword argument `return_document=ReturnDocument.AFTER` (import [`ReturnDocument`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.ReturnDocument) from `pymongo`). By default, `find_one_and_replace()` returns the document as it was _before_ the replacement, just like Mongoose's `findByIdAndUpdate()` if you've used that before. We want to send the updated Task back to the frontend, so we ask for the document _after_ the replacement instead. That way, we don't need a second query to look up the new version.
   4. Remember to `await` the result.
   5. If the result is `None`, then there was no document in the database with that ID, so return `None`. Otherwise, return the document converted into a `TaskResponse` with the `_to_response` helper, like `get_by_id` does.

   <details>
   <summary><strong>🤔 For new developers: Where did _id go?</strong></summary>

   _Look at the `TaskUpdate` schema in `backend/src/task/schemas.py`. Pydantic doesn't allow field names that start with an underscore, so the field is called `id` in Python and `_id` in JSON (its [alias](https://pydantic.dev/docs/validation/latest/concepts/fields/#field-aliases)). It also has [`exclude=True`](https://pydantic.dev/docs/validation/latest/concepts/fields/#exclude), which leaves it out of `model_dump()`. That's what we want: MongoDB keeps a document's original `_id` when it replaces the document, so the replacement only needs the other fields. Don't add `_id` back into the replacement document. Our `_id` is a string, but the one stored in MongoDB is an `ObjectId`, and MongoDB refuses to change a document's `_id`._

   </details>

4. Copy the skeleton code below into `backend/src/task/router.py`, under the `create_task` function. Also add `TaskIdMismatch` to the import from `src.task.exceptions` and `TaskUpdate` to the import from `src.task.schemas`.

   ```python
   @router.put("/task/{task_id}")
   async def update_task(task_id: str, data: TaskUpdate, database: Database) -> TaskResponse:
       """Replace the task with the ID in the URL with the request body and return it.

       Returns a 400 error if the _id in the body is not the ID in the URL, or a 404 error if
       there is no task with that ID.
       """
       # your code here
   ```

   The `@router.put("/task/{task_id}")` decorator tells FastAPI to call this function for `PUT` requests to `/api/task/{task_id}`. Since `src/main.py` already includes this router in the app, you don't need to register the route anywhere else. Like in `get_task` and `create_task`, FastAPI fills in the parameters for us: `task_id` comes from the URL, and `data` is the JSON request body. FastAPI validates the body against the existing `TaskUpdate` schema in `backend/src/task/schemas.py` (which requires `_id`, `title`, and `dateCreated`) and responds with a 422 error by itself if it's not valid, so we don't need to write any validation code. ([FastAPI request body docs](https://fastapi.tiangolo.com/tutorial/body/))

5. Compare the `task_id` from the URL with the `_id` in the request body. In Python, that field is called `data.id`, not `data._id`, because `_id` is only its name in JSON. If they're not equal, `raise TaskIdMismatch()`. Just like `raise TaskNotFound()` in `get_task`, this stops the function and sends the error response.
6. Call the `service.update` function you wrote earlier (remember to `await` it). If it returns `None`, then there was no Task with that ID, so `raise TaskNotFound()`. Otherwise, return the updated Task, and FastAPI will send it as JSON with a 200 status. See `get_task` for an example.
7. Test your implementation. Make sure your backend is running locally (`make start` automatically reloads it when you save a file, so check its terminal for errors), then call the new route through Postman or run the following command with your own values filled in:

   ```shell
   curl -X "PUT" http://127.0.0.1:3001/api/task/<paste a Task ID from your database here> \
     -H "Content-Type: application/json" \
     -d '{"_id":"<the same ID>","title":"<Your title>","description":"<Your description>","isChecked":false,"dateCreated":"2023-10-01T00:00Z"}'
   ```

   This example sets `dateCreated` to an old date, which moves the Task to the bottom of the newest-first list. To keep it in place, paste the Task's existing `dateCreated` instead.

   If you're on Windows PowerShell and you get an error, try using `curl.exe` instead of just `curl`. This is necessary because on Windows, `curl` aliases to a different tool with different syntax than the `curl` command, unless you specify `curl.exe`.

   You can also try the route in FastAPI's interactive API docs: open http://localhost:3001/docs, expand `PUT /api/task/{task_id}`, click "Try it out", fill in the ID and request body, and click "Execute".

   You should see the Task updated with its new data when you list all Tasks in mongosh and when you view the frontend Home page. Also test the error cases: a different `_id` in the request body should give a 400 error, an ID that isn't in your database (in both the URL and the body) should give a 404 error, and an empty title should give a 422 error.

8. Copy the skeleton code below into `frontend/src/api/tasks.ts`:
   ```typescript
   export async function updateTask(task: UpdateTaskRequest): Promise<APIResult<Task>> {
     try {
       // your code here
     } catch (error) {
       return handleAPIError(error);
     }
   }
   ```
9. Using the existing functions as guides, complete the implementation of `updateTask`.

## Update to component: `TaskItem`

### Specification

- When the user presses the `CheckButton`, call the `updateTask` function to flip the value of `isChecked` for this `TaskItem`'s `Task` object.
- Re-render the `TaskItem` when `updateTask` resolves to the updated `Task`.
  - If an error occurs, then display a Constellation `Dialog` component to the user with the error message.
- Prevent the user from pressing the `CheckButton` again until `updateTask` has resolved (this will require at least one additional state variable).

### Walkthrough

1. In `frontend/src/components/TaskItem.tsx`, add new state variables `task` and `isLoading` and a helper function `handleToggleCheck`:

   ```tsx
   import React, { useState } from "react"; // update this line
   // ...
   export function TaskItem({ task: initialTask }: TaskItemProps) {
     // update the previous line and add the following
     const [task, setTask] = useState<Task>(initialTask);
     const [isLoading, setLoading] = useState<boolean>(false);

     const handleToggleCheck = () => {
       // your code here
     };

     // ...
   }
   ```

2. Within `handleToggleCheck`, set `isLoading` to true (by calling `setLoading`—never assign directly to a state variable, because React will ignore it), then call the `updateTask` function (be sure to import it from `src/api/tasks`). Pass in the `task` state variable, with the value of `isChecked` flipped.
   <details>
   <summary><strong>🤔 For new developers: Spread syntax</strong></summary>

   _An easy way to do this is to use JavaScript's [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax#spread_in_object_literals). You can write something like `{ ...task, isChecked: !task.isChecked }`. This is preferable because it's concise and it creates a (shallow) copy of `task`; we shouldn't modify `task` or any other props directly because that might cause unintended side effects._
   </details>

3. When `updateTask` resolves, call `setTask` with the new task from the response (or use the Constellation `Dialog` component to the user if it failed) and set `isLoading` back to false. See the `handleSubmit` function in `components/TaskForm.tsx` for an example of how to handle the result of a request (the request is `createTask` in that case) and display the `Dialog` with a state variable for an error message.
   <details>
   <summary><strong>🤔 For new developers: await or async</strong></summary>

   _If you make `handleToggleCheck` an `async` function, you can use `await` syntax instead of `then()`. There's no real difference here, so it's up to preference. Just stay consistent and don't mix the two syntaxes together._
   </details>
   <details>
   <summary><strong>❓ Hint: Where to call setLoading</strong></summary>

   _Make sure you call `setLoading(false)` **inside** the `.then()` block. If it's outside, then it will run immediately instead of after the response-handling code finishes._
   </details>

4. Pass two props to the `CheckButton`: `onPress` and `disabled`. We want `handleToggleCheck` to be called when the `CheckButton` is pressed, and we want the `CheckButton` to be disabled when `isLoading` is true.
   <details>
   <summary><strong>✅ Good practice: Organize helper functions together</strong></summary>

   _We could write the `onPress` handler function directly inside the JSX instead of storing it in a named variable. However, we'd recommend only doing that for super simple, one-line functions. Otherwise, it's generally a good practice to organize nontrivial helper functions like `handleToggleCheck` separately from our rendering code, to make them easier to find._
   </details>

5. Test your changes by checking and unchecking some tasks on the Home page. Make sure that each `TaskItem` updates its text color correctly and that after clicking the `CheckButton`, you can't click it again until the `TaskItem` has updated. To be extra sure, you can verify that the value of `isChecked` changes in mongosh. Also make sure it works as expected when you shut down your local backend (to simulate network unavailability).

## Commit to Git

Follow the same process as in [Part 1.1](./1-1-Task-list.md): stage your changes using `git add`, commit them using `git commit` with a descriptive message, and push them using `git push`.

| Previous                                           | Up           | Next                                              |
| -------------------------------------------------- | ------------ | ------------------------------------------------- |
| [1.1. Implement the task list](./1-1-Task-list.md) | [Part 1](./) | [1.3. Make a pull request](./1-3-Pull-request.md) |
