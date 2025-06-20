#!/usr/bin/env python3
"""
SceneValidator - Validates scene structure and elements against production guidelines.

This tool helps ensure consistency and adherence to project standards by analyzing
scene files and providing detailed reports about compliance with naming conventions,
required elements, and proper structure.

Typical usage:
    python scene_validator.py --input scene.ma --config config.yaml
"""

import os
import sys
import json
import yaml
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("validator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SceneValidator")

class ValidationResult:
    """Class to store and manage validation results."""
    
    def __init__(self, scene_file_path: str):
        """Initialize with the scene file path."""
        self.scene_file_path = scene_file_path
        self.errors = []
        self.warnings = []
        self.validation_time = datetime.now()
        
    def add_error(self, code: str, message: str, location: str = ""):
        """Add an error to the validation result."""
        self.errors.append({
            "code": code,
            "message": message,
            "location": location
        })
        logger.error(f"Error {code}: {message} at {location}")
        
    def add_warning(self, code: str, message: str, location: str = ""):
        """Add a warning to the validation result."""
        self.warnings.append({
            "code": code,
            "message": message,
            "location": location
        })
        logger.warning(f"Warning {code}: {message} at {location}")
        
    def is_valid(self) -> bool:
        """Return True if no errors were found, False otherwise."""
        return len(self.errors) == 0
        
    def summary(self) -> str:
        """Return a text summary of the validation results."""
        status = "PASSED" if self.is_valid() else "FAILED"
        summary = f"Validation {status} for {self.scene_file_path}\n"
        summary += f"Validation Time: {self.validation_time}\n"
        summary += f"Errors: {len(self.errors)}\n"
        summary += f"Warnings: {len(self.warnings)}\n"
        
        if self.errors:
            summary += "\nERRORS:\n"
            for error in self.errors:
                summary += f"  [{error['code']}] {error['message']} at {error['location']}\n"
                
        if self.warnings:
            summary += "\nWARNINGS:\n"
            for warning in self.warnings:
                summary += f"  [{warning['code']}] {warning['message']} at {warning['location']}\n"
                
        return summary
        
    def to_json(self) -> str:
        """Export results as JSON."""
        return json.dumps({
            "scene_file": self.scene_file_path,
            "validation_time": self.validation_time.isoformat(),
            "is_valid": self.is_valid(),
            "errors": self.errors,
            "warnings": self.warnings
        }, indent=2)
        
    def to_html(self) -> str:
        """Export results as HTML report."""
        status_class = "pass" if self.is_valid() else "fail"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Validation Report - {os.path.basename(self.scene_file_path)}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ margin: 20px 0; padding: 10px; background-color: #f5f5f5; border-radius: 5px; }}
                .pass {{ color: green; }}
                .fail {{ color: red; }}
                .errors, .warnings {{ margin: 10px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Validation Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>File: <strong>{self.scene_file_path}</strong></p>
                <p>Status: <span class="{status_class}">{"PASSED" if self.is_valid() else "FAILED"}</span></p>
                <p>Validation Time: {self.validation_time}</p>
                <p>Errors: {len(self.errors)}</p>
                <p>Warnings: {len(self.warnings)}</p>
            </div>
        """
        
        if self.errors:
            html += """
            <div class="errors">
                <h2>Errors</h2>
                <table>
                    <tr>
                        <th>Code</th>
                        <th>Message</th>
                        <th>Location</th>
                    </tr>
            """
            
            for error in self.errors:
                html += f"""
                    <tr>
                        <td>{error['code']}</td>
                        <td>{error['message']}</td>
                        <td>{error['location']}</td>
                    </tr>
                """
            
            html += """
                </table>
            </div>
            """
            
        if self.warnings:
            html += """
            <div class="warnings">
                <h2>Warnings</h2>
                <table>
                    <tr>
                        <th>Code</th>
                        <th>Message</th>
                        <th>Location</th>
                    </tr>
            """
            
            for warning in self.warnings:
                html += f"""
                    <tr>
                        <td>{warning['code']}</td>
                        <td>{warning['message']}</td>
                        <td>{warning['location']}</td>
                    </tr>
                """
            
            html += """
                </table>
            </div>
            """
            
        html += """
        </body>
        </html>
        """
        
        return html


class SceneFile:
    """Class to parse and represent a scene file."""
    
    def __init__(self, file_path: str):
        """Initialize with the file path."""
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1].lower()
        self.elements = []
        self.hierarchy = {}
        self.metadata = {}
        self._parse_file()
        
    def _parse_file(self):
        """Parse the scene file based on its extension."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Scene file not found: {self.file_path}")
            
        logger.info(f"Parsing scene file: {self.file_path}")
        
        # This is a simplified parser for demonstration
        # In a real implementation, you would use specific parsers for each file format
        if self.extension in [".ma", ".mb"]:  # Maya ASCII or Binary
            self._parse_maya_file()
        elif self.extension == ".blend":  # Blender
            self._parse_blender_file()
        elif self.extension in [".c4d"]:  # Cinema 4D
            self._parse_c4d_file()
        else:
            raise ValueError(f"Unsupported file format: {self.extension}")
            
    def _parse_maya_file(self):
        """Parse Maya ASCII/Binary file."""
        # Simplified mock implementation
        # In a real implementation, you would parse the actual file format
        logger.info("Parsing Maya file (mock implementation)")
        
        # Mock data for demonstration
        self.elements = [
            {"name": "camera1", "type": "camera", "path": "root|camera1"},
            {"name": "light1", "type": "lighting", "path": "root|light1"},
            {"name": "environment", "type": "environment", "path": "root|environment"},
            {"name": "asset1", "type": "mesh", "path": "root|asset1"},
        ]
        
        self.hierarchy = {
            "root": {
                "camera1": {},
                "light1": {},
                "environment": {},
                "asset1": {}
            }
        }
        
        self.metadata = {
            "created": "2023-01-01T12:00:00",
            "modified": "2023-06-15T15:30:00",
            "author": "User123",
            "version": "1.0"
        }
        
    def _parse_blender_file(self):
        """Parse Blender file."""
        # Mock implementation
        logger.info("Parsing Blender file (mock implementation)")
        
        # Similar mock data structure as Maya
        self.elements = [
            {"name": "Camera", "type": "camera", "path": "Scene|Camera"},
            {"name": "Light", "type": "lighting", "path": "Scene|Light"},
            {"name": "default_cube", "type": "mesh", "path": "Scene|default_cube"},
        ]
        
        self.hierarchy = {
            "Scene": {
                "Camera": {},
                "Light": {},
                "default_cube": {}
            }
        }
        
        self.metadata = {
            "created": "2023-02-01T10:00:00",
            "modified": "2023-06-10T09:45:00",
            "author": "User456",
            "version": "2.8"
        }
        
    def _parse_c4d_file(self):
        """Parse Cinema 4D file."""
        # Mock implementation
        logger.info("Parsing Cinema 4D file (mock implementation)")
        
        # Similar mock data structure
        self.elements = [
            {"name": "Camera", "type": "camera", "path": "root|Camera"},
            {"name": "Light", "type": "lighting", "path": "root|Light"},
            {"name": "Object", "type": "mesh", "path": "root|Object"},
        ]
        
        self.hierarchy = {
            "root": {
                "Camera": {},
                "Light": {},
                "Object": {}
            }
        }
        
        self.metadata = {
            "created": "2023-03-01T14:00:00",
            "modified": "2023-06-20T11:20:00",
            "author": "User789",
            "version": "R23"
        }
        
    def get_element_names(self) -> List[str]:
        """Return a list of all element names."""
        return [element["name"] for element in self.elements]
        
    def get_elements_by_type(self, element_type: str) -> List[Dict]:
        """Return a list of elements of the specified type."""
        return [element for element in self.elements if element["type"] == element_type]
        
    def has_element(self, element_name: str) -> bool:
        """Check if an element with the given name exists."""
        return any(element["name"] == element_name for element in self.elements)


class SceneValidator:
    """Main class for scene validation."""
    
    def __init__(self, config_path: str):
        """Initialize with a configuration file path."""
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load the configuration from the YAML file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        logger.info(f"Loaded configuration from {self.config_path}")
        return config
        
    def validate(self, scene_file_path: str) -> ValidationResult:
        """Validate a single scene file."""
        logger.info(f"Starting validation of {scene_file_path}")
        
        result = ValidationResult(scene_file_path)
        
        try:
            scene = SceneFile(scene_file_path)
            
            # Validate file format
            if scene.extension not in [".ma", ".mb", ".blend", ".c4d"]:
                result.add_error("E001", f"Unsupported file format: {scene.extension}", scene_file_path)
                return result
                
            # Validate required elements
            self._validate_required_elements(scene, result)
            
            # Validate naming conventions
            self._validate_naming_conventions(scene, result)
            
            # Validate forbidden elements
            self._validate_forbidden_elements(scene, result)
            
            # Validate structure (simplified)
            self._validate_structure(scene, result)
            
        except Exception as e:
            result.add_error("E999", f"Validation error: {str(e)}", scene_file_path)
            logger.exception(f"Validation error for {scene_file_path}")
            
        logger.info(f"Completed validation of {scene_file_path}")
        return result
        
    def batch_validate(self, scene_file_paths: List[str]) -> List[ValidationResult]:
        """Validate multiple scene files."""
        return [self.validate(path) for path in scene_file_paths]
        
    def _validate_required_elements(self, scene: SceneFile, result: ValidationResult):
        """Validate that all required elements are present."""
        required_elements = self.config.get("validation_rules", {}).get("required_elements", [])
        
        for element_type in required_elements:
            elements = scene.get_elements_by_type(element_type)
            if not elements:
                result.add_error(
                    "E002", 
                    f"Missing required element type: {element_type}", 
                    scene.file_path
                )
                
    def _validate_naming_conventions(self, scene: SceneFile, result: ValidationResult):
        """Validate element naming conventions."""
        naming_convention = self.config.get("validation_rules", {}).get("naming_convention", "")
        
        if not naming_convention:
            return
            
        # For this example, we'll use a simple prefix_name_suffix pattern
        # In a real implementation, you would use regex or more sophisticated patterns
        for element in scene.elements:
            name = element["name"]
            
            # Simple check: should have at least one underscore if using prefix_name_suffix pattern
            if naming_convention == "prefix_objectName_suffix" and "_" not in name:
                result.add_error(
                    "E003", 
                    f"Element name '{name}' does not follow naming convention '{naming_convention}'", 
                    element["path"]
                )
                
    def _validate_forbidden_elements(self, scene: SceneFile, result: ValidationResult):
        """Validate that no forbidden elements are present."""
        forbidden_elements = self.config.get("validation_rules", {}).get("forbidden_elements", [])
        
        for forbidden in forbidden_elements:
            if scene.has_element(forbidden):
                result.add_error(
                    "E004", 
                    f"Forbidden element found: {forbidden}", 
                    scene.file_path
                )
                
    def _validate_structure(self, scene: SceneFile, result: ValidationResult):
        """Validate scene structure (simplified)."""
        # This is a simplified validation for demonstration purposes
        # In a real implementation, you would check for specific structure requirements
        
        # Example: Check if the scene has a clean root hierarchy
        if len(scene.hierarchy.keys()) != 1:
            result.add_warning(
                "W001", 
                "Scene does not have a single root node", 
                scene.file_path
            )


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Validate scene files against production guidelines.")
    parser.add_argument("--input", "-i", required=True, help="Path to the scene file to validate")
    parser.add_argument("--config", "-c", required=True, help="Path to the validation configuration file")
    parser.add_argument("--output", "-o", help="Path to save the validation report (optional)")
    parser.add_argument("--format", "-f", choices=["text", "json", "html"], default="text",
                        help="Output format for the validation report (default: text)")
    
    args = parser.parse_args()
    
    try:
        validator = SceneValidator(args.config)
        result = validator.validate(args.input)
        
        # Output result based on format
        if args.format == "json":
            output = result.to_json()
        elif args.format == "html":
            output = result.to_html()
        else:  # text
            output = result.summary()
            
        # Save to file if specified
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Validation report saved to {args.output}")
        else:
            print(output)
            
        # Exit with appropriate status code
        sys.exit(0 if result.is_valid() else 1)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(2)


if __name__ == "__main__":
    main()
