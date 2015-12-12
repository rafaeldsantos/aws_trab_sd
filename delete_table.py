from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
table = Table('video')

table.delete()
