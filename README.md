# job-posting-extractor-project
Pipeline to process and model job postings to create a robust database that will serve as the "single source of truth" for future analysis and applications.

Master branch: main
Development branch: develop
GitFlow: 
main: Master branch
develop: Development branch
For this process I'll use the next convention: branch-scope/descriptio-name
    feature: add new functionality
    bugfix: solve a problem non criticall
    docs: add docummentation lines
    test: add test cases

Poetry: Manage the Python project dependencies, virtual environment, and packaging in one place.
Make: Manage scripts, define commands for common tasks.

Development Dependencies for code quality, test code, keep style consistent, and catch bugs early:
pytest : runs automated tests. You write test files, and  pytest  discovers and executes them to verify your ETL code works as expected.
ruff : checks code quality and style, and it can also format code. It is very fast and is often used to catch linting issues like unused imports, bad patterns, or import ordering.
black : formats Python code automatically so your code style stays consistent across the team.
mypy : checks types statically, meaning it looks for type errors before you run the program.


Dataset: data_jobs.csv
