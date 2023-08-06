import pytest
import sys
import os
parent_dir = os.path.abspath("../..")
sys.path.insert(0, parent_dir)
from conftest import petrel_version, pythontooltestproject

@pytest.mark.parametrize("petrel_context", [(petrel_version, pythontooltestproject)], indirect=["petrel_context"])
class TestPolylineSet:
    def test_polylineset_template(self, polylineset):
        assert polylineset.template == ''

    def test_polylineset_workflow_enabled(self, polylineset, return_workflow):
        input_var = return_workflow.input["input_object"]
        output_var = return_workflow.output["output_object"]
        wf_result = return_workflow.run({input_var: polylineset})
        unpacked_object = wf_result[output_var]
        assert type(unpacked_object) == type(polylineset)
        assert unpacked_object.petrel_name == polylineset.petrel_name
        assert unpacked_object.path == polylineset.path
        assert unpacked_object.droid == polylineset.droid

    def test_polylineset_clone_no_attributes_no_copy(self, polylineset_no_attributes, delete_workflow):
        try:
            clone = polylineset_no_attributes.clone("Poly2", copy_values=False)
            assert clone.petrel_name == "Poly2"
            assert clone.path == "Input/Geometry/Poly2"
            assert clone.droid != polylineset_no_attributes.droid
            assert polylineset_no_attributes.get_positions(0) == clone.get_positions(0)
            # TODO once we have access to polyline attributes we should confirm clone also has none
            # Currently we have no way to check in the tests if copy-values actually works
        finally:
            obj = delete_workflow.input["object"]
            delete_workflow.run({obj: clone})

    def test_polylineset_clone_no_attributes_copy(self, polylineset_no_attributes, delete_workflow):
        try:
            clone = polylineset_no_attributes.clone("Poly2", copy_values=True)
            assert clone.petrel_name == "Poly2"
            assert clone.path == "Input/Geometry/Poly2"
            assert clone.droid != polylineset_no_attributes.droid
            assert polylineset_no_attributes.get_positions(0) == clone.get_positions(0)
            # TODO once we have access to polyline attributes we should confirm clone also has none
        finally:
            obj = delete_workflow.input["object"]
            delete_workflow.run({obj: clone})

    def test_polylineset_clone_attributes_no_copy(self, polylineset, delete_workflow):
        try:
            clone = polylineset.clone("Polygon_copy_noval", copy_values=False)
            assert clone.petrel_name == "Polygon_copy_noval"
            assert clone.path == "Input/Geometry/Polygon_copy_noval"
            assert clone.droid != polylineset.droid
            assert polylineset.get_positions(0) == clone.get_positions(0)
            ## Lines/points are copied even if copy_values is False
            lines_original = polylineset.polylines
            lines_clone = clone.polylines
            original_list = []
            clone_list = []
            for line in lines_original:
                for point in line.points:
                    original_list.append(point)
            for line in lines_clone:
                for point in line.points:
                    clone_list.append(point)

            assert original_list == clone_list
            
            # TODO once we have access to polyline attributes we should check values are not copied
        finally:
            obj = delete_workflow.input["object"]
            delete_workflow.run({obj: clone})

    def test_polylineset_clone_attributes_copy(self, polylineset, delete_workflow):
        try:
            clone = polylineset.clone("Polygon_copy", copy_values=True)
            assert clone.petrel_name == "Polygon_copy"
            assert clone.path == "Input/Geometry/Polygon_copy"
            assert clone.droid != polylineset.droid
            assert polylineset.get_positions(0) == clone.get_positions(0)

            lines_original = polylineset.polylines
            lines_clone = clone.polylines
            original_list = []
            clone_list = []
            for line in lines_original:
                for point in line.points:
                    original_list.append(point)
            for line in lines_clone:
                for point in line.points:
                    clone_list.append(point)

            assert original_list == clone_list
            # TODO once we have access to polyline attributes we should check values are actually copied
        finally:
            obj = delete_workflow.input["object"]
            delete_workflow.run({obj: clone})