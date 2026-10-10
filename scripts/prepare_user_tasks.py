import json
from collections import defaultdict
from pathlib import Path
import shutil
import os
import stat
from urllib.parse import quote


############################################################
# CHANGE THIS
# TODO: set this in a config file
############################################################
BASE = Path("/Users/royadams/OneDrive - Johns Hopkins/scratch/test_shared_ls_project")
############################################################

master_file = BASE / "assignments" / "master_assignments.json"
out_dir = BASE / "assignments"
docs_dir = BASE / "docs"

with open(master_file, "r", encoding="utf-8") as f:
    docs = json.load(f)

user_tasks = defaultdict(list)

users = set([user for doc in docs for user in doc["assigned_to"]])

for user in users:
    # out_file = out_dir / f"{user}_tasks.json"
    # with open(out_file, "w", encoding="utf-8") as f:
    #     json.dump(tasks, f, indent=2, ensure_ascii=False)
    # print(f"Wrote {len(tasks)} tasks to {out_file}")
    
    # Create directories and config files for each annotator
    user_dir = BASE / "users" / user
    
    # create user dir if not exists
    user_dir.mkdir(parents=True, exist_ok=True)

    run_script_file = BASE / "scripts" / "run.py"
    shutil.copy(run_script_file,user_dir)
    
    user_docs_dir = user_dir / "docs"
    user_docs_dir.mkdir(parents=True, exist_ok=True)
    
    user_ls_dir = user_dir / "label_studio_data"
    user_ls_dir.mkdir(parents=True, exist_ok=True)
    
    user_annotations_dir = user_dir / "annotations"
    user_annotations_dir.mkdir(parents=True, exist_ok=True)
    
    user_setup_dir = user_dir / "setup"
    user_setup_dir.mkdir(parents=True, exist_ok=True)
    
    setup_file = user_setup_dir / f"{user}_setup.sh"
    
    setup_str = f"""#!/usr/bin/env bash
export LABEL_STUDIO_BASE_DATA_DIR="{user_ls_dir}"
label-studio start --port 8080"""
    
    with open(setup_file,'w',encoding="utf-8") as f:
        f.write(setup_str)
        
    current_permissions = os.stat(setup_file).st_mode
    # Bitwise OR (|) to add owner execute permission (u+x)
    os.chmod(setup_file, current_permissions | stat.S_IXUSR)
    
    print(f"Set up users/{user}")

for doc in docs:
    doc_id = doc['id']
    file_name = doc['file']
    file_path = docs_dir / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"Missing document file for {doc_id}: {file_path}")
        
    for user in doc["assigned_to"]:
        user_docs_dir = BASE / "users" / user / "docs" / file_name
        shutil.copy(file_path,user_docs_dir)


    
    
    