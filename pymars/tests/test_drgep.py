"""Tests for drgep module"""

import sys
import os
import pkg_resources

import pytest
import cantera as ct

from ..drgep import create_drgep_matrix, graph_search_drgep, get_importance_coeffs
from ..drgep import reduce_drgep, run_drgep

def relative_location(file):
	file_path = os.path.join(file)
	return pkg_resources.resource_filename(__name__, file_path)


@pytest.mark.skip(reason='old tests for removed function')
class TestTrimDRGEP:

    ##################
    # Input: The GRI model with a dictionary threshold combo to save 2.  
    # Output: An exclusion list of 51 species
    ##################
    def testGRItrim51(self):

        # Original model
        solution_object = ct.Solution("gri30.cti")

        # Dictionary, retained species, and threshold value to input
        max_dict = {"CH4": 1.0, "N2": .25, "O2": .75}
        threshold_value = .5
        retained_species = []
        done = [False]	

        # Run unit
        exclusion_list = trim_drgep(max_dict, solution_object, threshold_value, retained_species, done)

        expected_list_len = 51

        # Print stuff out
        print(" -- Exclude all but CH4 and O2 -- ")
        print("Exclusion list length: " + str(len(exclusion_list)))
        print(" ")
        print(exclusion_list)

        # Assert list is correct length and doesn't include keepers
        assert len(exclusion_list) == expected_list_len
        assert "CH4" not in exclusion_list
        assert "O2" not in exclusion_list

    ##################
    # Input: The artificial model with a dictionary threshold combo to remove 1.  
    # Output: An exclusion list of 1 species
    ##################
    def testArtTrim1(self):

        # Original model
        path_to_original = relative_location("artificial-mechanism.cti")
        solution_object = ct.Solution(path_to_original)

        # Dictionary, retained species, and threshold value to input
        max_dict = {"H": 1.0, "H2": .2, "O2": 1, "H2O": 1}
        threshold_value = .5
        retained_species = []
        done = [False]	

        # Run unit
        exclusion_list = trim_drgep(max_dict, solution_object, threshold_value, retained_species, done)

        expected_list_len = 1

        # Print stuff out
        print(" -- Exclude only H2 -- ")
        print("Exclusion list length: " + str(len(exclusion_list)))
        print(" ")
        print(exclusion_list)

        # Assert list is correct length and doesn't include keepers
        assert len(exclusion_list) == expected_list_len
        assert "H2" in exclusion_list

    ##################
    # Input: The artificial model with a dictionary threshold combo to remove 2.  
    # Output: An exclusion list of 2 species
    ##################
    def testArtTrim2(self):

        # Original model
        path_to_original = relative_location("artificial-mechanism.cti")
        solution_object = ct.Solution(path_to_original)

        # Dictionary, retained species, and threshold value to input
        max_dict = {"H": 1.0, "H2": .2, "O2": .45, "H2O": 1}
        threshold_value = .5
        retained_species = []
        done = [False]	

        # Run unit
        exclusion_list = trim_drgep(max_dict, solution_object, threshold_value, retained_species, done)

        expected_list_len = 2

        # Print stuff out
        print(" -- Exclude H2 and O2 -- ")
        print("Exclusion list length: " + str(len(exclusion_list)))
        print(" ")
        print(exclusion_list)

        # Assert list is correct length and doesn't include keepers
        assert len(exclusion_list) == expected_list_len
        assert "H2" in exclusion_list
        assert "O2" in exclusion_list

    ##################
    # Input: The artificial model with a dictionary threshold combo to remove 2. 
    #        However, the retianed species list saves one of them from being removed. 
    # Output: An exclusion list of 1 species
    ##################
    def testArtRetain(self):

        # Original model
        path_to_original = relative_location("artificial-mechanism.cti")
        solution_object = ct.Solution(path_to_original)

        # Dictionary, retained species, and threshold value to input
        max_dict = {"H": 1.0, "H2": .2, "O2": .45, "H2O": 1}
        threshold_value = .5
        retained_species = ["O2"]
        done = [False]	

        # Run unit
        exclusion_list = trim_drgep(max_dict, solution_object, threshold_value, retained_species, done)

        expected_list_len = 1

        # Print stuff out
        print(" -- Exclude H2, retain O2 -- ")
        print("Exclusion list length: " + str(len(exclusion_list)))
        print(" ")
        print(exclusion_list)

        # Assert list is correct length and doesn't include keepers
        assert len(exclusion_list) == expected_list_len
        assert "H2" in exclusion_list

    ##################
    # Input: The artificial model with a dictionary threshold combo to remove 4.  
    # Output: An exclusion list of 4 species
    ##################
    def testArtRemoveAll(self):

        # Original model
        path_to_original = relative_location("artificial-mechanism.cti")
        solution_object = ct.Solution(path_to_original)

        # Dictionary, retained species, and threshold value to input
        max_dict = {"H": 0, "H2": 0, "O2": 0, "H2O": 0}
        threshold_value = .1
        retained_species = []
        done = [False]	

        # Run unit
        exclusion_list = trim_drgep(max_dict, solution_object, threshold_value, retained_species, done)

        expected_list_len = 4

        # Print stuff out
        print(" -- Exclude all -- ")
        print("Exclusion list length: " + str(len(exclusion_list)))
        print(" ")
        print(exclusion_list)

        # Assert list is correct length and doesn't include keepers
        assert len(exclusion_list) == expected_list_len
        assert "H2" in exclusion_list
        assert "H2O" in exclusion_list
        assert "H" in exclusion_list
        assert "O2" in exclusion_list

    ##################
    # Input: The artificial model with a dictionary value equal to the threshold.  
    # Output: The species is removed.
    ##################
    def testArtRemoveEqual(self):

        # Original model
        path_to_original = relative_location("artificial-mechanism.cti")
        solution_object = ct.Solution(path_to_original)

        # Dictionary, retained species, and threshold value to input
        max_dict = {"H": 1.0, "H2": .2, "O2": 1, "H2O": 1}
        threshold_value = .2
        retained_species = []
        done = [False]	

        # Run unit
        exclusion_list = trim_drgep(max_dict, solution_object, threshold_value, retained_species, done)

        expected_list_len = 1

        # Print stuff out
        print(" -- OIC == Threshold -- ")
        print("Exclusion list length: " + str(len(exclusion_list)))
        print(" ")
        print(exclusion_list)

        # Assert list is correct length and doesn't include keepers
        assert len(exclusion_list) == expected_list_len
        assert "H2" in exclusion_list

    ##################
    # Input: Dictionary is empty.  
    # Output: Nothing.
    ##################
    def testEmptyDict(self):

        # Original model
        path_to_original = relative_location("artificial-mechanism.cti")
        solution_object = ct.Solution(path_to_original)

        # Dictionary, retained species, and threshold value to input
        max_dict = {}
        threshold_value = .5
        retained_species = ["O2"]
        done = [False]	

        # Run unit
        exclusion_list = trim_drgep(max_dict, solution_object, threshold_value, retained_species, done)

        expected_list_len = 3

        # Print stuff out
        print(" -- Empty Dict -- ")
        print("Exclusion list length: " + str(len(exclusion_list)))
        print(" ")
        print(exclusion_list)

        # Assert list is correct length and doesn't include keepers
        assert len(exclusion_list) == expected_list_len
        assert "H2" in exclusion_list
        assert "H2O" in exclusion_list
        assert "H" in exclusion_list


    ##################
    # Input: Dictionary is mixed types.  
    # Output: Doesn't break, still works.
    ##################
    def testInvalidDict(self):

        # Original model
        path_to_original = relative_location("artificial-mechanism.cti")
        solution_object = ct.Solution(path_to_original)

        # Dictionary, retained species, and threshold value to input
        max_dict = {"LK": False, 3: 7.5, "H2O": True}
        threshold_value = .5
        retained_species = ["O2"]
        done = [False]	

        # Run unit
        exclusion_list = trim_drgep(max_dict, solution_object, threshold_value, retained_species, done)

        expected_list_len = 2

        # Print stuff out
        print(" -- Invalid Input -- ")
        print("Exclusion list length: " + str(len(exclusion_list)))
        print(" ")
        print(exclusion_list)

        # Assert list is correct length and doesn't include keepers
        assert len(exclusion_list) == expected_list_len
        assert "H2" in exclusion_list
        assert "H" in exclusion_list

    ##################
    # Input: Threshold is greater than 1.  
    # Output: Everything is removed.
    ##################
    def testThresholdGreaterThan1(self):

        # Original model
        path_to_original = relative_location("artificial-mechanism.cti")
        solution_object = ct.Solution(path_to_original)

        # Dictionary, retained species, and threshold value to input
        max_dict = {"H": 1.0, "H2": .2, "O2": 1, "H2O": 1}
        threshold_value = 5
        retained_species = []
        done = [False]	

        # Run unit
        exclusion_list = trim_drgep(max_dict, solution_object, threshold_value, retained_species, done)

        expected_list_len = 4

        # Print stuff out
        print(" -- Threshold Greater Than 1 -- ")
        print("Exclusion list length: " + str(len(exclusion_list)))
        print(" ")
        print(exclusion_list)

        # Assert list is correct length and doesn't include keepers
        assert len(exclusion_list) == expected_list_len
        assert "H2" in exclusion_list
        assert "H2O" in exclusion_list
        assert "H" in exclusion_list
        assert "O2" in exclusion_list