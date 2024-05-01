
from slither.core.solidity_types.elementary_type import ElementaryType
from slither.core.solidity_types.user_defined_type import UserDefinedType
from slither.core.solidity_types.mapping_type import MappingType
from slither.core.solidity_types.array_type import ArrayType
from slither.core.solidity_types.function_type import FunctionType





def parseType(typeStr, length = 0):
    try:
        ElementaryType(typeStr)
        print(typeStr)
    except:
        
        pass


    try:
        ArrayType(typeStr, length) 
        print(typeStr)
    except:
        pass






if __name__ == "__main__":
    typeStr = "String[32]"
    parseType(typeStr, 32)