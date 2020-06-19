from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import urllib3
from copy import deepcopy
urllib3.disable_warnings()

HOST = '##############'
YOUR_ACCESS_KEY = '########'
YOUR_SECRET_KEY = '########'

REGION = 'us-east-1'
awsauth = AWS4Auth(YOUR_ACCESS_KEY, YOUR_SECRET_KEY, REGION, 'es')

es = Elasticsearch(
    hosts=[{'host': HOST, 'port': '###'}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=False,
    connection_class=RequestsHttpConnection
)
print(es.info())

app = Flask(__name__)


@app.route('/api/v1/models/', methods=['GET'])
def models():
    res = es.search(index="models", body={
        "size":"0",
        "aggs" : {
            "models" : {
                "terms" : {
                    "field" : "model_id.keyword",
                    "size": 100
                },
            }
        }
    })
    
    return jsonify(res['aggregations']['models']['buckets'])

@app.route('/api/v1/brands/', methods=['GET'])
def brands():
    query_body = {
        "size":"0",
        "aggs" : {
            "brands" : {
                "terms" : {
                    "field" : "brand.keyword",
                    "size": 100
                }
            }
        }
    }

    res = es.search(index="models", body=query_body)
    return jsonify(res['aggregations']['brands']['buckets'])

@app.route('/api/v1/brandmodel/', methods=['POST'])
def brandModel():
    req = request.get_json()
    brandList = ''

    for brand in req['brands']:
        brandList += brand + ' '

    query_body = {
        "query": {
            "match": {
            "brand": brandList
            }
        }
    }

    res = es.search(index="models", body=query_body)
    return jsonify(res['hits']['hits'])


@app.route('/api/v1/reviews/', methods=['POST'])
def reviews():
    req = request.get_json()
    
    model_id = ''
    for model in req['models']:
        model_id += model + ' '

    frompage = req['frompage']

    query_body = {
        "sort": {"date" : "desc"},
        "from": frompage,
        "size": 10,
        "query": {
            "match" : {
                "model_id" : model_id
            }
        }
    }
    res = es.search(index="reviews", body=query_body)
    return jsonify(res['hits'])


@app.route('/api/v1/ratings/', methods=['POST'])
def ratings():
    req = request.get_json()

    results = []
    for model_id in req['models']:
        query_body = {
            "size": 0,
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "model_id": model_id 
                        }
                    },
                "filter": [{
                    "range": {
                        "date": {"gte": "2018-01-01"}
                    }
                }]      
                }
            },
            "aggs": {
                "ratings": {
                    "date_histogram": {
                        "field": "date",
                            "interval": "month"
                        },
                "aggs": {
                    "rating_score": {
                        "avg": {
                            "field": "rating"
                        }
                    }
                }
                }
            }
        }

        res = es.search(index="reviews", body=query_body)
        results.append({model_id: res['aggregations']['ratings']['buckets']})

    dates = []
    for y in range(2018, 2020):
        for m in range(1, 13):
            if 1 <= m <= 9:
                m = '0{}'.format(m)
            dates.append('{}-{}'.format(y, m))

    init_dict = {}
    for date in dates:
        init_dict[date] = [{
            "ratings_sum": 0.0000001,
            "review_count": 0.0000001,
            "average": 0,
        }]

    result_dict = {}
    for dic in results:
        k = list(dic.keys())[0]
        tmp_dict = deepcopy(init_dict)

        for v in dic[k]:
            tmp_key = v['key_as_string'][:7]
            tmp_dict[tmp_key] = []

            if not v['rating_score']['value']:
                rating_sum = 0.0000001
            else:
                rating_sum = int(v['doc_count'] * v['rating_score']['value'])

            tmp_dict[tmp_key].append({
                "rating_sum": rating_sum,
                "review_count": v['doc_count'],
                "average": v['rating_score']['value']
            })
        result_dict[k] = tmp_dict
    
    return jsonify(result_dict)



@app.route('/api/v1/sentiments/', methods=['POST'])
def sentiments():
    req = request.get_json()
    
    sentiment_result = []
    idx = 0
    for model_id in req['models']:
        query_body = {
        "size": 0,
        "aggs":{
            "group_by_model_id": {
            "terms": {
                "field": "model_id.keyword",
                "size": 12
            },
            "aggs": {
                "group_by_sentiment": {
                "range": {
                    "field": "sentiment",
                    "ranges": [
                    {
                        "from": -1,
                        "to": 0
                    },
                    {
                        "from": 1
                    }
                    ]
                }
                }
            }
            }
        }
        }

        res = es.search(index="reviews_new2", body=query_body)
        senti_count_info = res['aggregations']['group_by_model_id']['buckets'][idx]
        negative_count = senti_count_info['group_by_sentiment']['buckets'][0]['doc_count']
        positive_count = senti_count_info['group_by_sentiment']['buckets'][1]['doc_count']
        sentiment_result.append({model_id: [positive_count, negative_count]})
        idx += 1

    return jsonify(sentiment_result)

@app.route('/api/v1/num_rating/', methods=['POST'])
def num_rating():
    req = request.get_json()
    
    results_dict = {}
    for model_id in req['models']:
        query_body = {
            "size": 0,
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "model_id": model_id
                        }
                    }
                }
            },
            "aggs" : {
                "ratings" : {
                    "terms" : {
                        "field" : "rating",  "size" : 10000
                    }
                }
            }
        }

        res = es.search(index="reviews_new2", body=query_body)

        tmp_dict = {}
        for one_dict in res['aggregations']['ratings']['buckets']:
            tmp_dict[int(one_dict['key'])] = one_dict['doc_count']
        
        tmp_list = []
        for i in range(1, 6):
            tmp_list.append(tmp_dict[i])

        results_dict[model_id] = tmp_list

    return jsonify(results_dict)


app.run(port=5000, debug=True)