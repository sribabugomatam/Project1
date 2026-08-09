# Chapter 7: Git and GitHub Basics for This Project

Git is a version control system. It helps you track changes to your project over time.

GitHub is a website and service that hosts Git repositories online.

## Why Git is important

Git helps you:

- Save snapshots of your work
- Track changes over time
- Collaborate with others
- Restore earlier versions if needed

## Basic Git workflow

A typical workflow looks like this:

1. Create or clone a repository
2. Make changes to files
3. Stage the changes
4. Commit the changes
5. Push them to GitHub

## Clone a repository

To clone a repository from GitHub:

```bash
git clone https://github.com/your-username/your-repo.git
```

Example:

```bash
git clone https://github.com/sribabugomatam/Project1.git
```

## Check repository status

```bash
git status
```

This shows which files were changed, added, or deleted.

## Stage files

```bash
git add .
```

This stages all changes.

## Commit changes

```bash
git commit -m "Add new feature"
```

Good commit messages are short and clear.

## Push to GitHub

```bash
git push origin main
```

## Pull latest changes

```bash
git pull origin main
```

## Create a new branch

```bash
git checkout -b feature-name
```

## Switch branches

```bash
git checkout main
```

## Best practices for Git

- Commit often
- Write meaningful commit messages
- Do not commit large generated files unless needed
- Keep changes focused
- Pull before pushing if you are working with others

## GitHub repo remote setup

If you want to connect a local folder to GitHub:

```bash
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

## Summary

Git and GitHub are essential for modern development. Learning these basics will help you manage your code safely and professionally.

## Next chapter

Next, we will explain how to run the application from start to finish.
