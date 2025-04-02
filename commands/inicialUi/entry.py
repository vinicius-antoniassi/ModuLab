import adsk.core
app = adsk.core.Application.get()
ui = app.userInterface

# Define the location where the tab will be created. 
WORKSPACE_ID = 'FusionSolidEnvironment'

MODULES_TAB_ID = 'ModulesTab'
MODULES_TAB_NAME = 'Modules'

INICIAL_PANEL_ID = 'InicialPanel'
INICIAL_PANEL_NAME = 'Inicial Panel'

# Executed when add-in is run.
def start():
    # Get the DESIGN workspace.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Add a custom tab.
    modules_tab_add = workspace.toolbarTabs.add(MODULES_TAB_ID, MODULES_TAB_NAME)

    # Add a inicial panel to the tab.
    inicial_panel_add = modules_tab_add.toolbarPanels.add(INICIAL_PANEL_ID, INICIAL_PANEL_NAME)
    

# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    modules_tab = workspace.toolbarTabs.itemById(MODULES_TAB_ID)
    inicial_panel = workspace.toolbarPanels.itemById(INICIAL_PANEL_ID)

    # Delete the button command control
    if modules_tab:
        modules_tab.deleteMe()

    # Delete the command definition
    if inicial_panel:
        inicial_panel.deleteMe()