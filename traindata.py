import requests
from datetime import datetime

def get_schedule():
    # API key for CTA check gmail for key
    api_key = '8fceb40bfac243d581d2b5f5318dc127'
    endpoint = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx'
    params = {
        'key': api_key,
        'mapid': 40800,  # Sedgwick station ID
        'outputType': 'json'
    }

    try:
        # Make the API request
        response = requests.get(endpoint, params=params)
        data = response.json()
        
        # Extract relevant information from the response
        if 'ctatt' in data and 'eta' in data['ctatt']:
            sedgwick_trains = data['ctatt']['eta']
            train_data_list = [{"ETA":'0',"Line":'0',"Destination":'0'}]
            # Get information for the next few trains
            for train in sedgwick_trains:
                wait_time = train.get('arrT')
                present_time = train.get('prdt')
                arrival_time = datetime.strptime(wait_time, '%Y-%m-%dT%H:%M:%S')
                current_time = datetime.strptime(present_time, '%Y-%m-%dT%H:%M:%S')
                eta = arrival_time - current_time
                line = train.get('rt')
                destination = train.get('destNm')
                train_data = {"ETA": int((eta.seconds)/60), "Line": line,"Destination":destination}
                train_data_list.append(train_data)
                
            return(train_data_list)
        else:
            print("No data available for Brown Line trains at Sedgwick station.")
            return(101)

    except Exception as e:
        print(f"An error occurred: {e}")
        return(102)

