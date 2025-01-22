## Contributing

### Setup

First, install uv following the instructions at [uv-Astral](https://docs.astral.sh/uv/getting-started/installation/)

Then, setup the project by running the following command:

```bash
$ uv run dev-setup
```

### Development

To add new dependendencies to the project, run the following command:

```bash
$ uv add <package-name>
```

or

```bash
$ uv add --dev <package-name>
```

To make a new commit, follow the conventional commit message format at [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

This will run pre-commit hooks. It is possible that this will run some formatting and you will need to add the new changes to the commit again.
