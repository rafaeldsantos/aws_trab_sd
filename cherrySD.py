#   Universidade Federal de Sao Carlos - Campus Sorocaba
#   Trabalho de Sistemas Distribuidos
#   Nome Rafael Danilo dos Santos
#   Nome Mateus Gomes Barbieri

#webservice
import cherrypy
from cherrypy.lib import static

#template
from jinja2 import Environment, FileSystemLoader

#aws
import boto
import uuid

#dynamo
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from boto.s3.key import Key

#o. system
import os
import random

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

env = Environment(loader=FileSystemLoader('templates'))

class WebService(object):
    def __init__(self):
        self.s3 = boto.connect_s3()
        self.bucket_name = "sdbucket-f1fc915f-718d-4a55-bc70-74f7276a24eb"
        if(self.s3.lookup(self.bucket_name) == None):
            print "Creating new bucket with name: " + self.bucket_name
            self.bucket = self.s3.create_bucket(self.bucket_name)
        else:
            print "Opening bucket with name: " + self.bucket_name
            self.bucket = self.s3.get_bucket(self.bucket_name)


        self.k = Key(self.bucket)
        self.videos = Table('video')

    def index(self):
        tmpl = env.get_template('index.html')
        result_set = self.videos.scan()
        self.lista = []
        self.keydic = {}
        for item in result_set:
            self.lista.append(item['key'])
            self.keydic[item['key']] = item['id']
            # print '\n\n\n'+item['id']+'\n\n\n'

        return tmpl.render(lista=self.lista)
    index.exposed = True

    def download(self,mydownload):
        self.k.key = mydownload
        DownloadFile = self.k.get_contents_as_string()
        # test = self.videos.get_item(id=str(self.id))
        # test.delete()
        return static.serve_fileobj(DownloadFile,disposition='attachment',content_type=mydownload,name=mydownload)
    download.exposed = True

    def upload(self, myFile,name,description):
        tmpl = env.get_template('upload.html')

        self.upname = myFile.filename
        self.k.key = self.upname

        self.id = random.randint(0, 999999)
        self.videos.put_item(data={'id': str(self.id),'name': name,'description': description,'key':myFile.filename,})

        print "Uploading some data to " + self.bucket_name + " with key: " + self.k.key

        self.k.set_contents_from_file(myFile.file)
        size = 0
        while True:
            data = myFile.file.read(8192)
            if not data:
                break
            size += len(data)

        return tmpl.render(tam=size, filename=myFile.filename, type=myFile.content_type)
    upload.exposed = True

    def description(self,mydownload):
        tmpl = env.get_template('description.html')

        item = self.videos.get_item(id=self.keydic[mydownload] )
        return tmpl.render(mydownload=mydownload,id=item['id'],name=item['name'],description=item['description'],filename=item['key'])
    description.exposed = True

    def delete(self,mydelete):
        tmpl = env.get_template('delete.html')
        item = self.videos.get_item(id=self.keydic[mydelete] )
        item.delete()
        self.k.key = mydelete
        self.k.delete()
        return tmpl.render()
    delete.exposed = True




import os.path
myconf = os.path.join(os.path.dirname(__file__), 'local.conf')

if __name__ == '__main__':

    cherrypy.quickstart(WebService(), config=myconf)
else:

    cherrypy.tree.mount(WebService(), config=myconf)
