# Introduction

**Note:** We recommend viewing these writeup files on GitHub. You can quickly navigate the headings in each part by clicking on this icon at the top of the file: <img src="./images/contents-icon.png" width="20" height="20" />

## Project overview

We want to build a simple todo list app to keep track of tasks. At a high level, the app should be able to do the following things:

- Create a new task
- Check off a completed task
- Display a list of all tasks
- Edit the text of a task
- Assign someone to a task

We've decided that the first three points constitute a minimum viable product, or MVP, and the last two can be done in a "version 2" (v2) of the project.

<details>
<summary><strong>ℹ️ Definition: Minimum viable product (MVP)</strong></summary>

_A minimum viable product is a project version that only contains the features necessary to achieve the product's core purpose, without any extra "nice-to-haves." You'll often hear this term in the context of startups, where it's important to get something finished quickly so you can show it to investors._

</details>

In TSE, your team's product manager and designers will plan out most of the project's features before development starts. Typically, they'll create a project proposal and other documents that you can refer to for information about how certain features should work, and a Figma file with the frontend design prototypes. We explain each feature of this todo list app in this guide, so there's no separate proposal or writeup, but you should familiarize yourself with our [todo app Figma designs](https://www.figma.com/file/8eRDNyOrYRgyN7NNb0mIXA/Onboarding-Todo-App) in [Part 0](./part-0/).

## Submission

Completion of this onboarding repository is **required** for all new TSE members, and highly recommended for returning members who haven't completed it yet. After completing the tasks, you will submit a video demo of your work to your engineering manager (EM); see [the conclusion](./Conclusion.md#submission-instructions) for details on what to submit!

## Tools and technologies

The engineering manager on each TSE project chooses its tech stack (programming languages and frameworks) before development starts. For this todo list app, we'll use **MongoDB** as our database, **FastAPI** for our backend, **React** for our frontend, and **Node** to run the frontend tooling. We'll write the frontend in **TypeScript** and the backend in **Python**, test them with **Vitest** and **pytest**, and use **Git** to manage version history. Expand the sections below to learn more about each piece of this tech stack.

<details>
<summary><strong>🤔 For new developers: What about the MERN stack?</strong></summary>

_You may hear people at TSE talk about the **MERN stack** (MongoDB, Express, React, Node), which has historically been our most common stack. Express is a backend framework for Node, so a MERN app is written in JavaScript/TypeScript from top to bottom. This guide replaces Express with FastAPI, a Python backend framework, so our backend is written in Python and Node is only used for the frontend. The ideas you'll learn here (routes, requests and responses, validation, database queries) carry over directly to Express and most other backend frameworks._

</details>

<details>
<summary><strong>ℹ️ Definition: Frontend vs. backend</strong></summary>

_Generally, the **frontend** of a web app or mobile app is the code that runs on the user's device (browser or phone), while the **backend** is the code that runs on the servers. In order to make things efficient, the frontend usually only handles displaying the user interface and filling it with data from the backend, while the backend handles heavy lifting such as storing, manipulating, and sending data, calling third-party services, etc. The frontend initiates an operation by sending a **request** to the backend, which returns a **response** indicating success or failure. This communication model is fundamental to modern software._

</details>

### TypeScript

<details>
<summary><strong>About TypeScript</strong></summary>

Most of the frontend starter code files are [TypeScript](https://www.typescriptlang.org) files (ending in `.ts` or `.tsx`). TypeScript is closely related to [JavaScript](https://en.wikipedia.org/wiki/JavaScript) (`.js` or `.jsx`), the industry-standard **language for web development** along with HTML and CSS. Web browsers must be able to understand HTML, CSS, and JS in order to properly show most modern websites to users. As for TypeScript, it's an extended version ("superset") of JavaScript that adds static typing to the language.

**Static typing** means that the data type of each variable is determined **at compile time**, before the program runs, and the compiler can alert you to any type mismatches. Other statically-typed languages include Java and C++.

On the other hand, standard JavaScript is a **dynamically-typed** language, meaning that data types are determined **at runtime** and can change throughout the program's execution. Other dynamically-typed languages include Python and PHP.

While being dynamically-typed provides a lot of flexibility, it also makes code harder to understand, harder to write, and more prone to type errors at runtime, especially in large projects. For some examples to illustrate why, refer to this [article about TypeScript vs. JavaScript](https://www.toptal.com/typescript/typescript-vs-javascript-guide). It's now common in the industry to use TypeScript over JavaScript to write application code, and we strongly recommend it in TSE for the same reasons.

Note that although TypeScript and JavaScript are technically different languages, they are so closely related that they're practically interchangeable. In general, when we say something involving JavaScript, we mean "JavaScript and/or TypeScript."

<details>
<summary><strong>🤔 For new developers: How exactly is TypeScript related to JavaScript?</strong></summary>

<em>

For context, JavaScript comes from a standard called [ECMAScript](https://en.wikipedia.org/wiki/ECMAScript), which is designed to ensure that websites work the same across different web browsers. Microsoft created TypeScript when software engineers realized that static typing is actually very helpful for developing large applications. However, browsers still run JS, not TS, so we use a special compiler called [Babel](<https://en.wikipedia.org/wiki/Babel_(transcompiler)>) to automatically convert our original code into something they can understand.

</em>
</details>
</details>

### Python

<details>
<summary><strong>About Python</strong></summary>

The backend starter code is written in [Python](https://www.python.org) (in files ending in `.py`). Python is one of the most popular programming languages in the world, known for its readable syntax, and it's widely used for backend servers, scripting, data science, and machine learning.

As mentioned above, Python is a **dynamically-typed** language, just like JavaScript. Python doesn't check data types until the program runs, so it has the same drawbacks for large projects. To get the benefits of static typing anyway, we write **type hints** on our variables, function parameters, and return values. For example, here's the first line of a function in the starter code, which takes a `task_id` that's a string and a `database`, and returns a `TaskResponse`:

```python
async def get_task(task_id: str, database: Database) -> TaskResponse:
```

Python itself ignores type hints when it runs your code. Instead, we use a tool called [mypy](https://mypy.readthedocs.io/en/stable/) to check them **before** the program runs, similar to how the TypeScript compiler checks TypeScript code. We configure mypy in its strictest mode, so it requires type hints on every function and alerts you to any type mismatches. You can think of "Python with type hints and mypy" as Python's version of TypeScript.

Type hints aren't only for mypy, though. Some libraries read them while the program runs, too. As you'll see below, FastAPI and Pydantic use them to check that the data our backend receives has the correct shape.

We also use [Ruff](https://docs.astral.sh/ruff/) to lint and format our Python code, which does the same job for the backend that ESLint and Prettier do for the frontend.

<details>
<summary><strong>🤔 For new developers: If you're new to Python or type hints…</strong></summary>

_…we recommend skimming the official [Python tutorial](https://docs.python.org/3/tutorial/) if you haven't used Python before, and FastAPI's short [introduction to Python types](https://fastapi.tiangolo.com/python-types/), which explains type hints with examples. You don't need to master either one before starting this guide._

</details>
</details>

### MongoDB

<details>
<summary><strong>About MongoDB</strong></summary>

[MongoDB](https://www.mongodb.com) is a popular **cloud database service.** Its databases are **non-relational,** which basically means "not SQL." That is, unlike the rigid table, column, and row format of relational SQL databases, MongoDB stores **collections** of **documents** where the format of each document is highly flexible and can store arbitrary data. If you're familiar with [JSON](https://www.json.org/json-en.html), it's useful to think of MongoDB documents as JSON objects—in fact, they're stored as [binary encoded JSON](https://www.mongodb.com/basics/bson).

To interface with MongoDB from our backend, we use [PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/), MongoDB's official Python library, which lets us insert, find, update, and delete documents. However, MongoDB doesn't enforce data types like SQL databases do, and neither does PyMongo. So, we use another Python library called [Pydantic](https://docs.pydantic.dev/latest/) to describe the shape of our data (which fields each object has, and their types) and check that the data going in and out of our backend matches that shape.

<details>
<summary><strong>ℹ️ Definition: Database</strong></summary>

_A **database** is a specialized place for storing large amounts of data in the backend of an application. Examples of types of data we could store include usernames, passwords, profile pictures, post/comment text, order numbers, chat messages, payment information, and much more. We typically want to store these in the backend so that a user can log in on a different device and still have access to the same information._

</details>

</details>

### Node

<details>
<summary><strong>About Node</strong></summary>

[Node.js](https://nodejs.org), or just Node, is a **JavaScript runtime environment.** It allows us to run JavaScript code outside of a browser, such as on a backend server or in command-line scripts. Many projects, including most past TSE projects, use Node to run their backend. In this guide, our backend runs on Python instead, so we only use Node for the frontend's development tools (like Vite, ESLint, and Vitest) and for the Git hooks that check your code before each commit.

[npm](https://www.npmjs.com), or Node Package Manager, is a **package manager for JavaScript projects** that comes with Node by default. It provides a command-line interface, which we'll use later by running commands that start with `npm`, and a huge online database of open-source packages. These are vital for TSE and software projects of any size because they can save us from having to "reinvent the wheel" over and over.

</details>

### FastAPI

<details>
<summary><strong>About FastAPI</strong></summary>

[FastAPI](https://fastapi.tiangolo.com) is a **framework for writing backend APIs with Python.** Through FastAPI, we'll tell our server how to handle each type of request from the frontend. FastAPI is built around type hints: it uses them, together with Pydantic, to automatically check every request body and reject invalid ones before our code even runs. It also generates interactive documentation for our API, which you can use to try out requests right in your browser.

In order to set up our backend, we manually created and organized all of the files in the `backend` folder. Backend code usually doesn't require as much complicated setup as frontend in TSE projects, so we don't need any special setup tools.

To manage our backend's dependencies, we use [uv](https://docs.astral.sh/uv/), a **package manager for Python projects.** It does for the backend what npm does for the frontend: it installs the packages that the backend depends on (and even the right version of Python itself), and it provides a command-line interface, which we'll use later by running commands that start with `uv`.

<details>
<summary><strong>ℹ️ Definition: Application programming interface (API)</strong></summary>

_An application programming interface is the set of operations and ways to use them that the developer of an application or system exposes to its users. APIs are everywhere in software engineering—examples include the built-in functions in JavaScript and other languages, the third-party functions and React components in various NPM packages, and the external APIs of services like GitHub and AWS. In TSE, when we talk about a project's API, we're often referring to its backend API: the layer of code on the backend which receives requests from the frontend, handles them, and returns responses._

</details>
</details>

### React

<details>
<summary><strong>About React</strong></summary>

[React](https://react.dev) is a **component-based framework for building frontend user interfaces.** It's quite powerful, but often requires some adjustment for new developers because its paradigms may be very different from anything you've seen before. We'll explain how it works in some detail throughout this guide.

Websites are rendered (displayed) in a browser through a combination of HTML, CSS, and JavaScript. Each of the three plays a separate role: **HTML** specifies the **structure** of the UI (what elements are present and how they relate to each other), **CSS** adds **styles** (colors, fonts, sizes, borders, etc.) to those elements, and **JavaScript** adds **functionality** (what happens when the user clicks this button or that menu).

However, it's tedious to write lots of individual HTML, CSS, and JS files. React makes development easier by **combining structure and functionality** under one unified JavaScript framework. See [Part 0](./part-0/) for some illustration with the files in the starter code.

We used [Vite](https://vitejs.dev) to initialize our React project in the `frontend` folder. It can be quite involved to get React, TypeScript, and all the other packages to work together, but Vite takes care of that for us. Some of the frontend code, therefore, was auto-generated.

Alternatives to React include AngularJS and Vue.js.

<details>
<summary><strong>🤔 For new developers: If you're completely new to React…</strong></summary>

_…we recommend checking out the official [React quick start guide](https://react.dev/learn). The main concepts you should understand are **components, props, state, and side effects.** You can skim through those docs or do the entire tic-tac-toe tutorial before starting on this guide—we can provide support for that too in the **#onboarding** channel._

</details>

</details>

### Vitest

[Vitest](https://vitest.dev) is an **automated testing framework for Vite projects** that can work with many other specialized technologies, including React. We won't actually do much regarding testing in this guide because our focus is on core web development skills, but your engineering manager may place more emphasis on testing for your project.

Vitest is modeled after another well-known testing framework called [Jest](https://jestjs.io), following essentially the same patterns.

We also use [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) for extra powerful integration with React. RTL essentially simulates a browser, including the ability to render React components and trigger user interaction events.

On the backend, we use [pytest](https://docs.pytest.org), the most popular testing framework for Python. The backend starter code includes one small pytest test, which you can use as a starting point if you want to write more.

### TSE Constellation

[TSE Constellation](https://github.com/TritonSE/TSE-Constellation) is a **TSE-specific design system and library** for TSE projects. It's a library of React components for common frontend functionality, including buttons, input fields, popups, accordions, and much more!

We've been aiming to adopt Constellation into our TSE projects over the past couple years because it helps developers save time by not having to write standard, reusable components that are largely the same in every project. Interactive documentation for Constellation with demos and examples can be found on the [Storybook page](https://tritonse.github.io/TSE-Constellation/?path=/docs/welcome--documentation).

For examples of using Constellation in a real TSE project, see the [example project](https://github.com/TritonSE/Constellation-Example-Project), [TSE website](https://github.com/TritonSE/tritonse.github.io), and [Fulcrum](https://github.com/TritonSE/TSE-Fulcrum). Constellation is still a new library and may have some bugs or lack of extensibility, so please message the **#onboarding** Slack channel if you run into issues of have suggestions to improve it!

### Git and GitHub

<details>
<summary><strong>About Git and GitHub</strong></summary>

[Git](https://git-scm.com) is a **version control system** that tracks changes to source code files. You can think of a Git **repository** ("repo" for short), like this onboarding guide, as a special folder that stores the history of each file inside it. When we make new changes to our code, we **commit** them to the repository so they become part of that history.

[GitHub](https://github.com) is a **cloud-based Git service** where we can host repositories for an entire team to access. You can see all of TSE's past and current projects, including this guide, under our [TritonSE GitHub organization](https://github.com/TritonSE). Alternatives to GitHub include GitLab and Bitbucket.

<details>
<summary><strong>🤔 For new developers: Learn Git!</strong></summary>

_Git is an incredibly useful, industry-standard tool that UCSD's computer science classes don't cover in great detail. We highly recommend learning how to use it properly (this guide includes some tips), because it will help you contribute more effectively to TSE and will boost you in your internship/job search. Also, feel free to show off your TSE projects on your public GitHub profile!_

</details>

Git is useful because we can go back to a previous version of the repo if necessary—for example, if we realize there's a critical bug that we need to remove immediately before starting to work on a fix. More importantly, it allows multiple people to collaborate on the same code base without accidentally interfering with each other. Each developer can **pull** the latest version of the code from GitHub, make their own changes to finish their task, **push** their changes back to GitHub, and then **merge** their changes in so everyone else can access them.

Throughout this guide, we include pointers on Git usage to help you practice the workflow.

</details>

### Figma

<details>
<summary><strong>About Figma</strong></summary>

[Figma](https://www.figma.com) is an **online collaborative design prototyping software** used by many software companies. It's like Google Docs in that multiple people can work on the same file at the same time. It also has many tools for developers to help translate Figma designs into code, so feel free to play around with it to get some practice. We'll discuss Figma and our todo app designs more in [Part 0](./part-0/).

</details>

## Quick links

Here are some links to documentation and guides that you may find helpful:

- Mozilla Developer Network (MDN) references: Each is detailed and thorough, often with explanations of best practices too
  - [JavaScript reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference)—syntax, operators, built-in objects and functions
  - [HTML reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference)—elements and attributes
  - [CSS reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference)—properties, pseudo-classes, selectors
- [TypeScript language reference](https://www.typescriptlang.org/docs/handbook/utility-types.html)
  - Also see the [Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) for a higher-level overview of each concept
- [Python documentation](https://docs.python.org/3/)
  - Also see the [Python tutorial](https://docs.python.org/3/tutorial/) for an introduction to the language
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) - step-by-step guides to each feature
  - Also see the [FastAPI reference](https://fastapi.tiangolo.com/reference/) for the details of each class and function
- [Pydantic documentation](https://docs.pydantic.dev/latest/) - models, fields, and validators
- [PyMongo documentation](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/) - guides to connecting to MongoDB and writing queries
  - Also see the [PyMongo async API reference](https://pymongo.readthedocs.io/en/stable/api/pymongo/asynchronous/index.html) for the details of each class and method that we use
- [React reference](https://react.dev/reference/react)
  - [Built-in hooks](https://react.dev/reference/react/hooks)
  - [Built-in DOM components](https://react.dev/reference/react-dom/components)
- [CSS-Tricks flexbox guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

## Before we begin

This process is **not** an assessment of your skill level. There is no competition or evaluation based on your "performance." So, don't hesitate to use all of the resources available to you to better understand the concepts we discuss. Consult the Internet, your peers, the **#onboarding** Slack channel, your engineering manager, PVP members, or whoever/whatever else comes to mind! We want to facilitate the learning process for you, and we know it's subjective and unique to each individual. Do whatever it takes to maximize your own learning.

If you want to ask a question in **#onboarding**, just remember to include which part of the guide you're working on, the specific thing you're stuck on or want to know more about, and any relevant code that you've written if applicable. This information will help us help you faster!

Also, keep in mind that this guide is not comprehensive. We prioritized the ideas and challenges that you're most likely to encounter at TSE, while including plenty of links to official docs and other resources in case you'd like to learn more. We hope you'll feel empowered to explore further on your own!

Finally, if you find any errors/broken links or have any feedback, please reach out to **#onboarding.** Your voice is valuable in helping us iterate and improve on our processes.

With all that out of the way, let's get started!

| Next                                                                   |
| ---------------------------------------------------------------------- |
| [Part 0. Project setup and introduction to the code](/writeup/part-0/) |
