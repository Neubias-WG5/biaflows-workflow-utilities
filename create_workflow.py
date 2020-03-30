import os
import sys
import base64
import requests
import json
from subprocess import call
from cytomine import Cytomine
from cytomine.utilities.descriptor_reader import read_descriptor

def create_github_repo(auth, params):
    """
    Create a new GitHub repository from existing template.

    Parameters:
      auth: dict,
        includes 'username' and 'token' items for GitHub authentication
      params: dict,
        includes 'gh_owner', 'name', 'description', 'private' and 'template'
        items to describe the new repository
    Return:
      HTTP response, response.status_code == 201 for successful creation
    """
    data = {'owner': params['gh_owner'],
            'name': params['name'],
            'description': params['description'],
            'private': params['private']}
    
    response = requests.post(
        'https://api.github.com/repos/{}/{}/generate'.format(params['gh_owner'],params['template']),
        auth=(auth['username'],auth['token']),
        headers={'Accept': 'application/vnd.github.baptiste-preview+json'},
        data=json.dumps(data)
    )
    
    return response

def create_dockerhub_repo(auth, params):
    """
    Create a new DockerHub repository.

    Parameters:
      auth: dict, includes items 'username' and 'password' for DockerHub
        authentication
      params: dict, includes items 'dh_namespace', 'name', 'description',
        'private' items to describe the new repository
    Return:
      HTTP response, response.status_code == 201 for successful creation
    """
    # Login to get token
    token = ''
    response = requests.get(
        'https://hub.docker.com/v2/users/login',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'username': auth['username'],
                         'password': auth['password']})
        )

    if response.status_code == 200:
        token = json.loads(response.text)['token']
    else:
        return response

    data = {'namespace': params['dh_namespace'],
            'name': params['name'].lower(),
            'description': params['description'],
            'full_description': params['description'],
            'is_private': params['private']}
    
    response = requests.post(
        'https://hub.docker.com/v2/repositories/',
        headers={'Authorization': 'JWT {}'.format(token),
                 'Content-Type': 'application/json'},
        data=json.dumps(data)
        )

    return response

def modify_default(params, workflow_params, clonedir):
    """
    Modify default files copied from GitHub template repository

    Parameters:
      params: dict, includes 'gh_owner', 'name', 'description' and
        'dh_namespace' items to update the files and handle modifications
    Return:
      int, 0 if successful, otherwise error code from subprocess.call
    """
    repo_address = "https://github.com/{}/{}.git".format(params['gh_owner'],params['name'])
    command = "git clone {}".format(repo_address)
    return_code = call(command, shell=True, cwd=clonedir)
    if return_code != 0:
        return return_code

    desc_path = os.path.join(clonedir,params['name'],"descriptor.json")
    with open(desc_path) as fh:
        desc = json.load(fh)
    desc['name'] = params['name']
    desc['description'] = params['description']
    desc['container-image']['image'] = params['dh_namespace']+'/'+params['name'].lower()

    # Add workflow parameters
    for wp in workflow_params:
        param = {
            "id": wp['name'].lower().replace(' ','_'),
            "name": wp['name'],
            "description": wp['description'],
            "default-value": wp['default-value'],
            "type": wp['type'],
            "set-by-server": False,
            "value-key": '@ID',
            "optional": True,
            "command-line-flag": '--@id'
            }
        desc['inputs'].append(param)
        desc['command-line'] += " {}".format(param['id'].upper())
    
    with open(desc_path,'w') as fh:
        json.dump(desc, fh, indent=4, separators=(',', ': '))

    readme_path = os.path.join(clonedir,params['name'],"README.md")
    with open(readme_path,'w') as fh:
        fh.write("# {}\n".format(params['name']))
        fh.write("{}".format(params['description']))
    
    return 0

def commit(auth, params, repodir, files):
    """
    Commit changed files to GitHub repository

    Parameters:
      auth: dict, includes items 'username' and 'token' for GitHub
        authentication
      params: dict, includes items 'gh_owner' and 'name' for identifying the
        modified repository
      repodir: str, local path to repository directory
      files: list, list of filenames
    Return:
      int/str: 0 if successful, HTTP response.text if an error
    """
    # Commit all files separately
    for fn in files:
        # Get file sha
        response = requests.get(
            'https://api.github.com/repos/{}/{}/contents/{}'.format(params['gh_owner'],params['name'],fn),
            headers={'Accept': 'application/vnd.github.v3+json'},
            auth=(auth['username'],auth['token'])
        )
        if response.status_code == 200:
            filesha = json.loads(response.text)['sha']
        else:
            return response.text

        with open(os.path.join(repodir,fn),"rb") as f:
            bcontent = base64.b64encode(f.read())
            scontent = bcontent.decode('utf-8')
        data = {"message": "Initial commit of {}".format(fn),
                "content": scontent,
                "sha": filesha}
    
        response = requests.put(
            'https://api.github.com/repos/{}/{}/contents/{}'.format(params['gh_owner'],params['name'],fn),
            headers={'Accept': 'application/vnd.github.v3+json'},
            auth=(auth['username'],auth['token']),
            data=json.dumps(data)
        )
        if response.status_code != 200:
            return response.text

    return 0

def main():
    with open('config.json') as jfile:
        data = json.load(jfile)
    gh_auth = data['gh_auth']
    dh_auth = data['dh_auth']
    params = data['params']
    workflow_params = data['workflow_params']

    # 1. Create a new GitHub repo
    gh_status = create_github_repo(gh_auth, params)
    if gh_status.status_code == 201:
        status_output = json.loads(gh_status.text)
        print("Successfully created a GitHub repository: {}".format(status_output['name']))
    else:
        print("Creation of a GitHub repository failed: {}".format(gh_status.text))
        sys.exit(1)

    # 2. Create a new DockerHub repo
    dh_status = create_dockerhub_repo(dh_auth, params)
    if dh_status.status_code == 201:
        status_output = json.loads(dh_status.text)
        print("Successfully created a DockerHub repository: {}".format(status_output['name']))
    else:
        print("Creation of a DockerHub repository failed: {}".format(dh_status.text))
        sys.exit(1)

    # 3. Modify template files
    status = modify_default(params, workflow_params, data['general']['clonedir'])
    if status == 0:
        print("Template files modified successfully")
    else:
        print("Failed to modify template files: {}".format(status))
        sys.exit(1)

    # 4. Make initial commit with modified files
    status = commit(gh_auth, params, os.path.join(data['general']['clonedir'],params['name']), ["descriptor.json", "README.md"])
    if status == 0:
        print("Modified files committed successfully")
    else:
        print("Failed to commit modified files: {}".format(status))
        sys.exit(1)

    return 0

if __name__=="__main__":
    main()
