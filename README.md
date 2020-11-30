# biaflows-workflow-utilities
Utilities to simplify BIAFLOWS workflow creation. The complete documentation for creating a new workflow and adding it to a BIAFLOWS instance is available at:
https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html

These workflow creation utilities handle the following steps:\
**Step 1**. Create a GitHub repository for the new workflow (but not adding a trusted source to a BIAFLOWS server)\
**Step 2**. Add the required files to the workflow repository\
**Step 3**. Update the sections of the Descriptor\
**Step 7**. Compile the workflow repository as a BIAFLOWS Docker image from DockerHub\
**Step 10**. Build workflow Docker image (done automatically by DockerHub)

The following steps still need to be performed manually (workflow specific):\
**Step 4**. Update DockerFile (see [step 4](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html#workflow_step4))\
**Step 5**. Update wrapper script (see [step 5](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html#workflow_step5))\
**Step 6**. Update the workflow script (see [step 6](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html#workflow_step6))\
**Step 8**. Link DockerHub repository to the workflow GitHub repository, and configure automated build (see [step 8](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html#workflow_step8))

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
    - workflow_params: List of workflow parameter. For each parameter, set (see [step 3](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html#workflow_step3), workflow parameters section):
        - name: Name of the parameter
        - description: Parameter description (presented in BIAFLOWS)
        - default-value: Parameter default value
        - type: String either 'Number' or 'String'
3. Run create_workflow.py script (python3.6 create_workflow.py)
4. Link created DockerHub repository to workflow GitHub repository ([step 8](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html#workflow_step8))
5. Update created GitHub repository and commit changes to GitHub repository ([steps 4-6](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html#workflow_step4))
6. Follow workflow release and test ([steps 9-12](https://neubias-wg5.github.io/creating_bia_workflow_and_adding_to_biaflows_instance.html#workflow_step9))
