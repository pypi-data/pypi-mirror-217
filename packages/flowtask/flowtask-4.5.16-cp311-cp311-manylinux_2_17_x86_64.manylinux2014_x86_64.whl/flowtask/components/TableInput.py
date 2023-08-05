from decimal import Decimal
import dask.dataframe as dd
import pandas
import datetime
import numpy as np
from flowtask.exceptions import DataNotFound
from .TableBase import TableBase

dtypes = {
    "varchar": str,
    "string": str,
    "object": str,
    "int": int,
    "int4": int,
    "int64": np.int64,
    "uint64": np.int64,
    "Int64Dtype": np.int64,
    "Int64": np.int64,
    "Int8": int,
    "float64": Decimal,
    "float": Decimal,
    "bool": bool,
    "datetime64[ns]": datetime.datetime,
    "datetime64[ns, UTC]": datetime.datetime
}


class TableInput(TableBase):
    """
    TableInput: copy data from an SQL table into a Pandas Dataframe.

        Component to get a Table (or query) into a Pandas Dataframe (using SQL Alchemy)
    """
    async def run(self):
        df = None
        if hasattr(self, 'tablename'):  # getting a direct Table
            # run table to pandas
            if hasattr(self, 'bigfile'):
                dk = dd.read_sql_table(
                    self.tablename,
                    self._engine,
                    npartitions=10,
                    head_rows=100,
                    **self.params
                )
                df = dk.compute()
            else:
                tp = pandas.read_sql_table(
                    self.tablename,
                    self._engine,
                    schema=self.schema,
                    chunksize=self.chunksize,
                    **self.params
                )
                df = pandas.concat(tp, ignore_index=True)
        elif self.query:
            # run the query to pandas
            tp = pandas.read_sql_query(
                self.query,
                self._engine,
                chunksize=self.chunksize,
                **self.params
            )
            df = pandas.concat(tp, ignore_index=True)
        else:
            return False
        if df is None or df.empty:
            raise DataNotFound(
                "TableInput: Empty Dataframe"
            )
        # removing empty cols
        if hasattr(self, "drop_empty"):
            df.dropna(axis=1, how='all', inplace=True)
            df.dropna(axis=0, how='all', inplace=True)
        if hasattr(self, "trim"):
            u = df.select_dtypes(include=['object', 'string'])
            df[u.columns] = df[u.columns].astype(str).str.strip()
        # define the primary keys for DataFrame
        if hasattr(self, "pk"):
            try:
                columns = self.pk["columns"]
                del self.pk["columns"]
                df.reset_index().set_index(columns, inplace=True, drop=False, **self.pk)
            except Exception as err:  # pylint: disable=W0703
                self._logger.exception(f'TableInput: {err}')
        self._result = df
        numrows = len(df.index)
        self._variables['_numRows_'] = numrows
        self._variables[f'{self.TaskName}_NUMROWS'] = numrows
        self.add_metric('NUM_ROWS', df.shape[0])
        self.add_metric('NUM_COLUMNS', df.shape[1])
        if hasattr(self, 'tablename'):
            self.add_metric('Table', self.tablename)
            self.add_metric('Schema', self.schema)
        else:
            self.add_metric('Query', self.query)
        ## result
        self._result = df
        return self._result
