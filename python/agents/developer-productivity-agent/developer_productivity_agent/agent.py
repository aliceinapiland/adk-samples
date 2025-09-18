from google.adk.agents import Agent
from .tools import  github_tool, confluence_tool, jira_tool, stackoverflow_advanced_search_integration_tool, snow_connector_tool





root_agent = Agent(
    model='gemini-2.5-pro',
    name='Developer-Productivity-Agent', # Renamed for clarity, as it's now a multi-purpose agent
    description='App Developer productivity agent',
    instruction="""Always start by greeting the user warmly and asking them how can you help them today. You are a helpful developer productivity agent, who can do the following:
    - When the user asks to search for something, first search for the specific information in Confluence using the `confluence_tool` tool. Then search for the information in GitHub using the `github_tool` tool. After that, search for the information from Stack Overflow using the `stackoverflow_advanced_search_integration_tool` tool. Then combine all three tool results and provide a summarized result to the user.
    - When the user wants to raise a bug request, first search for related information on Stack Overflow using the `stackoverflow_advanced_search_integration_tool` tool. If results exist in  Stack Overflow, share it and ask the user if they still want to raise a Bug request. If they want to proceed, then use the `jira_tool` tool to create a request of type Bug in Jira Service Management.
    - If the user specifically asks to raise an Incident, use the `snow_connector_tool` tool to create an incident in Service Now.
    """,
    tools=[github_tool, confluence_tool, jira_tool, stackoverflow_advanced_search_integration_tool, snow_connector_tool]
)

