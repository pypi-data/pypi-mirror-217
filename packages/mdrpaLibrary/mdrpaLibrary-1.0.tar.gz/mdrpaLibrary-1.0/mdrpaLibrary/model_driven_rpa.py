from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class ModelDrivenRpa:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.builtin = BuiltIn()
        self.resource_files = [
            'clickButtonModel.robot',
            'inputFieldModel.robot',
            'selectCheckboxModel.robot',
            'selectFromDropdownModel.robot',
            'getUiModel.robot'
        ]  # Update with the actual resource file names

    def import_resource_file(self, resource_file):
        # Use the BuiltIn library's `Import Resource` keyword to import the specified resource file
        self.builtin.import_resource(resource_file)

    @keyword
    def click_button_model(self, *args):
        self.import_resource_file(self.resource_files[0])  # Import the first resource file
        self.builtin.run_keyword('Click Button Model', *args)

    @keyword
    def input_field_model(self, *args):
        self.import_resource_file(self.resource_files[1])  # Import the second resource file
        self.builtin.run_keyword('Input Field Model', *args)

    @keyword
    def select_checkbox_model(self, *args):
        self.import_resource_file(self.resource_files[2])  # Import the third resource file
        self.builtin.run_keyword('Select Checkbox Model', *args)

    @keyword
    def select_from_dropdown_model(self, *args):
        self.import_resource_file(self.resource_files[3])  # Import the fourth resource file
        self.builtin.run_keyword('Select From Dropdown Model', *args)
    
    @keyword
    def get_ui_models(self, *args):
        self.import_resource_file(self.resource_files[4])  # Import the fifth resource file
        self.builtin.run_keyword('Get UiModels', *args)
