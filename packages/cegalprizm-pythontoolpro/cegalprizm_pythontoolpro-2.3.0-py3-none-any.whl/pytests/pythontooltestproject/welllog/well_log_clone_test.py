import pytest
import sys
import os
from cegalprizm.pythontool.welllog import WellLog
parent_dir = os.path.abspath("../..")
sys.path.insert(0, parent_dir)
from conftest import petrel_version, pythontooltestproject

@pytest.mark.parametrize("petrel_context", [(petrel_version, pythontooltestproject)], indirect=["petrel_context"])
class TestWellLogClone:
    def test_well_log_clone_copy_values_False(self, well_log_vs, delete_workflow):
        try:
            clone = well_log_vs.clone(name_of_clone='clone', copy_values=False)
            clone_global_well_log = clone.global_well_log
            assert isinstance(clone, WellLog)
            assert clone.petrel_name == 'clone'
            assert clone.path == 'Input/Wells/Well_Good/Well logs/clone'
            assert clone.template == well_log_vs.template
            assert len(clone.samples) == 0
        finally:
            obj = delete_workflow.input['object']
            delete_workflow.run({obj: clone})
            delete_workflow.run({obj: clone_global_well_log})

    def test_well_log_clone_copy_values_True(self, well_log_vs, delete_workflow):
        try:
            clone = well_log_vs.clone(name_of_clone='clone', copy_values=True)
            clone_global_well_log = clone.global_well_log
            assert clone.petrel_name == 'clone'
            assert clone.path == 'Input/Wells/Well_Good/Well logs/clone'
            assert clone.template == well_log_vs.template
            log_vs_samples = well_log_vs.samples
            log_vs_copy_samples = clone.samples
            for i in range(9300, 10000, 100):
                s = log_vs_samples.at(i)
                s_copy = log_vs_copy_samples.at(i)
                assert s.position == s_copy.position
                assert s.md == s_copy.md
                assert s.twt == s_copy.twt
                assert s.tvd == s_copy.tvd
                assert s.value == s_copy.value
        finally:
            obj = delete_workflow.input['object']
            delete_workflow.run({obj: clone})
            delete_workflow.run({obj: clone_global_well_log})

    def test_well_log_clone_copy_values_False_template(self, well_log_vs, delete_workflow, petrellink):
        new_template = petrellink.templates['Templates/Geophysical templates/S-impedance']
        try:
            clone = well_log_vs.clone(name_of_clone='clone', template=new_template)
            clone_global_well_log = clone.global_well_log
            clone_template = clone.get_template()
            assert clone_template.path == new_template.path
            assert clone_template.droid == new_template.droid
        finally:
            obj = delete_workflow.input['object']
            delete_workflow.run({obj: clone})
            delete_workflow.run({obj: clone_global_well_log})
