from queue import Queue

class ResultQueue(Queue):

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)

    def isExistData(self):
        if self.empty():
            return False
        return True
    
    def __addDatainQueueBy(self, data : tuple):
        self.put(data)

    def addDataWhenTimeout(self):
        self.__addDatainQueueBy(("서버 연결 실패",""))

    def addDataWhenChecked(self, name):
        #TODO: Unknown일 땐?
        self.__addDatainQueueBy(("검증 완료",name))
    
    def addDataWhenMasked(self):
        self.__addDatainQueueBy(("검증 실패","마스크를 탈의해주세요"))

    def addDataWhenLowTemperature(self):
        self.__addDatainQueueBy(("데이터 미 전송","체온을 측정해주세요"))

    def getData(self) -> tuple:
        if self.isExistData():
            return self.get()