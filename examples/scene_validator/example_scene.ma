//Maya ASCII 2023 scene
//Name: example_scene.ma
//Last modified: Thu Jun 20 2025
//Codeset: UTF-8
requires maya "2023";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2023";
fileInfo "version" "2023";
fileInfo "cutIdentifier" "202211180446-193bacfe3e";
fileInfo "osv" "Windows 10 Pro 2009 (Build: 19045)";
fileInfo "UUID" "21EC2020-3AEA-4069-A2DD-08002B30309D";
createNode transform -s -n "persp";
	attribute -e -keyable off ".v" persp;
	attribute -e -keyable off ".tx" persp;
	attribute -e -keyable off ".ty" persp;
	attribute -e -keyable off ".tz" persp;
	attribute -e -keyable off ".rx" persp;
	attribute -e -keyable off ".ry" persp;
	attribute -e -keyable off ".rz" persp;
	attribute -e -keyable off ".sx" persp;
	attribute -e -keyable off ".sy" persp;
	attribute -e -keyable off ".sz" persp;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v";
	setAttr ".fl" 34.999999999999993;
	setAttr ".fcp" 10000;
	setAttr ".fd" 40;
	setAttr ".coi" 10.392304845413265;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "21EC2020-3AEA-1234-A2DD-08002B30309D";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
	setAttr ".rp" -type "double3" 0 0 0 ;
	setAttr ".rpt" -type "double3" 0 0 0 ;

// This is a sample Maya ASCII file, truncated for demonstration purposes
