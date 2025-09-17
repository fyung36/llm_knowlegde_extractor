## Getting started

To get started with this boilerplate, first install miniconda and create a new environment:

```bash
conda create -n lim_knowledgee_extractor python=3.12
```

Next, activate the environment:

```bash
conda activate lim_knowledgee_extractor
```

Finally modify the `.env` file with your database connection details and run the following command to install the dependencies:

```bash
pip install -r requirements.txt
```

## Migrations

To run the migrations, use the following command:

```bash
migrations upgrade head
```

## Running the app

To run the app, use the following command:

```bash
python runserver.py
```
