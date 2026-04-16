import os
from pathlib import Path

from huggingface_hub import HfApi


REPO_ID = "mertvoysal/I-Kit-Health-Pro"
REPO_TYPE = "space"
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

INCLUDE_PATHS = [
    ("app.py", "app.py"),
    ("thyroidDF.csv", "thyroidDF.csv"),
    ("requirements.txt", "requirements.txt"),
    ("Dockerfile", "Dockerfile"),
    ("README_SPACE.md", "README.md"),
    ("templates/index.html", "templates/index.html"),
    ("artifacts/catboost_thyroid_model.cbm", "artifacts/catboost_thyroid_model.cbm"),
    ("artifacts/model_metadata.json", "artifacts/model_metadata.json"),
]


def main() -> None:
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN is not set. Define HF_TOKEN and run again.")

    api = HfApi(token=token)
    who = api.whoami()
    print(f"Authenticated as: {who.get('name', 'unknown')}")

    api.create_repo(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        space_sdk="docker",
        exist_ok=True,
    )
    print(f"Space ready: https://huggingface.co/spaces/{REPO_ID}")

    for source_path, target_path in INCLUDE_PATHS:
        src = PROJECT_ROOT / source_path
        if not src.exists():
            raise FileNotFoundError(f"Missing required file: {src}")
        api.upload_file(
            path_or_fileobj=str(src),
            path_in_repo=target_path.replace("\\", "/"),
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            commit_message=f"Update {target_path}",
        )
        print(f"Uploaded: {source_path} -> {target_path}")

    print(f"Upload completed to https://huggingface.co/spaces/{REPO_ID}")


if __name__ == "__main__":
    main()
