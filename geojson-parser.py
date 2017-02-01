import json
with open("tweets.json", 'w+') as json_file:
    a = []
    with open("scored_tweets.txt", "r") as text_file:
        json_objects = [json.loads(line) for line in text_file]
    geo_list = [{'type': 'Feature',
                 'geometry': {
                     'type': 'Point',
                     'coordinates': json_object['coordinates'],
                 },
                 'properties': {
                     'text': json_object['text'],
                     'score': json_object['score']
                 }} for json_object in json_objects]
    geo_json = {'type': 'FeatureCollection',
                'features': geo_list}
    json.dump(geo_json, json_file)
