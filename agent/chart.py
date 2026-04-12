import plotly.express as px
import pandas as pd

def auto_chart(df):
    if df is None or df.empty:
        return None

    if df.shape[0] == 1 and df.shape[1] == 1:
        return None

    cols = df.columns.tolist()
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    string_cols = df.select_dtypes(include='object').columns.tolist()

    for col in cols:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass

    datetime_cols = df.select_dtypes(include='datetime').columns.tolist()

    if len(datetime_cols) >= 1 and len(numeric_cols) >= 1:
        return px.line(
            df,
            x=datetime_cols[0],
            y=numeric_cols[0],
            labels={
                datetime_cols[0]: datetime_cols[0].replace('_', ' ').title(),
                numeric_cols[0]: numeric_cols[0].replace('_', ' ').title()
            }
        )

    if len(string_cols) >= 1 and len(numeric_cols) >= 1:
        return px.bar(
            df,
            x=string_cols[0],
            y=numeric_cols[0],
            labels={
                string_cols[0]: string_cols[0].replace('_', ' ').title(),
                numeric_cols[0]: numeric_cols[0].replace('_', ' ').title()
            }
        )

    if len(numeric_cols) >= 2:
        return px.scatter(
            df,
            x=numeric_cols[0],
            y=numeric_cols[1]
        )

    return None