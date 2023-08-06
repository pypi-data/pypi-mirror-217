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
        ]  

    def import_resource_file(self, resource_file):
        self.builtin.import_resource(resource_file)

    @keyword
    def click_button_model_keyword(self, *args):
        self.import_resource_file(self.resource_files[0])  
        self.builtin.run_keyword('Click Button Model', *args)

    @keyword
    def input_field_model_keyword(self, *args):
        self.import_resource_file(self.resource_files[1])  
        self.builtin.run_keyword('Input Field Model', *args)

    @keyword
    def select_checkbox_model_keyword(self, *args):
        self.import_resource_file(self.resource_files[2])  
        self.builtin.run_keyword('Select Checkbox Model', *args)

    @keyword
    def select_from_dropdown_model_keyword(self, *args):
        self.import_resource_file(self.resource_files[3])  
        self.builtin.run_keyword('Select Value From Dropdown Model', *args)
    
    @keyword
    def get_ui_models_keyword(self, *args):
        self.import_resource_file(self.resource_files[4]) 
        self.builtin.run_keyword('Get UiModels', *args)
