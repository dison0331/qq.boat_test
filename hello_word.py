import requests
import json

with open('query.txt', 'r') as file:
    query = file.read().strip()

def main():
        
    url = "https://qianfan.baidubce.com/v2/app/conversation/runs"
    
    payload = json.dumps({
        "app_id": "6d86a6ee-4f1d-4b60-b96c-327ce22b4b7c",
        "query": query,
        "conversation_id": "22033d9a-f0f2-4512-af0b-80585dd502d5",
        "stream": False
    }, ensure_ascii=False)
    headers = {
        'Content-Type': 'application/json',
        'X-Appbuilder-Authorization': 'Bearer bce-v3/ALTAK-ozMSELKF93HkpPMRGxG2t/f66d2d77f4f669ea57377e016b136fe1fdd03c8c'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    
    print(response.text)
    

if __name__ == '__main__':
    main()
