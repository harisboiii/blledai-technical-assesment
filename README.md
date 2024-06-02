Demo video: https://www.loom.com/share/0041577268d144c4891470f364bf38ae




## Setup and Installation

### Conda Environment
1. Clone this repository.
2. Install Conda.
3. Create and activate a new Conda environment:

Run these commands to  activate conda environment with all libraries installed

   ```
conda env create -f environment.yml
conda activate myenv
```

```
pip install -r requirements.txt
```
# After downloading dependencies run this command to run the application:

```
uvicorn users:app --reload
```

# Running with Docker

1. Install Docker.
2. Run the following command to build and start the application:

```
docker run -p 8000:8000 bleed-ai
```







