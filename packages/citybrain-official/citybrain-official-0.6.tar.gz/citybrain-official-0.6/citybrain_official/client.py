import requests
import json
import os
import pandas

__DEFAULT_ENDPOINT = "https://dev.citybrain.org/api/getData"
__DEFAULT_ODPS_DATA_ADDRESS = "170DD61338021000"

endpoint: str = ""

def __get_endpoint() -> str:
    if endpoint != "":
        return endpoint
    envEndpoint = os.getenv('ENDPOINT')
    if envEndpoint is not None and envEndpoint != "":
        return envEndpoint
    return __DEFAULT_ENDPOINT


def __get_odps_dataaddress(dataAddress: str) -> str:
    if dataAddress != "":
        return dataAddress
    envODPSDataAddress = os.getenv('ODPS_DATA_ADDRESS')
    if envODPSDataAddress is not None and envODPSDataAddress != "":
        return envODPSDataAddress
    return __DEFAULT_ODPS_DATA_ADDRESS

def retrieve_raw(dataAddress: str, sql: str) -> any:
    if sql is None or sql == '':
        return __download_csv(dataAddress=dataAddress)
    else:
        # create odps sql task
        taskID = createSQLTask(dataAddress=dataAddress, sql=sql)

        # query task status until terminated
        status = queryTaskStatus(dataAddress=dataAddress, taskID=taskID)
        while status != 'Terminated':
            status = queryTaskStatus(dataAddress=dataAddress, taskID=taskID)

        # download task result
        return __download_task_result(dataAddress=dataAddress, taskID=taskID)

def retrieve_df(dataAddress: str, sql: str) -> pandas.DataFrame:
    if sql is None or sql == '':
        csvData = __download_csv(dataAddress=dataAddress)
        return __parse_list_to_dataframe(csvData)
    else:
        # create odps sql task
        taskID = createSQLTask(dataAddress=dataAddress, sql=sql)

        # query task status until terminated
        status = queryTaskStatus(dataAddress=dataAddress, taskID=taskID)
        while status != 'Terminated':
            status = queryTaskStatus(dataAddress=dataAddress, taskID=taskID)

        # download task result
        result = __download_task_result(dataAddress=dataAddress, taskID=taskID)
        return __parse_list_to_dataframe(result)
    
def __download_csv(dataAddress: str) -> list[str]:
    endpoint = __get_endpoint()
    reqBody = {'dpAddress': dataAddress, 'payload': ''}
    resp = requests.post(url=endpoint, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    if isinstance(result['data'], str):
        return result['data'].split('\n')

def __parse_list_to_dataframe(rows: list[str]) -> pandas.DataFrame:
    if len(rows) == 0:
        return pandas.DataFrame([])
    src = []
    for row in rows[1:]:
        src.append(row.split(';'))
    return pandas.DataFrame(src, columns=rows[0].split(';'))
	
def __download_task_result(dataAddress: str, taskID: str) -> list[str]:
    endpoint = __get_endpoint()
    reqBody = {"dpAddress": dataAddress, 'payload': json.dumps({'payload': taskID, 'action': 'TASK_DownloadResult'})}
    resp = requests.post(url=endpoint, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    strList = json.loads(result['data'])
    return strList


def queryTaskStatus(dataAddress: str, taskID: str) -> str:
    endpoint = __get_endpoint()
    reqBody = {"dpAddress": dataAddress, 'payload': json.dumps({'payload': taskID, 'action': 'TASK_QueryStatus'})}
    resp = requests.post(url=endpoint, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    return result['data']


def createSQLTask(dataAddress: str, sql: str) -> str:
    endpoint = __get_endpoint()
    dataAddress = __get_odps_dataaddress(dataAddress=dataAddress)
    reqBody = {'dpAddress': dataAddress,'payload': json.dumps({'payload': sql, 'action':'TASK_Create'})}
    resp = requests.post(url=endpoint, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    return result['data']
