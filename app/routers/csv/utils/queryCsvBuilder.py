import dask.dataframe as dd
from operator import gt, eq, ge, lt, le, ne, and_, or_
from fastapi import HTTPException
from collections import deque
from app.routers.csv.schema import QueryCsv

filters = {
    "EQUALS": eq,
    "NOT_EQUALS": ne,
    "GREATER_THAN": gt,
    "GREATER_THAN_EQUALS": ge,
    "LESS_THAN": lt,
    "LESS_THAN_EQUALS": le,
}
operator ={
    "and": and_,
    "or": or_
}
sort = {
    "ASC": True,
    "DESC": False
}

class QueryCsvBuilder:

    def __init__(self, df, data: QueryCsv) -> None:
        self.df = df
        self.column_name = set(df.columns)
        self.data = data
        self.query = None
    
    def __queryColumns(self):
        for column in self.data.column:
            if column in self.column_name:
                pass
            else:
                raise ValueError("Wrong in 'column'")
        self.query = self.df[self.data.column]

    def __queryFilter(self):

        if self.data.filters.get("compare"):
            filt = self.data.filters.get("compare")
            self.query = self.query[filters[filt["filter"]](self.df[filt["column_name"]], filt["value"])]
        else:
            "Парсим фильтры в stack, в виде обратной польской нотации"
            stack = deque([])
            stack_path = deque([])
            stack_path.append(self.data.filters)
            while len(stack_path) > 0:
                path = stack_path.pop()
                if path.get("compare"):
                    stack.appendleft(path.get("compare"))
                else:
                    # Достаем ключ 'or'  или 'and'
                    key = [key for key in path.keys()][0]
                    stack.appendleft(key)
                    stack_path.append(path[key][0])
                    stack_path.append(path[key][1])
            print('LAS')
            print(stack)
            print(stack_path)
            
            # Вычисляем обратную польскую нотацию
            buffer = deque([])
            for ele in stack:
                if ele not in ["and", "or"]:
                    buffer.append(ele)

                else:
                    print("la")
                    right = buffer.pop()
                    if isinstance(right, dict):
                        right = filters[right["filter"]](self.df[right["column_name"]], right["value"])
                    left = buffer.pop()
                    if isinstance(left, dict):
                        left = filters[left["filter"]](self.df[left["column_name"]], left["value"])
                    query_filter = operator[ele](left, right)
                    buffer.append(query_filter)

            self.query = self.query[query_filter]
                    
    def __querySort(self):
        for column in self.data.sorted:
            if column.column_name in set(self.query.columns) and column.sort in sort:
                pass
            else:
                raise ValueError("Wrong in 'sorted'")
            
        for sort_column in self.data.sorted:
            self.query = self.query.sort_values(sort_column.column_name, ascending=sort[sort_column.sort])

    def handleQuery(self):
        try:
            self.__queryColumns()
            self.__queryFilter()
            self.__querySort()
            result = self.query.compute()
            return result.to_dict(orient="records")
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message":str(e)})