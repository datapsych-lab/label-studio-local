# label-studio-local
This is repo contains a simple setup for coordinating use of Label Studio for annotations when you cannot run a server and instead only have a shared drive. The repo is populated with examples some examples, but the only code that really matters is in scripts. To set up a project, use the following steps:

## 0. Setup.
The only setup requirement is that Label Studio be installed on each annotator's computer. If running this on SAFE or SAFER, Label Studio is already installed.

## 1. Load documents and make assignments.
Copy all documents for annotation into the `docs/` directory. These should be `.txt` files. Then edit (or generate) the `assignments/master_assignments.json` file to assign each document to one or more annotators.

## 2. Create labeling schema.
Edit `schema/schema.xml` to reflect the labeling schema you would like to use. Label Studio has a lot of documentation on creating labeling schema.

## 3. Run prepare_user_tasks.py.
This will create individual user directories and populate them with their assigned documents. It will also place a copy of run.py in each user's directory which they will use to start label studio.

## 4. Set up each annotators Label Studio environment.
This is the most annoying manual part. There is probably a better way to do this, but I haven't figured it out. Complete the following steps for each annotator:
1. Go to the annotators directory (e.g., `cd users/alice`).
2. Run `./setup/<user>_setup.sh`. This will set an environment variable and run Label Studio.
3. Log in with the username `<user>@annotation.local` and password `annotation`.
4. Create a new project and give it a title. This project is specific to the annotator.
5. In the documents tab, load the documents from `users/<user>/docs`.
6. In the Labeling Setup tab, click `Custom template` at the bottom left. Then copy the contents of `schema/schema.xml` to the `Labeling Interface` window.
7. Click `Save`, exit the browser window, kill Label Studio, and repeat for any remaining annotators.

## 5. Start annotating.
Each annotator can now navigate to their directory, double click `run.py` to start Label Studio, log in with username `<user>@annotation.local` and password `annotation`, and annotate away.

## 6. Exporting annotations.
Once annotators finish, you or they can export their annotations by running their `run.py`, opening the project, and clicking export. 
