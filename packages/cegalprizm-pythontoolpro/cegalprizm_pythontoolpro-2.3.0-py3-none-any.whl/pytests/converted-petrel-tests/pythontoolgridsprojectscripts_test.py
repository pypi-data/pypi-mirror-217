# Copyright 2023 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import io
import os
import sys
import pytest
parent_dir = os.path.abspath("..")
sys.path.insert(0, parent_dir)
from conftest import petrel_version, pythontoolgridsproject

@pytest.mark.parametrize("petrel_context", [(petrel_version, pythontoolgridsproject)], indirect=['petrel_context'])
class Testpythontoolgridsproject:

    
    def test_GrpcConnection(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        
        try:
            a = petrellink.ping()
            b = petrellink.ping()
            print(b-a)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\grpc_connection_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_CoordsExtent(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        var = petrellink._get_grid('Models/New model/RH-111-Ti')
        var.readonly = True
        try:
            def approx_equal(a, b):
                return abs(a - b) < 0.000001
            
            ok = True
            xtnt = var.coords_extent
            if not approx_equal(xtnt.x_axis.min, 0.0):
                ok = False
            if not approx_equal(xtnt.x_axis.max, 500.0):
                ok = False
            if not approx_equal(xtnt.y_axis.min, 0.0):
                ok = False
            if not approx_equal(xtnt.y_axis.max, 500.0):
                ok = False
            if not approx_equal(xtnt.z_axis.min, -500.0):
                ok = False
            if not approx_equal(xtnt.z_axis.max, 0.0):
                ok = False
            
            print(ok)
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\coords_extent_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunk1(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-115-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-115-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk_vals = chunk.as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in chunk_vals])
                if irange is None: irange = (0, prop.grid.extent.i - 1)
                if jrange is None: jrange = (0, prop.grid.extent.j - 1)
                if krange is None: krange = (0, prop.grid.extent.k - 1)
                for i in range(irange[0] , irange[1] + 1):
                    for j in range(jrange[0], jrange[1] + 1):
                        for k in range(krange[0], krange[1] + 1):
                            #print(" checking value",i, j, k)
                            if not check_value_matches(chunk_vals[i - irange[0], j - jrange[0], k - krange[0]], i, j, k):
                                raise Exception("value doesn't match for inputs ", irange, jrange, krange)
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = prop.grid.extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            check_all_possible_chunks()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_1_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunk2(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-155-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-155-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk_vals = chunk.as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in chunk_vals])
                if irange is None: irange = (0, prop.grid.extent.i - 1)
                if jrange is None: jrange = (0, prop.grid.extent.j - 1)
                if krange is None: krange = (0, prop.grid.extent.k - 1)
                for i in range(irange[0] , irange[1] + 1):
                    for j in range(jrange[0], jrange[1] + 1):
                        for k in range(krange[0], krange[1] + 1):
                            #print(" checking value",i, j, k)
                            if not check_value_matches(chunk_vals[i - irange[0], j - jrange[0], k - krange[0]], i, j, k):
                                raise Exception("value doesn't match for inputs ", irange, jrange, krange)
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = prop.grid.extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            check_all_possible_chunks()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_2_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunk3(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-515-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-515-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk_vals = chunk.as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in chunk_vals])
                if irange is None: irange = (0, prop.grid.extent.i - 1)
                if jrange is None: jrange = (0, prop.grid.extent.j - 1)
                if krange is None: krange = (0, prop.grid.extent.k - 1)
                for i in range(irange[0] , irange[1] + 1):
                    for j in range(jrange[0], jrange[1] + 1):
                        for k in range(krange[0], krange[1] + 1):
                            #print(" checking value",i, j, k)
                            if not check_value_matches(chunk_vals[i - irange[0], j - jrange[0], k - krange[0]], i, j, k):
                                raise Exception("value doesn't match for inputs ", irange, jrange, krange)
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = prop.grid.extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            check_all_possible_chunks()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_3_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunk4(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-555-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-555-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk_vals = chunk.as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in chunk_vals])
                if irange is None: irange = (0, prop.grid.extent.i - 1)
                if jrange is None: jrange = (0, prop.grid.extent.j - 1)
                if krange is None: krange = (0, prop.grid.extent.k - 1)
                for i in range(irange[0] , irange[1] + 1):
                    for j in range(jrange[0], jrange[1] + 1):
                        for k in range(krange[0], krange[1] + 1):
                            #print(" checking value",i, j, k)
                            if not check_value_matches(chunk_vals[i - irange[0], j - jrange[0], k - krange[0]], i, j, k):
                                raise Exception("value doesn't match for inputs ", irange, jrange, krange)
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = prop.grid.extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            check_all_possible_chunks()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_4_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunk5(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-111-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-111-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk_vals = chunk.as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in chunk_vals])
                if irange is None: irange = (0, prop.grid.extent.i - 1)
                if jrange is None: jrange = (0, prop.grid.extent.j - 1)
                if krange is None: krange = (0, prop.grid.extent.k - 1)
                for i in range(irange[0] , irange[1] + 1):
                    for j in range(jrange[0], jrange[1] + 1):
                        for k in range(krange[0], krange[1] + 1):
                            #print(" checking value",i, j, k)
                            if not check_value_matches(chunk_vals[i - irange[0], j - jrange[0], k - krange[0]], i, j, k):
                                raise Exception("value doesn't match for inputs ", irange, jrange, krange)
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = prop.grid.extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            check_all_possible_chunks()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_5_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunk6(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-151-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-151-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk_vals = chunk.as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in chunk_vals])
                if irange is None: irange = (0, prop.grid.extent.i - 1)
                if jrange is None: jrange = (0, prop.grid.extent.j - 1)
                if krange is None: krange = (0, prop.grid.extent.k - 1)
                for i in range(irange[0] , irange[1] + 1):
                    for j in range(jrange[0], jrange[1] + 1):
                        for k in range(krange[0], krange[1] + 1):
                            #print(" checking value",i, j, k)
                            if not check_value_matches(chunk_vals[i - irange[0], j - jrange[0], k - krange[0]], i, j, k):
                                raise Exception("value doesn't match for inputs ", irange, jrange, krange)
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = prop.grid.extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            check_all_possible_chunks()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_6_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunk7(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-511-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-511-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk_vals = chunk.as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in chunk_vals])
                if irange is None: irange = (0, prop.grid.extent.i - 1)
                if jrange is None: jrange = (0, prop.grid.extent.j - 1)
                if krange is None: krange = (0, prop.grid.extent.k - 1)
                for i in range(irange[0] , irange[1] + 1):
                    for j in range(jrange[0], jrange[1] + 1):
                        for k in range(krange[0], krange[1] + 1):
                            #print(" checking value",i, j, k)
                            if not check_value_matches(chunk_vals[i - irange[0], j - jrange[0], k - krange[0]], i, j, k):
                                raise Exception("value doesn't match for inputs ", irange, jrange, krange)
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = prop.grid.extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            check_all_possible_chunks()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_7_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunk8(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-551-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-551-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk_vals = chunk.as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in chunk_vals])
                if irange is None: irange = (0, prop.grid.extent.i - 1)
                if jrange is None: jrange = (0, prop.grid.extent.j - 1)
                if krange is None: krange = (0, prop.grid.extent.k - 1)
                for i in range(irange[0] , irange[1] + 1):
                    for j in range(jrange[0], jrange[1] + 1):
                        for k in range(krange[0], krange[1] + 1):
                            #print(" checking value",i, j, k)
                            if not check_value_matches(chunk_vals[i - irange[0], j - jrange[0], k - krange[0]], i, j, k):
                                raise Exception("value doesn't match for inputs ", irange, jrange, krange)
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = prop.grid.extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None]  + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            check_all_possible_chunks()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_8_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunkSet1(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-115-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-115-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            parent_extent = prop.grid.extent
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            
            def reset_prop():
                prop.all().set(0)
                for (_, _, _, val) in prop.all().enumerate():
                    if val != 0.0:
                        raise Exception("resetting failed?")
            
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                # set all prop values to 0
                reset_prop()
            
                # set a chunk value to 1
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk.set(1)
            
                all_vals = input_prop.all().as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in all_vals])
            
                # check all the values in the prop to see if the chunk set has set only the correct values
                if irange is None: irange = (0, parent_extent.i - 1)
                if jrange is None: jrange = (0, parent_extent.j - 1)
                if krange is None: krange = (0, parent_extent.k - 1)
            
                ilist = list(range(irange[0], irange[1] + 1))
                jlist = list(range(jrange[0], jrange[1] + 1))
                klist = list(range(krange[0], krange[1] + 1))
            
                for i in range(0, parent_extent.i):
                    for j in range(0, parent_extent.j):
                        for k in range(0, parent_extent.k):
            
                            if i not in ilist or j not in jlist or k not in klist:
                                if all_vals[i, j, k] != 0:
                                    raise Exception("chunk set value outside of chunk")
                            else:
                                if all_vals[i, j, k] != 1:
                                    raise Exception("chunk set didn't work")
            
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = parent_extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            
            initial_vals = prop.all().as_array()
            
            check_all_possible_chunks()
            
            prop.all().set(initial_vals)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_1_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunkSet2(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-155-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-155-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            parent_extent = prop.grid.extent
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            
            def reset_prop():
                prop.all().set(0)
                for (_, _, _, val) in prop.all().enumerate():
                    if val != 0.0:
                        raise Exception("resetting failed?")
            
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                # set all prop values to 0
                reset_prop()
            
                # set a chunk value to 1
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk.set(1)
            
                all_vals = input_prop.all().as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in all_vals])
            
                # check all the values in the prop to see if the chunk set has set only the correct values
                if irange is None: irange = (0, parent_extent.i - 1)
                if jrange is None: jrange = (0, parent_extent.j - 1)
                if krange is None: krange = (0, parent_extent.k - 1)
            
                ilist = list(range(irange[0], irange[1] + 1))
                jlist = list(range(jrange[0], jrange[1] + 1))
                klist = list(range(krange[0], krange[1] + 1))
            
                for i in range(0, parent_extent.i):
                    for j in range(0, parent_extent.j):
                        for k in range(0, parent_extent.k):
            
                            if i not in ilist or j not in jlist or k not in klist:
                                if all_vals[i, j, k] != 0:
                                    raise Exception("chunk set value outside of chunk")
                            else:
                                if all_vals[i, j, k] != 1:
                                    raise Exception("chunk set didn't work")
            
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = parent_extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            
            initial_vals = prop.all().as_array()
            
            check_all_possible_chunks()
            
            prop.all().set(initial_vals)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_2_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunkSet3(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-515-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-515-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            parent_extent = prop.grid.extent
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            
            def reset_prop():
                prop.all().set(0)
                for (_, _, _, val) in prop.all().enumerate():
                    if val != 0.0:
                        raise Exception("resetting failed?")
            
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                # set all prop values to 0
                reset_prop()
            
                # set a chunk value to 1
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk.set(1)
            
                all_vals = input_prop.all().as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in all_vals])
            
                # check all the values in the prop to see if the chunk set has set only the correct values
                if irange is None: irange = (0, parent_extent.i - 1)
                if jrange is None: jrange = (0, parent_extent.j - 1)
                if krange is None: krange = (0, parent_extent.k - 1)
            
                ilist = list(range(irange[0], irange[1] + 1))
                jlist = list(range(jrange[0], jrange[1] + 1))
                klist = list(range(krange[0], krange[1] + 1))
            
                for i in range(0, parent_extent.i):
                    for j in range(0, parent_extent.j):
                        for k in range(0, parent_extent.k):
            
                            if i not in ilist or j not in jlist or k not in klist:
                                if all_vals[i, j, k] != 0:
                                    raise Exception("chunk set value outside of chunk")
                            else:
                                if all_vals[i, j, k] != 1:
                                    raise Exception("chunk set didn't work")
            
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = parent_extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            
            initial_vals = prop.all().as_array()
            
            check_all_possible_chunks()
            
            prop.all().set(initial_vals)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_3_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunkSet4(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-555-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-555-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            parent_extent = prop.grid.extent
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            
            def reset_prop():
                prop.all().set(0)
                for (_, _, _, val) in prop.all().enumerate():
                    if val != 0.0:
                        raise Exception("resetting failed?")
            
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                # set all prop values to 0
                reset_prop()
            
                # set a chunk value to 1
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk.set(1)
            
                all_vals = input_prop.all().as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in all_vals])
            
                # check all the values in the prop to see if the chunk set has set only the correct values
                if irange is None: irange = (0, parent_extent.i - 1)
                if jrange is None: jrange = (0, parent_extent.j - 1)
                if krange is None: krange = (0, parent_extent.k - 1)
            
                ilist = list(range(irange[0], irange[1] + 1))
                jlist = list(range(jrange[0], jrange[1] + 1))
                klist = list(range(krange[0], krange[1] + 1))
            
                for i in range(0, parent_extent.i):
                    for j in range(0, parent_extent.j):
                        for k in range(0, parent_extent.k):
            
                            if i not in ilist or j not in jlist or k not in klist:
                                if all_vals[i, j, k] != 0:
                                    raise Exception("chunk set value outside of chunk")
                            else:
                                if all_vals[i, j, k] != 1:
                                    raise Exception("chunk set didn't work")
            
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = parent_extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            
            initial_vals = prop.all().as_array()
            
            check_all_possible_chunks()
            
            prop.all().set(initial_vals)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_4_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunkSet5(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-111-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-111-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            parent_extent = prop.grid.extent
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            
            def reset_prop():
                prop.all().set(0)
                for (_, _, _, val) in prop.all().enumerate():
                    if val != 0.0:
                        raise Exception("resetting failed?")
            
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                # set all prop values to 0
                reset_prop()
            
                # set a chunk value to 1
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk.set(1)
            
                all_vals = input_prop.all().as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in all_vals])
            
                # check all the values in the prop to see if the chunk set has set only the correct values
                if irange is None: irange = (0, parent_extent.i - 1)
                if jrange is None: jrange = (0, parent_extent.j - 1)
                if krange is None: krange = (0, parent_extent.k - 1)
            
                ilist = list(range(irange[0], irange[1] + 1))
                jlist = list(range(jrange[0], jrange[1] + 1))
                klist = list(range(krange[0], krange[1] + 1))
            
                for i in range(0, parent_extent.i):
                    for j in range(0, parent_extent.j):
                        for k in range(0, parent_extent.k):
            
                            if i not in ilist or j not in jlist or k not in klist:
                                if all_vals[i, j, k] != 0:
                                    raise Exception("chunk set value outside of chunk")
                            else:
                                if all_vals[i, j, k] != 1:
                                    raise Exception("chunk set didn't work")
            
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = parent_extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            
            initial_vals = prop.all().as_array()
            
            check_all_possible_chunks()
            
            prop.all().set(initial_vals)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_5_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunkSet6(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-151-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-151-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            parent_extent = prop.grid.extent
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            
            def reset_prop():
                prop.all().set(0)
                for (_, _, _, val) in prop.all().enumerate():
                    if val != 0.0:
                        raise Exception("resetting failed?")
            
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                # set all prop values to 0
                reset_prop()
            
                # set a chunk value to 1
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk.set(1)
            
                all_vals = input_prop.all().as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in all_vals])
            
                # check all the values in the prop to see if the chunk set has set only the correct values
                if irange is None: irange = (0, parent_extent.i - 1)
                if jrange is None: jrange = (0, parent_extent.j - 1)
                if krange is None: krange = (0, parent_extent.k - 1)
            
                ilist = list(range(irange[0], irange[1] + 1))
                jlist = list(range(jrange[0], jrange[1] + 1))
                klist = list(range(krange[0], krange[1] + 1))
            
                for i in range(0, parent_extent.i):
                    for j in range(0, parent_extent.j):
                        for k in range(0, parent_extent.k):
            
                            if i not in ilist or j not in jlist or k not in klist:
                                if all_vals[i, j, k] != 0:
                                    raise Exception("chunk set value outside of chunk")
                            else:
                                if all_vals[i, j, k] != 1:
                                    raise Exception("chunk set didn't work")
            
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = parent_extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            
            initial_vals = prop.all().as_array()
            
            check_all_possible_chunks()
            
            prop.all().set(initial_vals)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_6_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunkSet7(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-511-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-511-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            parent_extent = prop.grid.extent
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            
            def reset_prop():
                prop.all().set(0)
                for (_, _, _, val) in prop.all().enumerate():
                    if val != 0.0:
                        raise Exception("resetting failed?")
            
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                # set all prop values to 0
                reset_prop()
            
                # set a chunk value to 1
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk.set(1)
            
                all_vals = input_prop.all().as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in all_vals])
            
                # check all the values in the prop to see if the chunk set has set only the correct values
                if irange is None: irange = (0, parent_extent.i - 1)
                if jrange is None: jrange = (0, parent_extent.j - 1)
                if krange is None: krange = (0, parent_extent.k - 1)
            
                ilist = list(range(irange[0], irange[1] + 1))
                jlist = list(range(jrange[0], jrange[1] + 1))
                klist = list(range(krange[0], krange[1] + 1))
            
                for i in range(0, parent_extent.i):
                    for j in range(0, parent_extent.j):
                        for k in range(0, parent_extent.k):
            
                            if i not in ilist or j not in jlist or k not in klist:
                                if all_vals[i, j, k] != 0:
                                    raise Exception("chunk set value outside of chunk")
                            else:
                                if all_vals[i, j, k] != 1:
                                    raise Exception("chunk set didn't work")
            
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = parent_extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            
            initial_vals = prop.all().as_array()
            
            check_all_possible_chunks()
            
            prop.all().set(initial_vals)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_7_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyChunkSet8(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-551-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-551-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the chunk match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            parent_extent = prop.grid.extent
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            
            def reset_prop():
                prop.all().set(0)
                for (_, _, _, val) in prop.all().enumerate():
                    if val != 0.0:
                        raise Exception("resetting failed?")
            
            
            def check_chunk(irange, jrange, krange):
                #print("Checking " + str(irange) + "  " + str(jrange) + " " + str(krange))
                # set all prop values to 0
                reset_prop()
            
                # set a chunk value to 1
                chunk = input_prop.chunk(irange, jrange, krange)
                chunk.set(1)
            
                all_vals = input_prop.all().as_array()
                #print("size", chunk_vals.GetLength(0), chunk_vals.GetLength(1), chunk_vals.GetLength(2))
                #print([ v for v in all_vals])
            
                # check all the values in the prop to see if the chunk set has set only the correct values
                if irange is None: irange = (0, parent_extent.i - 1)
                if jrange is None: jrange = (0, parent_extent.j - 1)
                if krange is None: krange = (0, parent_extent.k - 1)
            
                ilist = list(range(irange[0], irange[1] + 1))
                jlist = list(range(jrange[0], jrange[1] + 1))
                klist = list(range(krange[0], krange[1] + 1))
            
                for i in range(0, parent_extent.i):
                    for j in range(0, parent_extent.j):
                        for k in range(0, parent_extent.k):
            
                            if i not in ilist or j not in jlist or k not in klist:
                                if all_vals[i, j, k] != 0:
                                    raise Exception("chunk set value outside of chunk")
                            else:
                                if all_vals[i, j, k] != 1:
                                    raise Exception("chunk set didn't work")
            
            
            def check_all_possible_chunks():
                # get a chunk
                # iterate over it
                # check values for each
                extent = parent_extent
                possible_is = [None] + list(range(0, extent.i))
                possible_js = [None] + list(range(0, extent.j))
                possible_ks = [None] + list(range(0, extent.k))
            
                import itertools as it
            
                i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
                j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
                k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]
            
                for irange in i_s:
                    for jrange in j_s:
                        for krange in k_s:
                            check_chunk(irange, jrange, krange)
            
            
            initial_vals = prop.all().as_array()
            
            check_all_possible_chunks()
            
            prop.all().set(initial_vals)
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_chunk_set_8_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices1(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-115-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-115-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_1_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices2(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-155-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-155-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_2_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices3(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-515-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-515-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_3_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices4(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-555-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-555-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_4_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices5(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-111-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-111-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_5_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices6(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-151-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-151-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_6_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices7(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-511-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-511-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_7_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices8(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-551-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-551-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_8_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices9(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-115-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-115-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_9_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices10(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-155-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-155-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_10_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices11(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-515-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-515-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_11_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices12(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-555-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-555-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_12_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices13(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-111-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-111-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_13_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices14(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-151-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-151-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_14_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices15(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-511-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-511-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_15_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyEnumerateValuesMatchVisibleIndices16(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-551-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-551-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : given [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            all_correct = True
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    for (i, j, k, value) in col.enumerate():
                        if not check_value_matches(value, i, j, k):
                             all_correct = False
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                for (i, j, k, value) in layer.enumerate():
                    if not check_value_matches(value, i, j, k):
                        all_correct = False
            
            for (i, j, k, value) in prop.all().enumerate():
                if not check_value_matches(value, i, j, k):
                    all_correct = False
            
            if not all_correct:
                raise Exception("incorrect values")
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_enumerate_values_match_visible_indices_16_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices1(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-115-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-115-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_1_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices2(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-155-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-155-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_2_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices3(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-515-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-515-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_3_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices4(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-555-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-555-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_4_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices5(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-111-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-111-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_5_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices6(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-151-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-151-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_6_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices7(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-511-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-511-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_7_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices8(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-551-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-551-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_8_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices9(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-115-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-115-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_9_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices10(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-155-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-155-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_10_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices11(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-515-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-515-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_11_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices12(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-555-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-555-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_12_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices13(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-111-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-111-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_13_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices14(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-151-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-151-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_14_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices15(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-511-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-511-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_15_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_GridpropertyLayerValuesMatchVisibleIndices16(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-551-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-551-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for k in range(grid.extent.k):
                    layer = prop.layer(k)
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            prop_value = layer.as_array()[i, j]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for k in range(grid.extent.k):
                layer = prop.layer(k)
                with layer.values() as vals:
                    for i in range(grid.extent.i):
                        for j in range(grid.extent.j):
                            vals[i, j] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\gridproperty_layer_values_match_visible_indices_16_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices1(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-115-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-115-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_1_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices2(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-155-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-155-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_2_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices3(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-515-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-515-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_3_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices4(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-555-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-555-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_4_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices5(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-111-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-111-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_5_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices6(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-151-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-151-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_6_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices7(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-511-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-511-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_7_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices8(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-551-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-551-Ti/Properties/IJK cell value')
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_8_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices9(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-115-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-115-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_9_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices10(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-155-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-155-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_10_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices11(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-515-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-515-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_11_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices12(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/LHInv-555-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/LHInv-555-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_12_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices13(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-111-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-111-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_13_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices14(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-151-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-151-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_14_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices15(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-511-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-511-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_15_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_ValuesMatchVisibleIndices16(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        input_grid = petrellink._get_grid('Models/New model/RH-551-Ti')
        input_grid.readonly = True
        input_prop = petrellink._get_grid_property('Models/New model/RH-551-Ti/Properties/discrete_IJK_cell_value', True)
        input_prop.readonly = False
        try:
            # check that the indices of the grid match the visible indicies
            # by using the visible index property
            grid = input_grid
            prop = input_prop
            
            def check_value_matches(val, i, j, k):
                # value is expected to be i + 10 * k + 100 * k
                # but with i, j, k from 1 instead of 0
                expected = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
                if val != expected:
                    print("%s : internal [%d %d %d] expected %d, visible prop %d" % (grid.petrel_name, i, j, k, expected, val))
                    return False
                return True
            
            def check_all_values():
                all_correct = True
                for i in range(grid.extent.i):
                    for j in range(grid.extent.j):
                        col = prop.column(i, j)
                        for k in range(grid.extent.k):
                            prop_value = col.as_array()[k]
                            if not check_value_matches(prop_value, i, j, k):
                                all_correct = False
            
                if not all_correct:
                    raise Exception("reading indicices not ok")
            
            check_all_values()
            
            for i in range(grid.extent.i):
                for j in range(grid.extent.j):
                    col = prop.column(i, j)
                    with col.values() as vals:
                        for k in range(grid.extent.k):
                            vals[k] = (i + 1) + 10 * (j + 1) + 100 * (k + 1)
            
            check_all_values()
            
            print("Ok")
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\values_match_visible_indices_16_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))




    
    def test_VerticesSmoketest(self, petrellink):
        try_output = io.StringIO()
        sys_out = sys.stdout
        sys.stdout = try_output
        is_oop = True
        var = petrellink._get_grid('Models/New model/Faulted')
        var.readonly = True
        try:
            import math
            
            def check_all_defined(vertices):
                all_good = True
                for v in vertices:
                    if math.isnan(v.x) or math.isnan(v.y) or math.isnan(v.z):
                        all_good = False
                return all_good
            
            def check_all_undefined(vertices):
                all_good = True
                for v in vertices:
                    if not math.isnan(v.x) or not math.isnan(v.y) or not math.isnan(v.z):
                        all_good = False
                return all_good
            
            
            good_all_defined =  check_all_defined(var.vertices(3, 3, 3))
            bad_all_undefined = check_all_undefined(var.vertices_unchecked(2, 11, 0))
            
            bad_checked_raises_error = False
            try:
                var.vertices(2, 11, 0)
            except ValueError:
                bad_checked_raises_error = True
            
            print(str(good_all_defined)+str(bad_checked_raises_error)+str(bad_all_undefined))
            
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        with open(r'..\..\Blueback.PythonTool.PythonApi.PetrelTest\Resources\ValidatedScripts\txt\vertices_smoketest_expected.txt', 'r') as f:
            expected_output =  f.read().strip()
        try_output.seek(0)
        actual_output = try_output.read().strip()
        sys.stdout = sys_out
        print('')
        print('##### expected_output:')
        print(expected_output)
        print('##### actual_output:')
        print(actual_output)
        assert ''.join(expected_output.split()) in ''.join(actual_output.split()), "\nexpected:\n%s\n\nactual:\n%s\n\n" %(''.join(expected_output.split()), ''.join(actual_output.split()))

