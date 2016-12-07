from databox import Client

client = Client('2cdt4yoytbvockc51cowgs4gsss84ow4s')
client.insert_all([
    {'key': 'sales', 'value': 83000, 'date': '2016-01-19', attributes={
      'channel': 'online',
    }},
    {'key': 'sales', 'value': 4000, 'date': '2016-01-20 16:07:37-06:00', attributes={
      'channel': 'retail',
    }},
])