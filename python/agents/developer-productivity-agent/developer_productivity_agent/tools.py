import os
from dotenv import load_dotenv

from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset
from google.adk.auth import AuthCredential, AuthCredentialTypes, OAuth2Auth

from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows

load_dotenv()

SNOW_CONNECTION_PROJECT_ID=os.getenv("SNOW_CONNECTION_PROJECT_ID")
SNOW_CONNECTION_REGION=os.getenv("SNOW_CONNECTION_REGION")
SNOW_CONNECTION_NAME=os.getenv("SNOW_CONNECTION_NAME")
SNOW_INSTANCE_NAME=os.getenv("SNOW_INSTANCE_NAME")
SNOW_OAUTH_SCOPES=os.getenv("SNOW_OAUTH_SCOPES")
AGENT_REDIRECT_URI=os.getenv("AGENT_REDIRECT_URI")
SNOW_CLIENT_ID=os.getenv("SNOW_CLIENT_ID")
SNOW_CLIENT_SECRET=os.getenv("SNOW_CLIENT_SECRET")

TOOL_INSTR="""
        **Tool Definition: ServiceNow Connector via Application Integration**

        This tool interacts with ServiceNow Incidents using an Application Integration Connector.
        It supports GET, LIST, and CREATE operations as defined for each entity.

         **Incident Getting:**

         If the user asks to get incident details:

        *   **Rendering User Response:**
            1. The user will input a sys_id value, use that value and the GET tool available to return the following (make it easy to read via rendering):
               - Incident Number (available in the "Number" JSON key/value)
               - Incident Description (available in the "Description" JSON key/value)
               - Ticket Creator (available in the "sys_created_by" JSON key/value)
               - Time of Creation (available in the "sys_created_on" JSON key/value)

        **Incident Creation:**

        If the user asks to create an incident:

        *   **Information Gathering:**
            1.  Collect minimal information from the user to describe the new incident. The only fields you should need to create an incident are the description, short_description, impact and urgency. Sample can be seen here: 
            {
              "description": "My Macbook Pro mouse is broken, I need a new one delivered to my home",
              "short_description": "I need a new mouse for my Macbook Pro",
              "impact": 2.0,
              "urgency": 2.0
            }
            Deduce appropriate values for `impact`, and `urgency` based on the user-provided details.
        *   **User Confirmation:**
            1.  Before calling into the tool, present the summarized details (description, deduced category, impact, urgency) to the user.
            2.  Ask for explicit confirmation from the user to proceed with creation

        *   **Rendering User Response:**
            1. Please provide a reference to the ID returned in the response for tracking purposes

"""


oauth2_scheme = OAuth2(
   flows=OAuthFlows(
      authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl=f"https://{SNOW_INSTANCE_NAME}.service-now.com/oauth_auth.do",
            tokenUrl=f"https://{SNOW_INSTANCE_NAME}.service-now.com/oauth_token.do",
            scopes={
                f"{SNOW_OAUTH_SCOPES}" : "default",
            }
      )
   )
)

oauth2_credential = AuthCredential(
  auth_type=AuthCredentialTypes.OAUTH2,
  oauth2=OAuth2Auth(
    client_id=SNOW_CLIENT_ID,
    client_secret=SNOW_CLIENT_SECRET,
    redirect_uri=AGENT_REDIRECT_URI # This is the ADK Web UI
  )
)

# Tool for ServiceNow
snow_connector_tool = ApplicationIntegrationToolset(
    project=SNOW_CONNECTION_PROJECT_ID,
    location=SNOW_CONNECTION_REGION,
    connection=SNOW_CONNECTION_NAME,
    entity_operations= {"Incident": ["GET","LIST","CREATE"]},
    tool_name_prefix="tool_snow",
    tool_instructions=TOOL_INSTR,
    auth_credential=oauth2_credential,
    auth_scheme=oauth2_scheme,
)

# Tool for GitHub
github_tool = ApplicationIntegrationToolset(
     project="bap-amer-south-demo1",
     location="us-central1",
     connection="ravindranv-github-conn",
     entity_operations={
         "Information.Repositories": ["GET","LIST"],
          "Information.OrganizationTeamRepositories": ["GET","LIST"]
     },
     tool_instructions="Use this tool when information has to be searched in Github"

 )

 # Tool for Confluence
confluence_tool = ApplicationIntegrationToolset(
     project="bap-amer-south-demo1",
     location="us-central1",
     connection="ravindranv-confluence-con",
     entity_operations={
         "Pages": ["GET","LIST"],
         "Spaces": ["GET","LIST"],
         "Blogposts": ["GET","LIST"],
         "Whiteboards": ["GET","LIST"]
     },
     # empty list for actions means all operations on the entity are supported
     # actions=["action1"],
     # service_account_credentials='{...}',
     # tool_name="ConfluenceTool",
      tool_instructions="Use this tool when information has to be searched in Confluence"
 )

# Tool for Jira Service Management
jira_tool = ApplicationIntegrationToolset(
     project="bap-amer-south-demo1",
     location="us-central1",
     connection="ravindranv-jsm-conn",
     entity_operations={
         "ServiceDesks": ["GET","LIST", "CREATE"],
         "RequestTypes": ["GET","LIST", "CREATE"],
         "Requests": ["GET","LIST", "CREATE", "UPDATE"]
     },
     # empty list for actions means all operations on the entity are supported
     # actions=["action1"],
      tool_instructions="Use this tool when Requests need to be created or retrieved from Jira Service Management"
 )

# Tool for stackoverflow
stackoverflow_advanced_search_integration_tool = ApplicationIntegrationToolset(
    project="bap-amer-south-demo1", # GCP project of the connection
    location="us-central1", # location of the integration
    integration="stackoverflow-advanced-search", # integration name
    triggers=["api_trigger/stackoverflow-advanced-search_API_1"],# trigger id(s). Empty list would mean all api triggers in the integration to be considered.
    # service_account_json='{...}', #optional. Stringified json for service account key
    # tool_name_prefix="tool_prefix1",
    tool_instructions="Use this tool to perform advanced search on Stack Overflow for questions and answers. The tool accepts a searchString input parameter."
)


