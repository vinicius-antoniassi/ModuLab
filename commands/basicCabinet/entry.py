import adsk.core
import os
from ...lib import fusionAddInUtils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface


# Specify the command identity information. ***
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_cmdBasicCabinets'
CMD_NAME = 'Command Basic Cabinet'
CMD_Description = 'A Fusion Add-in Command to create a basic cabinet'

# Specify that the command will be promoted to the panel.
IS_PROMOTED = True

# Define the location where the command button will be created. ***
# This is done by specifying the workspace, the tab, and the panel, and the 
# command it will be inserted beside. Not providing the command to position it
# will insert it at the end.
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'InicialPanel'
PROJECT = app.data.activeProject

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []

# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get the panel the button will be created in.
    panel = workspace.toolbarPanels.itemById(PANEL_ID)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def)

    # Specify if the command is promoted to the main toolbar. 
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()


# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to the command related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    # https://help.autodesk.com/view/fusion360/ENU/?contextId=CommandInputs
    # Define the dialog for your command by adding different inputs to the command.
    inputs = args.command.commandInputs

    # Create value input fields for frame specs.
    inputs.addValueInput('width', 'Largura', 'cm', adsk.core.ValueInput.createByReal(80))
    inputs.addValueInput('height', 'Altura', 'cm', adsk.core.ValueInput.createByReal(65))
    inputs.addValueInput('depth', 'Profundidade', 'cm', adsk.core.ValueInput.createByReal(30))
    inputs.addValueInput('thickness', 'Grossura MDF', 'cm', adsk.core.ValueInput.createByReal(1.5))       

    # Connect to the events that are needed by this command.
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)

# This event handler is called when the user clicks the OK button in the command dialog or 
# is immediately called after the created event not command inputs were created for the dialog.
def command_execute(args: adsk.core.CommandEventArgs):

    # Get a reference to your command's inputs.
    inputs = args.command.commandInputs
    width = inputs.itemById('width').value
    height = inputs.itemById('height').value
    depth = inputs.itemById('depth').value
    thickness = inputs.itemById('thickness').value

    # Get the active Fusion design
    design = adsk.fusion.Design.cast(app.activeProduct)
    rootComp = design.rootComponent

    allOccs = rootComp.occurrences
    transform = adsk.core.Matrix3D.create()

    # Create a component and a sub component (the sub component is the one we work with)
    occ1 = allOccs.addNewComponent(transform)
    subComp1 = occ1.component

    # --------- Sketch 1 (sides + back) ------------- #
    # Create a new sketch on the XY plane
    sketches1 = subComp1.sketches
    xzPlane = rootComp.xZConstructionPlane 
    sketch1 = sketches1.add(xzPlane)

    # Draw outer profile
    sketch1.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(width, height, 0)
    )

    # Draw inner profile
    sketch1.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(thickness, thickness, 0),
        adsk.core.Point3D.create(width - thickness, height - thickness, 0)
    )
    # --------- End of Sketch 1 ------------- #

    # --------- Extrude 1 (sides) -------------#
    # Get the profile of the first sketch
    prof1 = sketch1.profiles.item(0)

    # Create an extrusion input
    extrudes1 = subComp1.features.extrudeFeatures
    extInput1 = extrudes1.createInput(prof1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    # Get the distance from the input
    distance1 = adsk.core.ValueInput.createByReal(depth)
    extent_distance1 = adsk.fusion.DistanceExtentDefinition.create(distance1)

    # Set the distance extent
    extInput1.setOneSideExtent(extent_distance1, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    # Set the extrude type to be solid
    extInput1.isSolid = True
    
    # Create the extrusion
    ext1 = extrudes1.add(extInput1)
    # --------- End of Extrude 1 ------------- #

    # --------- Extrude 2 (back) ------------- #
    # Get the profile of the first sketch
    prof2 = sketch1.profiles.item(1)

    # Create an extrusion input
    extrudes2 = subComp1.features.extrudeFeatures
    extInput2 = extrudes2.createInput(prof2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    # Get the distance from the input
    distance2 = adsk.core.ValueInput.createByReal(thickness)
    extent_distance2 = adsk.fusion.DistanceExtentDefinition.create(distance2)

    # Set the distance extent
    extInput2.setOneSideExtent(extent_distance2, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    # Set the extrude type to be solid
    extInput2.isSolid = True
    
    # Create the extrusion
    ext2 = extrudes2.add(extInput2)
    # --------- End of Extrude 2 ------------- #

    # --------- Plane Creation ------------- #
    # Get the profile again since the sketch has been edit.
    prof1 = sketch1.profiles.item(0)
    
    # Get construction planes
    planes = subComp1.constructionPlanes

    # Create construction plane input
    planeInput = planes.createInput()

    # Add construction plane by offset
    offsetValue = adsk.core.ValueInput.createByReal(depth + 0.1)
    planeInput.setByOffset(prof1, offsetValue)
    planeOne = planes.add(planeInput)
    # --------- End of Plane Creation ------------- #

    # --------- sketch 2 (doors) ------------- #
    # Create a new sketch on the XY plane
    sketches2 = subComp1.sketches
    doorPlane = planes.item(0)
    sketch2 = sketches2.add(doorPlane)

    # Draw right profile
    sketch2.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create((width / 2), height, 0)
    )

    # Draw left profile
    sketch2.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(width, 0, 0),
        adsk.core.Point3D.create((width / 2), height, 0)
    )
    # --------- End of sketch 3 ------------- #

    # --------- Extrude 3 (doors) -------------#
    # Get the profile of the first sketch
    prof3 = sketch2.profiles.item(0)
    prof4 = sketch2.profiles.item(1)

    # Create an extrusion input
    extrudes3 = subComp1.features.extrudeFeatures
    extrudes4 = subComp1.features.extrudeFeatures
    extInput3 = extrudes3.createInput(prof3, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput4 = extrudes4.createInput(prof4, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    # Get the distance from the input
    distance3 = adsk.core.ValueInput.createByReal(1.5)
    extent_distance3 = adsk.fusion.DistanceExtentDefinition.create(distance3)

    # Set the distance extent
    extInput3.setOneSideExtent(extent_distance3, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    extInput4.setOneSideExtent(extent_distance3, adsk.fusion.ExtentDirections.PositiveExtentDirection)

    # Set the extrude type to be solid
    extInput3.isSolid = True
    extInput4.isSolid = True
    
    # Create the extrusion
    ext3 = extrudes3.add(extInput3)
    ext4 = extrudes4.add(extInput4)
    # --------- End of Extrude 3 ------------- #

    # --------- Handle insert  ------------- #
    #Get the handle from another design 
    project = app.data.activeProject
    handle = None
    for file in project.rootFolder.dataFiles:
        if file.name == 'Simple Handle':
            handle = file
    
    #Insert handle (the positioning of the handle needs to be done by hand, for now)
    subComp1.occurrences.addByInsert(handle, adsk.core.Matrix3D.create(), True)
    subComp1.occurrences.addByInsert(handle, adsk.core.Matrix3D.create(), True)
    # --------- End of Handle insert  ------------- #


# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []