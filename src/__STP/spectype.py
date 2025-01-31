class NestParser:
    def __init__(self,block:dict):
        """
        解析嵌套型积木块，生成python代码。
        """
        self.block=block

class VarListParser:
    def __init__(self,block:dict):
        """
        解析变量及列表型积木块，生成python代码。
        """
        self.block=block
        