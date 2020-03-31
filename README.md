# biaflows-workflow-utilities
Utilities to simplify BIAFLOWS workflow creation. The complete documentation for creating a new workflow and adding it to a BIAFLOWS instance is available at:
https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html

These workflow creation utilities handle the following steps:\
**Step 1**. Create a GitHub repository for the new workflow\
**Step 2**. Add the 4 required files to the workflow repository\
**Step 3**. Update the sections of the Descriptor\
**Step 7**. Compile the workflow repository as a BIAFLOWS Docker image from DockerHub\
**Step 10**. Workflow Docker image build (done automatically by DockerHub)\

The following steps still need to be performed manually (workflow specific):\
**Step 4**. Update DockerFile (only necessary if the execution environment is different)\
**Step 5**. Update wrapper script\
**Step 6**. Copy/paste your workflow code to the workflow script\
**Step 8**. Link DockerHub repository to the workflow GitHub repository, and configure automated build\

And, as usual to trigger and test a new workflow release:\
**Step 9**. Trigger a workflow release (from GitHub workflow repository)\
**Step 11**. Add new workflow to a BIAFLOWS problem (from BIAFLOWS, on first release only)\
**Step 12**. Run the workflow (from BIAFLOWS)

## Instructions for a new workflow creation
1. Clone this repository: git clone https://github.com/Neubias-WG5/biaflows-workflow-utilities.git
2. Modify config.json file to include (see example [W_NucleiSegmentation-ImageJ.json](https://github.com/Neubias-WG5/biaflows-workflow-utilities/blob/master/W_NucleiSegmentation-ImageJ_example.json)):
    - clonedir: Local path to create the new repository
    - gh_auth: Include your GitHub account details: username, authentication token, name and email
    - dh_auth: Include your DockerHub account details: username and password (DockerHub API does not currently support authentication token)
    - params:
        - gh_owner: GitHub organization
        - dh_namespace: DockerHub namespace
        - name: Name of the new workflow repository
        - description: Description of the repository (max 100 characters, limitation of DockerHub)
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
