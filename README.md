# BPY Tools

Some CLI and code tools to help with Blender Python development.
Includes opinionated tools and simple utilities to reduce code boilerplate and improve the development experience.

# Installation

Inlude the bpy_tools folder in the root of your addon.

# How To Use

TODO include wiki link

Run all CLI tools from the root of your addon. You might have to use `python3` instead of `python` depending on your system.
You can run all CLI tools with the `---help` flag to get more info on that tool.

## Setup Tools

These tools are meant to help you with the initial setup proces of your addon.

TODO

## Development Tools

These tools are meant to help you during the development process.

## Auto Load

TODO

## Export Tools

These tools are meant to help you with building and distributing your addon.

### Build to zip

```bash
python build_tools build
```

<details>
    <summary>Details</summary>
    
This CLI command will build your addon into a zip file.
It will remove \_\_pycache\_\_ as well as .git folders. It will also clean up unnecessary files from the bpy_tools folder that are only needed during development to reduce your build size.

You can run the command with the `--dirname` flag to provide the name of the folder to build to. If you don't provide a name it will ask you for one the first time you run the command. The tool will include this build folder in your .gitignore file if you have one.

</details>

# Contributing

TODO
