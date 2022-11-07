# Python Style Guide / Coding Standards

This style guide is a list of do’s and don’ts for Python data pipeline development.

---

## Contents

1. Naming conventions and standards
2. General guidelines.
3. Linting, autoformatting and security plugins

---

## 1. Naming conventions and standards

### 1.1. Use the `snake_case` naming convention

* All code (objects, variables etc) including column names and associated objects created should be named using `snake_case`
* Snake case combines words by replacing each space with an underscore (_) and all letters are lower case, as follows:

**Raw**: user login count

**Snake case**: `user_login_count`

* [The following link](https://betterprogramming.pub/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841) explains the differences between different case styles.
* One of the benefits of Snake case is that many of the allowed characters are compatible across S3 and Snowflake

### 1.2. Naming of functions, variables and filenames

* Function names, variables and filenames should all be descriptive, eschew abbreviation
* In particular, don’t use abbreviations that are ambiguous to readers outside your projects
* Also don’t abbreviate by deleting letters within a word

### 1.3. String formatting: use f-strings

* `f-strings` should be used where possible, they provide a clean way to format strings
* Avoid using `str().format`
* Detailed examples of `f-strings` in action can be found [here](https://realpython.com/python-f-strings/).

### 1.4. Comments and Docstrings

#### 1.4.1. Comments

Comments **SHOULD** detail **why** something is being done, as well as **what** is occurring.

##### Example of *good* commenting

```python
# Display Ads are not included in the Product Count due to them being…
# This business rule was requested by the … team for these reasons …
```

##### Example of *bad* commenting

``` # Looping through list, setting Product Count to 0 where Type == ‘Display’ ```

##### `#TODO` keyword

* There are times when not everything can be built into a pipeline within the given time frames
* The `#TODO` keyword **MAY** be used to help future you

#### 1.4.2. Docstrings

##### Description

All pipelines and functions should start with a Docstring, explaining **what** the pipeline / function is, **what** it does and **why**.

##### Business logic / rules

* Business rules / logic should be explained at a high-level, focussing on **why** something is happening
* This is to help data engineers who open your pipelines in 1-2 years team and try to decipher what business rules exist and why they are being applied
* If a pipeline or transform doesn’t have any business rules, then you can leave this blank

###### Example **good** business logic / rule comments

```python

# Product codes X, Y and Z are excluded from metric revenue as hey are considered free ads
# Finance has requested for these to be excluded

```

###### Example **bad** business logic / rule comments

``` # Dim abc inner joins to Dim xyz and selects all fields ```

##### Parameters

Parameters required by the pipeline should be listed along with a description of what they are

##### Example Doc String

```python
"""
Description:
This pipeline is a sample pipeline, at the top of each pipeline we explain what the pipeline is and what it does
Business rules / logic:
Detail business logic at a high-level that might not be visible at first glance to the developer
E.g. Test Accounts are excluded from this pipeline
Parameters:
input_file_raw:
    Raw customer table
output_file_path:
    Output S3 file

Example usage:
    Include example usage if it is a global transform and the function can be used in multiple different ways.
    This section is not required for local transforms.
"""
```

---

## 2. General guidelines

### 2.1. Code readability and effective white spacing

Code **MUST** be spaced logically to maintain readability.

#### Example of **good** code readability

```python
# Pipeline parameters
src_bucket = self.s3_bucket_src
logging.info(f”source_bucket = {src_bucket}”)

target_bucket = self.s3_bucket_target
logging.info(f”target_bucket = {target_bucket}”)
```

#### Example of bad **code** readability

```python
# Pipeline parameters
src_bucket = self.s3_bucket_src
logging.info(f”source_bucket = {src_bucket}”)
target_bucket = self.s3_bucket_target
logging.info(f”target_bucket = {target_bucket}”)
```

### 2.2. Don’t capture change history / log

* The change history of a data pipeline SHOULD NOT be stored in the code itself
* Manually maintaining the change history in the code itself is unreliable, as it doesn’t show the actual change that has occurred and isn’t enforceable
  * The change history is captured by the version control system (e.g. Git) for each commit that’s occurred. All changes that are pushed to development and production are captured and diffs of those changes are available
* An example of the anti-pattern that SHOULD NOT be used:

```python
# Create by: Joe Bloggs
# Date: 01-01-2021
# Purpose: Eg transformation script

# Change log:
# Date: 02-01-2021
# Change Made By: Donald Duck
# Change Description: Small change to JSON file read in
```

### 2.3. Style guide decisions

Consider reading the [Google Python style guide](https://google.github.io/styleguide/pyguide.html), it gives great examples with do’s and don’t on writing clean code.

---

## 3. Linting, autoformatting and security plugins

* Standard linting and code formatting plugins can be used to maintain code quality and standardised formatting
* Pipelines should all have ‘problems’ identified by the plugins resolved prior to deployment to development or production systems
* Code not meeting these standards will be rejected by the CICD pipeline and the build will fail

### 3.1.Setup Instructions (for VSCode)

#### 3.1.1. VSCode Extensions

Install the following VSCode extensions (plugins):

* Docker
* Bracket Pair Colorizer 2

#### 3.1.2. Linting, Security and Autoformatting Plugin Settings

* Within VSCode, go to Settings -> Open Settings (JSON) – Icon Top Right
* From there, add the following additional settings:

```bash
"python.linting.flake8Enabled": true,
"python.linting.banditEnabled": true,
"python.linting.pylintEnabled": false,
"python.linting.flake8Args": [
    "--extend-ignore=F401"
],
"files.trimTrailingWhitespace": true,
"python.formatting.provider": "black",
"python.formatting.blackArgs": [
    "--line-length",
    "200"
],
"python.formatting.blackPath": "black",
"[python]": {
    "editor.formatOnSave": true,
}
```
