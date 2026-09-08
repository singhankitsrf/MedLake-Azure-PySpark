# MedLake PySpark on Hugging Face

Target Space: `singhankit491/medlake-pyspark` (a deployment target, not a claim that it is live).

## Run locally

From the repository root:

```bash
pip install -r hf_space/requirements.txt
PYTHONPATH=.:src python hf_space/app.py
```



Java 17 is required. Docker installs it automatically.

## Build the exact deployment

```bash
pip install huggingface_hub==1.30.0
python scripts/publish_space.py --repo-id singhankit491/medlake-pyspark --stage-only /tmp/medlake-pyspark-space
docker build -t medlake-pyspark /tmp/medlake-pyspark-space
docker run --rm -p 7860:7860 medlake-pyspark
```

The staging command copies only tracked allowlisted source files. Commit intended changes first.
Patient data, local credentials and trained checkpoints are excluded.

## Publish

Authenticate securely with `hf auth login`, then run:

```bash
python scripts/publish_space.py --repo-id singhankit491/medlake-pyspark
```

Alternatively, configure a narrowly scoped Hugging Face write token as the GitHub Actions secret
`HF_TOKEN` and run the **Hugging Face Space** workflow. It builds and checks application startup before uploading.
No token belongs in source code, a README, a Docker build argument, or a chat message.
The workflow uses default CPU Space hardware and does not request paid GPU resources.

After publishing, wait for the Hugging Face build to finish, open the application, execute its example,
and verify the displayed output. Record the Space commit and the GitHub source revision.
The upload script reports current runtime state but does not mistake BUILDING for RUNNING.

## Scope

Run a real PySpark data-quality pipeline on synthetic events. The AWS/Azure infrastructure remains in GitHub and requires its own account deployment.
This CPU demonstration is not evidence of clinical validation or a measured production cloud deployment.
