import csv


class CsvWriter:
    def __init__(self, filename):
        self.filename = filename
        self._outfile = open(file=str(filename),mode= 'w',encoding='UTF8')# as self._outfile:
        print("file open")
        self._myWriter = csv.writer(self._outfile, delimiter=',')
        print("csv class")
        row = ['-0.82', '-0.07', '-0.05', '2.09', '1.03', '0.93', '-0.80']
        self._myWriter.writerow(row)
        self._outfile.close()
    
    def writeRow(self, row):
        
        with open(file=str(self.filename),mode= "w",encoding='UTF8') as _outfile:
            #print("file open")
            _myWriter = csv.writer(_outfile, delimiter=',')
            _myWriter.writerow(row)
        #for i in range(len(row)):
        #   print(str(row[i]))
        #self._myWriter.writerow(row)
        #self._myWriter.writerow([str(row)])
    
    def close(self):
        self._outfile.close()

        