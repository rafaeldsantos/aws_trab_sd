from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table

Table.create('video', schema=[HashKey('id')]);
print 'Success'
