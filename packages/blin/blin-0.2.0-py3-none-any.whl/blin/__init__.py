import requests

url = "https://blin.lemeni.cloud"

def version():
    """
    blin package version

    Returns:
    str: blin package version
    """
    return "0.2.0"


class HTTPError(Exception):
    def __init__(self, response):
        super().__init__(f'HTTPError {response.status_code}: {response.reason}. Content: {response.text}' )

class Error(Exception):
    def __init__(self, what):
        super().__init__(what)

def result(response, expectedResult=None, orError=None):
    if response.status_code != 200:
        raise HTTPError(response)

    if expectedResult and response.json()['result'] != expectedResult:
        raise Error(orError)

    return response.json()['result']



def create_project(project_id, settings, key):
    """
    Create project. All learned commands/texts will be stored in it

    Parameters:
    project_id (str) : project identifier 
    settings (dict)  : project settings dict with following required fields:
     {
        "openai_key"    : <openapi_key>,
        "pinecone_key"  : <pinecone_key>,
        "pinecone_index": <pinecone_index_name>,
     }
    key (str) : blin authorization key

    Returns:
    str: result. Raises exception if the project was already created.
    """
    response = requests.post(f"{url}/project/{project_id}",
        headers={"authorizationToken": key},
        json   ={"settings": settings})
        
    return result(response, expectedResult='Created', orError="Project with this id already exists")
    

def open_project(project_id, key):
    """
    Open created project for learning or usage

    Parameters:
    project_id (str)    : project identifier     
    key (str)           : blin authorization key

    Returns:
    Project: Project object
    """
    return Project(project_id, key)

def delete_project(project_id, key):
    """
    Delete the project

    Parameters:
    project_id (str)    : project identifier     
    key (str)           : blin authorization key

    Returns:
    str: result. Raises exception if the project was not deleted.
    """
    response = requests.delete(f"{url}/project/{project_id}", 
        headers={"authorizationToken": key})

    return result(response, expectedResult='Deleted', orError="Error during project deletion")
   

class Project():
    def __init__(self, project_id, key):
        self.project_id = project_id
        self.key   = key

        self.headers={ "authorizationToken": self.key }
                     
    
    def learn_commands(self, commands):
        """
        Add commands to the project

        Parameters:
        commands (dict)      : command to learn in the format:
        {
            "command_name"  : {
                "brief"     : "string description of command purpose",
                "parameters": {
                    "<parameter_name>": "string description of parameter purpose, type, range",
                    ...
                }
        }

        Returns:
        None
        """
        for command_name, command_data in commands.items():
            response = self._call_learn(command_name, command_data, _type='command')
            

    def learn_texts(self, texts):
        """
        Add texts to the project
        
        Parameters:
        texts (dict)   : texts to learn in the format:
        { "text_name"  : "<text>", ... }

        Returns:
        None
        """
        for text_name, text_data in texts.items():
            response = self._call_learn(text_name, text_data, _type='text')


    def request(self, request):     
        """
        Return command to execute or/and text response based on user request and project knowledge

        Parameters:
        request (str)  : user request 

        Returns:
        dict: command to execute (can be {}) and text response (can be "") in the format:
        {
            "commands"  : <commands_dict>,
            "text"      : "text response"
        }
        """    
        response = requests.get(f"{url}/project/{self.project_id}/command",
            headers=self.headers,
            json   ={'request':request})
        
        return result(response)


    def recall_command_names(self):
        """
        Return a list of names of all learned commands

        Returns:
        list: names of all learned commands
        """  
        response = requests.get(f"{url}/project/{self.project_id}/knowledge",
            headers=self.headers,
            json   ={'type':'command'})

        return result(response)

    def recall_text_names(self):
        """
        Return a list of names of all learned texts

        Returns:
        list: names of all learned texts
        """  
        response = requests.get(f"{url}/project/{self.project_id}/knowledge",
            headers=self.headers,
            json   ={'type':'text'})

        return result(response)

    def recall(self, name):
        """
        Return learned command or text for given name

        Parameters:
        name (str) : command or text name

        Returns:
        dict: learned command or text (see learn_commands, learn_texts)
        """  
        response = requests.get(f"{url}/project/{self.project_id}/knowledge/{name}", headers=self.headers)
        return result(response)
        
    def forget(self, name):
        """
        Delete the knowledge (command of text)

        Parameters:
        name (str) : command or text name

        Returns:
        str: result. Raises exception if the knowledge was not deleted. 
        """  
        response = requests.delete(f"{url}/project/{self.project_id}/knowledge/{name}", headers=self.headers)
        
        return result(response, expectedResult='Deleted', orError="Error during knowledge deletion")


    def _call_learn(self, name, data, _type):
        response = requests.post(f"{url}/project/{self.project_id}/knowledge/{name}",
            headers=self.headers,
            json   ={'knowledge': {name:data},'type':_type})        
        
        return result(response)





