42cc TODO Test Task
----

# System requirements
- python 3.10
- nodejs 16.x or higher
- poetry 1.3.x
- pnpm 7.18.x
- Optionally heroku-cli, although you can use any other platform to host your application

# Local and remote deploy
Setup script should guide you through installation:
```shell
./scripts/setup.sh
```

If you're on Mac then make sure you have a normal `grep` installed and not the default one which is very limited (`brew install grep`).

If you cannot run the script, setup the app manually:
- Create *.env* file with the following content:
  - `DEBUG=True`
  - `ALLOWED_HOSTS=*`
- Double check system requirements.
- Create virtualenv using poetry, `poetry install`.
- Install git hooks, `poetry run pre-commit install`.
- Install frontend dependencies, `cd frontend && pnpm install`.
- Configure platform where your code will be deployed. You can take command to run server from *Procfile*.
- Make sure that you have `DEBUG=False`, `ALLOWED_HOSTS=domain.yourhosting.com` and `SECRET_KEY=random32lenstring` set
  on your server.

To make it easy we keep frontend build artifacts in repository: *frontend/static*, before deploying on server please run
`cd frontend && pnpm run build` to rebuild static assets.

# How to work

1. Assign the first issue (see Issues tab on Gitea repository page) to your self and start a timer
2. Create a separate branch to do the task
3. Read [task](TASK.md) description, understand the task requirements. If something is unclear - ask questions.
4. Plan your work ahead in the first comment of the issue and follow the plan (there is already an example).
5. Work aloud - write every 15-20 minutes what you are thinking about, questions, answers, URLs to documentation, code samples, where you're reading, git commit output, etc
6. When the task is finished create a PR. Self-review your code, cleanup any dead / commented-out code, print / console statements, run unittest tests.
7. Re-assign the task and the PR to your reviewer.

# How to code
1. You can prefix every command with `poetry run` or active virtualenv using `poetry shell`.
2. To start server run `poetry run inv devserver` (or, in activated virtualenv, `inv devserver`).
3. Local server is available at localhost:8000
4. [Options or Composition API?](https://vuejs.org/guide/introduction.html#api-styles) You probably know well the
    Options API if you know Composition API, use latter, otherwise take Options API.
