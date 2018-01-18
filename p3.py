import sys
print sys.version #use when testing

#use the following code to test
#try:
#   #from html.parser import HTMLParser
#   from HTMLParser import HTMLParser
#   import requests,re,os,json
#except:
#   #print("Unexpected error:", sys.exc_info(),file=sys.stderr)
#   print "Unexpected error:", sys.exc_info()
#   raise
   
from HTMLParser import HTMLParser
import requests,re,os,json

class MyHTMLParser(HTMLParser,object):
    def __init__(self):
         super(MyHTMLParser,self).__init__()
         self.flag = False
         self.pl_iter = 0
         self.data_item = ''
         self.section = ''
         self.fin_data = {}; self.fin_data['header'] = {}
         # handle special cases
         self.tseF = False
         self.tseRC = 0
         self.cshF = False
         self.cshRC = 0
         self.depF = False
         self.depRC = 0
         self.stdF = False
         self.stdRC = 0
         self.dfsecF = False

    def handle_starttag(self, tag, attrs):
        global period

        if not self.flag and not self.dfsecF:
            self.data_item = ''

        if tag == 'optionxx':
            #print(attrs,file=sys.stderr)
            for a,v in attrs:
                #print(a,file=sys.stderr)
                if a == 'selected': #in str(a):
                    for suffix in ['income-statement','balance-sheet','cash-flow']:
                        if attrs[0][1].endswith(suffix):
                           #print(tag,suffix)
                           self.section = suffix
                           self.fin_data[self.section] = {}

                           #print(attrs[0][1], file=sys.stderr)
                           #m1 = re.search('(?<=/)(annual|quarter)[.]*',attrs[0][1])
                           #try:
                           #   if m1 is not None:
                           #      print(m1.group(0),file=sys.stderr)
                           #      period = m1.group(0)
                           #except:
                           #   print("Unexpected error:", sys.exc_info(), file=sys.stderr)
                           #   raise
                           #self.fin_data[self.section]['period'] = period
                           break
        elif tag == 'link':
            #print(attrs,file=sys.stderr)
            for a,v in attrs:
                #print(a,file=sys.stderr)
                if a == 'href': #in str(a):
                    for suffix in ['income-statement','balance-sheet','cash-flow']:
                        if v.endswith(suffix):
                           #print(tag,suffix)
                           self.section = suffix
                           if self.section not in self.fin_data:
                               self.fin_data[self.section] = [{}]
                           else:
                               self.fin_data[self.section].append({})

                           #print(v, file=sys.stderr)
                           m1 = re.search('(?<=/)(annual|quarter)[.]*',v)
                           try:
                              if m1 is not None:
                                 #print(m1.group(0),file=sys.stderr)
                                 period = m1.group(0)
                           except:
                              #print("Unexpected error:", sys.exc_info())
                              print >> sys.stderr, "Unexpected error:", sys.exc_info()
                              raise
                         
                           #print(len(self.fin_data[self.section]),file=sys.stderr)
                           self.fin_data[self.section][len(self.fin_data[self.section])-1]['period'] = period
                           break
        elif tag == 'span':
            if self.dfsecF:
               for a,v in attrs:
                   if a == 'class':
                       if v == 'data_lbl':
                          self.data_item = v
            else:
               for a,v in attrs:
                   if a == 'class':
                       if v in ('companyName','tickerName','exchangeName'):
                           try:
                              self.fin_data['header'][v]
                           except KeyError:
                              self.data_item = v
                           else:
                              pass
                   elif a == 'id':
                       if v in ('quote_val'):
                           try:
                              self.fin_data['header'][v]
                           except KeyError:
                              self.data_item = v
                           else:
                              pass
        elif tag == 'ul':
            for a,v in attrs:
                if a == 'class':
                    if v == 'cr_data_collection cr_charts_info':
                        try:
                           self.fin_data['header']['range_52w']
                        except KeyError:
                           self.dfsecF = True
                        else:
                           pass                     
                          
                        
        if self.flag:
            pass
            #print("start tag:", tag)


    def handle_data(self, data):
        if self.dfsecF:
           if self.data_item == 'data_lbl': 
              if data == '52 Week Range':
                 self.data_item = 'range_52w'
           elif data != ' ': 
              if self.data_item == 'range_52w':                           
                 self.fin_data['header'][self.data_item] = data
                 self.dfsecF = False
              
        if self.tseRC == 0:
           m1 = re.search('Total Shareholders[.]*',data)
           try:
              if m1 is not None:
                 if self.tseRC == 0:
                     self.tseF = True
                     self.tseRC += 1 
                     #print(data)
           except:
              #print("Unexpected error:", sys.exc_info())
              print "Unexpected error:", sys.exc_info()
              raise
              
        if self.cshRC == 0:
           m1 = re.search('[.]*Short Term Investments',data)
           try:
              if m1 is not None:
                 if self.cshRC == 0:
                     self.cshF = True
                     self.cshRC += 1 
                     #print(data)
           except:
              #print("Unexpected error:", sys.exc_info())
              print "Unexpected error:", sys.exc_info()
              raise
           
        if self.depRC == 0:
           m1 = re.search('[.]*Amortization Expense',data)
           try:
              if m1 is not None:
                 if self.depRC == 0:
                     self.depF = True
                     self.depRC += 1 
                     #print(data)
           except:
              #print("Unexpected error:", sys.exc_info())
              print "Unexpected error:", sys.exc_info()
              raise
              
        if self.stdRC == 0:
           m1 = re.search('ST Debt[.]*',data)
           try:
              if m1 is not None:
                 if self.stdRC == 0:
                     self.stdF = True
                     self.stdRC += 1 
                     #print(data)
           except:
              #print("Unexpected error:", sys.exc_info())
              print "Unexpected error:", sys.exc_info()
              raise      
                 
        # extract data from financial statements     
        if 'Fiscal year' in data:
            self.flag = True
            self.pl_iter = 6
            #print("data  :", data)
            m = re.search('USD[ a-zA-Z]+',data)
            #self.fin_data[self.section]['Data Unit'] = m.group(0)
            self.fin_data[self.section][len(self.fin_data[self.section])-1]['Data Unit'] = m.group(0)
            self.data_item = 'Year'
        elif self.data_item in ('companyName','tickerName','exchangeName','quote_val'):
            m1 = data.replace('&amp;','&')
            try:
                self.fin_data['header'][self.data_item]
            except KeyError:             
                self.fin_data['header'][self.data_item] = m1
            #except NameError:             
                #print "well, it WASN'T defined after all!"    
            else:           
                self.fin_data['header'][self.data_item] += m1
            #self.data_item = ''
        elif data in ['Sales/Revenue', 'Depreciation & Amortization Expense',\
                'EBIT', 'Interest Expense', 'Pretax Income', 'Income Tax',\
                'EPS (Diluted)', 'Diluted Shares Outstanding', 'EBITDA',\
                'Cash & Short Term Investments','Long-Term Note Receivable',\
                'Intangible Assets','Other Long-Term Investments',\
                'ST Debt & Current Portion LT Debt',\
                'Long-Term Debt',\
                'Total Shareholders\' Equity',\
                'Net Operating Cash Flow','Capital Expenditures','Cash Dividends Paid - Total']\
                  or self.tseF or self.cshF or self.depF or self.stdF:
            self.flag = True
            self.data_item = data
            self.pl_iter = 6 # 6 items : label + 5 data values
            if self.tseF and self.section == 'balance-sheet':      
               m1 = re.search('[.]*Equity',self.data_item)
               try:
                  if m1 is None:
                     #print(data)
                     self.pl_iter += 1 # 7 items : 2 label items + 5 data values
                     self.data_item += '\' Equity'
               except:
                  #print("Unexpected error:", sys.exc_info())
                  print "Unexpected error:", sys.exc_info()
                  raise
               #print(data)
               self.tseF = False
            elif self.stdF and self.section == 'balance-sheet':      
               m1 = re.search('[.]*Current Portion LT Debt',self.data_item)
               try:
                  if m1 is None:
                     #print(data)
                     self.pl_iter += 1
                     self.data_item += '& Current Portion LT Debt'
               except:
                  #print("Unexpected error:", sys.exc_info())
                  print "Unexpected error:", sys.exc_info()
                  raise
               #print(data)
               self.stdF = False
            elif self.cshF and self.section == 'balance-sheet':     
               m1 = re.search('Cash &[.]*',self.data_item)
               try:
                  if m1 is None:
                     #print(data)
                     self.data_item = 'Cash &' + self.data_item
               except:
                  #print("Unexpected error:", sys.exc_info())
                  print "Unexpected error:", sys.exc_info()
                  raise
               #print(data)
               self.cshF = False
            elif self.depF and self.section == 'income-statement':     
               m1 = re.search('Depreciation &[.]*',self.data_item)
               try:
                  if m1 is None:
                     #print(data)
                     self.data_item = 'Depreciation &' + self.data_item
               except:
                  #print("Unexpected error:", sys.exc_info())
                  print "Unexpected error:", sys.exc_info()
                  raise
               #print(data)
               self.depF = False     

        if self.flag:
            if self.pl_iter >= 6: # skip over the label
                self.pl_iter -= 1
                self.fin_data[self.section][len(self.fin_data[self.section])-1][self.data_item] = []
            elif self.pl_iter > 0:
                if data != ' ': # don't decrement pl_iter for space between tags
                    #print("data  :", data,file=sys.stderr)
                    #if self.pl_iter == 4: # select the second column of data
                    if data != '-':
                        self.fin_data[self.section][len(self.fin_data[self.section])-1][self.data_item].append(data)
                        #self.fin_data[self.section][self.data_item] = data
                    else:
                        self.fin_data[self.section][len(self.fin_data[self.section])-1][self.data_item].append('0')
                        #self.fin_data[self.section][self.data_item] = '0'
                    self.pl_iter -= 1
                    if self.pl_iter == 0:
                        self.flag = False

# html parser class definition - end

if len(sys.argv) == 1:
    #print ("Ticker symbol not present")
    print "Ticker symbol not present"
    sys.exit()

ticker = sys.argv[1].upper()
#period = 'annual'
web_data = ''

try:
   parser = MyHTMLParser()
except:
   #print("Unexpected error:", sys.exc_info(),file=sys.stderr)
   print "Unexpected error:", sys.exc_info()
   raise

euid = str(os.geteuid())
#if euid == '10106': #uid on Nexus 9
if euid == '10003': 
    filedir = os.path.expandvars('$HOME/project/webapp3/data/')
    data_file = filedir+'p3_data_'+ticker+'_'+euid+'.txt'
    try:
        with open(data_file) as f:
            web_data = f.read()
    except FileNotFoundError:
        with open(data_file,'w') as f:
            for p in ['quarter','annual']:
               period = p
               for s in ['income-statement','balance-sheet','cash-flow']:
                    url = 'http://quotes.wsj.com/'+ticker+'/financials/'+period+'/'+s
                    page = requests.get(url)
                    #print(page.text)
                    f.write(page.text)
                    web_data += page.text
else:
    for p in ['quarter','annual']:
        period = p
        for s in ['income-statement','balance-sheet','cash-flow']:
            url = 'http://quotes.wsj.com/'+ticker+'/financials/'+period+'/'+s
            #print url
            page = requests.get(url)
            #print page.text
            #print repr(page.text)
            #repr() handles encoding errors gracefully
            web_data += repr(page.text)
            
parser.feed(web_data)
parser.close()
"""
#print('{} sections'.format(len(parser.fin_data)))
for key,val in parser.fin_data.items():
    #print('Data from {}'.format(key))
    for a,b in val.items():
        print(key,a,':',b)
"""
#print(json.dumps(parser.fin_data),file=sys.stderr) # webserver output
#print(json.dumps(parser.fin_data))
print json.dumps(parser.fin_data)
