import tornado.ioloop
import tornado.web
import pickle
import os


class X1(tornado.web.RequestHandler):
	def get(self):
		self.render('html_test.html')


class X2(tornado.web.RequestHandler):
	def get(self):
		index=pickle.load(open('/Data/engine_data.p','rb'))
		self.lookup(index,self.get_argument("message"))
	def lookup(self,index,keyword):
		arr=[]
		if keyword in index:
			for ele in index[keyword]:
				self.write("<a href='Data/airports/"+ele+"'>"+ele[:-5]+"</a>")
				self.write("</br>")



	def ranking(arr):
		page=[]
		x={}
		index=pickle.load(open('Data/data_files/page_ranks.p','rb'))
		for ele in arr:
			page.append(index[ele])
		for i in sort(page):
			for j in arr:
				if index[j]==i:
					x[j]=i
		return x

	def sort(page):
    		"""Sort the mutable sequence seq in place and return it."""
    		for i in reversed(range(len(seq))):
        		finished = True
        		for j in range(i):
            			if seq[j] > seq[j + 1]:
                			seq[j], seq[j + 1] = seq[j + 1], seq[j]
                			finished = False
        		if finished:
            			break
    		return seq
		
			



application = tornado.web.Application([
	(r"/",X1),
	(r"/x",X2),
    ])

if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
