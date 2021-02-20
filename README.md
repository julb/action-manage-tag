![Build](https://github.com/julb/action-manage-tag/workflows/Build/badge.svg)

# GitHub Action to manage tages

The GitHub Action for managing tags of the GitHub repository.

- Create a new tag
- Update an existing tag
- Delete a tag

## Usage

### Example Workflow file

- Create a tag:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Create/Update the tag
        uses: julb/action-manage-tag@v1
        with:
          name: tag-name
          state: present
          from: ${{ github.ref }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- Delete a tag

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Delete the tag
        uses: julb/action-manage-tag@v1
        with:
          name: tag-name
          state: absent
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

| Name    | Type   | Default      | Description                                                                                                                                                 |
| ------- | ------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`  | string | `Not set`    | Name of the tag. **Required**                                                                                                                            |
| `state` | string | `present`    | Expected state of the tag. Valid values are `present` to create the tag or `absent` to delete the tag                                              |
| `from`  | string | `github.ref` | The reference from which to create tag - could be a tag, a branch, a ref or a specific SHA. By default, it takes the commit that triggered the workflow. |

### Outputs

| Name   | Type   | Description                                                                       |
| ------ | ------ | --------------------------------------------------------------------------------- |
| `ref`  | string | Git ref of the tag `refs/tags/tag-name`, or `none` in case the tag is deleted. |
| `name` | string | Name of the tag, or `none` in case the tag is deleted.                      |
| `sha`  | sha    | SHA Commit of the tag, or `none` in case the tag is deleted.                |

## Contributing

This project is totally open source and contributors are welcome.

When you submit a PR, please ensure that the python code is well formatted and linted.

```
$ make install.dependencies
$ make format
$ make lint
```
