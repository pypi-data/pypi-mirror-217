# Copyright 2023 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc
from .observeddata_grpc import ObservedDataSetGrpc
from .wellsurvey_grpc import XyzWellSurveyGrpc, XytvdWellSurveyGrpc, DxdytvdWellSurveyGrpc, MdinclazimWellSurveyGrpc, ExplicitWellSurveyGrpc

from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.ooponly.ip_oop_transition import Tuple2
from cegalprizm.pythontool.grpc import utils as grpc_utils

import numpy as np

import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.borehole_hub import BoreholeHub

class BoreholeGrpc(PetrelObjectGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(BoreholeGrpc, self).__init__('borehole', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content = {}
        self._channel = typing.cast("BoreholeHub", petrel_connection._service_borehole)
        
    def GetCrs(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.Borehole_GetCrs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.Borehole_GetCrs(request)
             
        return response.GetCrs

    def GetAllContinuousLogs(self):
        return self._get_logs(False)

    def GetAllDictionaryLogs(self):
        return self._get_logs(True)
    
    def GetWellDatum(self) -> typing.Tuple[str, float, str]:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        response = self._channel.Borehole_GetWellDatum(request)
        return (response.Name, response.Offset, response.Description)
    
    def SetWellDatum(self, name: str, offset: float, description: str):
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_SetWellDatum_Request(
            Guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type),
            Name = name,
            Offset = offset,
            Description = description,
        )
        self._channel.Borehole_SetWellDatum(request)

    def _get_logs(self, is_discrete):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.GetAllLogs_Request(
            guid = po_guid,
            discrete_logs = is_discrete
        )
        response = self._channel.Borehole_GetAllLogs(request)
        guids = [po_guid.guid for po_guid in response.guids]
        logs = []
        if is_discrete:
            logs = [DiscreteWellLogGrpc(guid, self._plink) for guid in guids]
        else:
            logs = [WellLogGrpc(guid, self._plink) for guid in guids]

        return logs

    def GetLogs(self, global_logs, discrete_global_logs):
        global_guids = [gl._guid for gl in global_logs]
        discrete_global_guids = [gl._guid for gl in discrete_global_logs]
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.GetLogsValues_Request(
            guid = po_guid
        )
        request.global_logs_guids[:] = global_guids # pylint: disable=no-member
        request.discrete_global_logs_guids[:] = discrete_global_guids # pylint: disable=no-member
        response_iterator = self._channel.Borehole_GetLogsValues(request)
        is_first = True
        col = 0
        for log_values in response_iterator:
            v = log_values.values
            if is_first:
                value_matrix = np.empty((len(v), len(global_guids) + len(discrete_global_guids) + 3))
            value_matrix[:, col] = v
            col += 1
            is_first = False

        return value_matrix

        
    def GetElevationTimePosition(self, depths):
        self._plink._opened_test()

        request = petrelinterface_pb2.Borehole_GetElevationTimePosition_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , depths = [v for v in depths]
        )

        response = self._channel.Borehole_GetElevationTimePosition(request)

        return [[x for x in response.x], [y for y in response.y], [z for z in response.z]]

    def GetTvdPosition(self, depths):
        self._plink._opened_test()

        request = petrelinterface_pb2.Borehole_GetTvdPosition_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , depths = [v for v in depths]
        )

        response = self._channel.Borehole_GetTvdPosition(request)
             
        return [[x for x in response.x], [y for y in response.y], [z for z in response.z]]

    def GetObservedDataSets(self) -> typing.List[typing.Optional[ObservedDataSetGrpc]]:
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_GetObservedDataSets_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.Borehole_GetObservedDataSets(request)
        return [ObservedDataSetGrpc(item.guid, self._plink) if item.guid else None for sublist in responses for item in sublist.GetObservedDataSets] 

    def GetNumberOfObservedDataSets(self) -> int:
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_GetNumberOfObservedDataSets_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._channel.Borehole_GetNumberOfObservedDataSets(request)
        return response.GetNumberOfObservedDataSets 

    def GetXyzWellSurveys(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_GetWellSurveys_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.Borehole_GetXyzWellSurveys(request)
        return [XyzWellSurveyGrpc(item.GetWellSurveys.guid, self._plink) for item in responses]

    def GetXytvdWellSurveys(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_GetWellSurveys_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.Borehole_GetXytvdWellSurveys(request)
        return [XytvdWellSurveyGrpc(item.GetWellSurveys.guid, self._plink) for item in responses]

    def GetDxdytvdWellSurveys(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_GetWellSurveys_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.Borehole_GetDxdytvdWellSurveys(request)
        return [DxdytvdWellSurveyGrpc(item.GetWellSurveys.guid, self._plink) for item in responses]

    def GetMdinclazimWellSurveys(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_GetWellSurveys_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.Borehole_GetMdinclazimWellSurveys(request)
        return [MdinclazimWellSurveyGrpc(item.GetWellSurveys.guid, self._plink) for item in responses]

    def GetExplicitWellSurveys(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_GetWellSurveys_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.Borehole_GetExplicitWellSurveys(request)
        return [ExplicitWellSurveyGrpc(item.GetWellSurveys.guid, self._plink) for item in responses]

    def GetNumberOfWellSurveys(self) -> int:
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_GetNumberOfWellSurveys_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._channel.Borehole_GetNumberOfWellSurveys(request)
        return response.GetNumberOfWellSurveys 

    def CheckCompletionsSetExists(self) -> bool:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid)
        response = self._channel.Borehole_CompletionsSetExists(request)
        return response.value
    
    def GetWellHeadCoordinates(self) -> typing.Tuple[float, float]:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        response = self._channel.Borehole_GetWellHeadCoordinates(request)
        return response.x, response.y
    
    def SetWellHeadCoordinates(self, coordinates: typing.Tuple[float, float]) -> bool:
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_SetWellHeadCoordinates_Request(
            Guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type),
            Coordinates = petrelinterface_pb2.Primitives.Double2(x=coordinates[0], y = coordinates[1])
        )
        response = self._channel.Borehole_SetWellHeadCoordinates(request)
        return response.value
    
    def IsLateral(self) -> bool:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        response = self._channel.Borehole_IsLateral(request)
        return response.value
    
    def CreateLateral(self, lateral_name: str) -> "BoreholeGrpc":
        self._plink._opened_test()
        request = petrelinterface_pb2.Borehole_CreateLateral_Request(
            Guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type),
            LateralName = lateral_name
        )
        response = self._channel.Borehole_CreateLateral(request)
        if response.guid:
            return BoreholeGrpc(response.guid, self._plink)
    
    def CreateWellSurvey(self, name: str, well_survey_type: str, tie_in_guid: str = "", tie_in_sub_type: str = "", tie_in_md: float = -9999
                         ) -> typing.Union[XyzWellSurveyGrpc, XytvdWellSurveyGrpc, DxdytvdWellSurveyGrpc, MdinclazimWellSurveyGrpc]:
        self._plink._opened_test()
        if well_survey_type.lower() == "X Y Z survey".lower():
            trajectory_type = petrelinterface_pb2.WellSurveyType.XYZ
        elif well_survey_type.lower() == "X Y TVD survey".lower():
            trajectory_type = petrelinterface_pb2.WellSurveyType.XYTVD
        elif well_survey_type.lower() == "DX DY TVD survey".lower():
            trajectory_type = petrelinterface_pb2.WellSurveyType.DXDYTVD
        elif well_survey_type.lower() == "MD inclination azimuth survey".lower():
            trajectory_type = petrelinterface_pb2.WellSurveyType.MDINCAZI
        else:
            raise ValueError("Invalid well_survey_type: " + well_survey_type + 
                             ". Valid values are: 'X Y Z survey', 'X Y TVD survey', 'DX DY TVD survey', 'MD inclination azimuth survey'.")

        request = petrelinterface_pb2.Borehole_CreateTrajectory_Request(
            Guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type),
            Name = name,
            WellSurveyType = trajectory_type,
            TieInGuid = petrelinterface_pb2.PetrelObjectGuid(guid = tie_in_guid, sub_type = tie_in_sub_type),
            TieInMd = tie_in_md
        )
        response = self._channel.Borehole_CreateTrajectory(request)
        if trajectory_type == petrelinterface_pb2.WellSurveyType.XYZ and response.guid:
            return XyzWellSurveyGrpc(response.guid, self._plink)
        elif trajectory_type == petrelinterface_pb2.WellSurveyType.XYTVD and response.guid:
            return XytvdWellSurveyGrpc(response.guid, self._plink)
        elif trajectory_type == petrelinterface_pb2.WellSurveyType.DXDYTVD and response.guid:
            return DxdytvdWellSurveyGrpc(response.guid, self._plink)
        elif trajectory_type == petrelinterface_pb2.WellSurveyType.MDINCAZI and response.guid:
            return MdinclazimWellSurveyGrpc(response.guid, self._plink)
        
class WellLogGrpc(PetrelObjectGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection", sub_type: str = 'well log'):
        super(WellLogGrpc, self).__init__(sub_type, guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = petrel_connection._service_welllog        

    def GetDisplayUnitSymbol(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.WellLog_DisplayUnitSymbol_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._channel.WellLog_DisplayUnitSymbol(request)
        return response.display_unit_symbol.value

    def GetParentPythonBoreholeObject(self):
        return self._get_parent_python_borehole_object()
        
    def _get_parent_python_borehole_object(self, is_discrete = False):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.WellLog_GetParentPythonBoreholObject_Request(
            guid = po_guid,
            discrete_logs = is_discrete
        )
        response = self._channel.WellLog_GetParentPythonBoreholeObject(request)
        guid = response.guid.guid
        return BoreholeGrpc(guid, self._plink)

    def _get_GlobalWellLog(self, is_discrete):
        self._plink._opened_test()
        request = petrelinterface_pb2.WellLog_GetGlobalWellLog_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type),
            discrete_logs = is_discrete
        )
        response = self._channel.WellLog_GetGlobalWellLog(request)
        guid = response.petrel_object_ref.guid
        if (is_discrete):
            return DiscreteGlobalWellLogGrpc(guid, self._plink)
        return GlobalWellLogGrpc(guid, self._plink)

    def GetGlobalWellLog(self):
        return self._get_GlobalWellLog(is_discrete=False)

    def SetSamples(self, mds, values):
        return self._set_samples(mds, values)

    def _set_samples(self, mds, values, discrete = False):
        self.write_test()
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        if discrete:
            request = petrelinterface_pb2.WellLog_SetSamples_Request(
                guid = po_guid,
                meassured_depths = mds,
                int_values = values,
                is_discrete = discrete
            )
        else:
            request = petrelinterface_pb2.WellLog_SetSamples_Request(
                guid = po_guid,
                meassured_depths = mds,
                values = values,
                is_discrete = discrete
            )

        return self._channel.WellLog_SetSamples(request).result.value

    def Samples(self):
        return self._get_samples()

    def _get_samples(self, discrete = False):
        self._plink._opened_test()
        request = petrelinterface_pb2.WellLog_GetSamples_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        samples = self._channel.WellLog_GetSamples(request).values
        log_samples = []
        for sample in samples:
            value = sample.int_value if discrete else sample.value
            log_samples.append(
                LogSample(
                    Md = sample.md,
                    X = sample.x,
                    Y = sample.y,
                    ZMd = sample.z_md,
                    ZTwt = sample.z_twt,
                    ZTvd = sample.z_tvd,
                    Value = value
                )
            )
        return log_samples

    def _get_sample_values(self, discrete = False):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        samples = self._channel.WellLog_GetSamples(request).values
        sample_values = [0] * len(samples)
        i = 0
        for sample in samples:
            value = sample.int_value if discrete else sample.value 
            sample_values[i] = value
            i += 1

        return sample_values

class DiscreteWellLogGrpc(WellLogGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection", sub_type: str = 'discrete well log'):
        super(DiscreteWellLogGrpc, self).__init__(guid, petrel_connection, sub_type = sub_type)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = petrel_connection._service_welllog
    
    def GetParentPythonBoreholeObject(self):
        return self._get_parent_python_borehole_object(is_discrete = True)
    
    def GetAllDictionaryCodes(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.DiscreteWellLog_GetAllDictionaryCodes_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        values = self._channel.DiscreteWellLog_GetAllDictionaryCodes(request).codes.values
        collection = []
        for pair in values:
            collection.append(Tuple2(Item1 = pair.item1, Item2 = pair.item2))

        return tuple(collection)

    def GetGlobalWellLog(self):
        return self._get_GlobalWellLog(is_discrete=True)

    def Samples(self):
        return self._get_samples(discrete = True)

    def SetSamples(self, mds, values):
        return self._set_samples(mds, values, discrete = True)

class GlobalWellLogGrpc(PetrelObjectGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection", sub_type: str = 'global well log'):
        super(GlobalWellLogGrpc, self).__init__(sub_type, guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = petrel_connection._service_globalwelllog        

    def GetWellLogByBoreholeName(self, borehole_name):
        return self._get_well_log_by_borehole_name_or_guid(borehole_name, is_discrete = False)

    def _get_well_log_by_borehole_name_or_guid(self, borehole_name, is_discrete = False):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        name = petrelinterface_pb2.ProtoString(value = borehole_name)
        request = petrelinterface_pb2.GlobalWellLog_GetWellLogByBoreholeName_Request(
            guid = po_guid,
            borehole_name = name,
            discrete_logs = is_discrete
        )
        response = self._channel.GlobalWellLog_GetWellLogByBoreholeNameOrGuid(request)
        guid = response.guid.guid
        if not guid:
            return None
        if not is_discrete:
            return WellLogGrpc(guid, self._plink)
        else:
            return DiscreteWellLogGrpc(guid, self._plink)

    def GetAllWellLogs(self):
        return self._get_all_well_logs(is_discrete = False)

    def _get_all_well_logs(self, is_discrete = False):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.GlobalWellLog_GetAllLogs_Request(
            guid = po_guid,
            discrete_logs = is_discrete
        )
        response = self._channel.GlobalWellLog_GetAllLogs(request)
        guids = [po_guid.guid for po_guid in response.guids.guids]
        if not is_discrete:
            well_logs = [WellLogGrpc(guid, self._plink) for guid in guids]
        else:
            well_logs = [DiscreteWellLogGrpc(guid, self._plink) for guid in guids]
        return well_logs

    def GetDisplayUnitSymbol(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.GlobalWellLog_DisplayUnitSymbol_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._channel.GlobalWellLog_DisplayUnitSymbol(request)
        return response.display_unit_symbol.value

    def CreateWellLog(self, pyBorehole):
        self._plink._opened_test()

        request = petrelinterface_pb2.GlobalWellLog_CreateWellLog_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , pyBorehole = petrelinterface_pb2.PetrelObjectRef(guid = pyBorehole._petrel_object_link._guid, sub_type = pyBorehole._petrel_object_link._sub_type)
        )

        response = self._channel.GlobalWellLog_CreateWellLog(request)
             
        return grpc_utils.pb_PetrelObjectRef_to_grpcobj(response.CreateWellLog, self._plink) if response.CreateWellLog.guid else None #TODO: Double check

class DiscreteGlobalWellLogGrpc(GlobalWellLogGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection", sub_type: str = 'global discrete well log'):
        super(DiscreteGlobalWellLogGrpc, self).__init__(guid, petrel_connection, sub_type = sub_type)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = petrel_connection._service_globalwelllog       

    def GetAllWellLogs(self):
        return self._get_all_well_logs(is_discrete = True)
        
    def GetWellLogByBoreholeName(self, borehole_name):
        return self._get_well_log_by_borehole_name_or_guid(borehole_name, is_discrete = True)

    def CreateDictionaryWellLog(self, pyBorehole):
        self._plink._opened_test()

        request = petrelinterface_pb2.GlobalWellLog_CreateDictionaryWellLog_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , pyBorehole = petrelinterface_pb2.PetrelObjectRef(guid = pyBorehole._petrel_object_link._guid, sub_type = pyBorehole._petrel_object_link._sub_type)
        )

        response = self._channel.GlobalWellLog_CreateDictionaryWellLog(request)
             
        return grpc_utils.pb_PetrelObjectRef_to_grpcobj(response.CreateDictionaryWellLog, self._plink) if response.CreateDictionaryWellLog.guid else None #TODO: Double check
    



class LogSample:
    def __init__(self, Md = 0.0, X = 0.0, Y = 0.0, ZMd = 0.0, ZTwt = 0.0, ZTvd = 0.0, Value = 0.0):
        self.Md = Md
        self.X = X
        self.Y = Y
        self.ZMd = ZMd
        self.ZTwt = ZTwt
        self.ZTvd = ZTvd
        self.Value = Value