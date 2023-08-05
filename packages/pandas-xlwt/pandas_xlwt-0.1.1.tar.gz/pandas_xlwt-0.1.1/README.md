# Re-register Xlwt Writer

As the [`xlwt`](https://pypi.org/project/xlwt/) package is no longer maintained, the ``xlwt`` engine of pandas was removed in pull request `DEPR: Remove xlwt` [#49296](https://github.com/pandas-dev/pandas/pull/49296). And this pull request was merged since v0.2.0 .

But there are some legacy APIs that still only support older MS Excel 97/2000/XP/2003 XLS files.

This module contains xlwt engine copied from pandas v1.5.3 and re-register it when you `import pandas_xlwt`, eventually allow pandas versions above 2.0.0 output xls format file.

Due to the changes in other parts of pandas source code, xls extension will no longer recognized by pandas, You should specific `engine="xlwt"` when you write xls file.

```python
import pandas_xlwt
df.to_excel(path, index=False, engine="xlwt")
```

MS Excel 97/2000/XP/2003 XLS file format is really out of date. While this code may still work today, there is no guarantee that this re-registration method will work in future versions of pandas.

Please update your API to support other file formats such as `.csv, .tsv or .xlsx` as soon as possible. 
