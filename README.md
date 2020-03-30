# biaflows-workflow-utilities
Utilities for simpler BIAFLOWS workflow creation. The full documentation for creating a new workflow and adding it to a BIAFLOWS instance is available at:
https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html

These workflow creation utilities handle following steps of a new workflow creation:
1. Create a workflow GitHub repository
2. Add the 4 required files to the workflow repository
3. Update sections of the Descriptor
7. Create Docker image in DockerHub

Following steps needs to be done manually as these are workflow specific tasks:
4. Update DockerFile
5. Update wrapper script
6. Adapt your workflow script
8. Link DockerHub repository to workflow GitHub repository and configure workflow Docker image automated build
9. Trigger a workflow release
10. Workflow Docker image build (done automatically by DockerHub)
11. Add workflow to BIAFLOWS problem
12. Run the workflow

## Instructions for a new workflow creation
1. Clone this repository: git clone https://github.com/Neubias-WG5/biaflows-workflow-utilities.git
2. Modify config.json file to include (see example W_NucleiSegmentation-ImageJ.json):
- clonedir: Local path to create the new repository
- gh_auth: Include your GitHub account details: username, authentication token, name and email
- dh_auth: Include your DockerHub account details: username and password (DockerHub API does not currently support authentication token)
- params:
  - gh_owner: GitHub organization
  - dh_namespace: DockerHub namespace
  - name: Name of the new workflow repository
  - description: Description of the repository
  - template: Template repository for the new workflow
- workflow_params: List of parameter definitions for the workflow. For each parameter, set (see more information in [step 3 Workflow parameter sections](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html)):
  - name: Name of the parameter
  - description: Parameter description (presented in BIAFLOWS)
  - default-value: Parameter default value
  - type: String either 'Number' or 'String'
3. Run create_workflow.py script (python3.6 create_workflow.py)
4. Link newly created DockerHub repository to workflow GitHub repository ([step 8](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html))
5. Adapt newly created GitHub repository to implement your workflow and commit the changes into GitHub repository ([steps 4-6](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html))
6. Follow workflow release and test [steps 9-12](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html)
