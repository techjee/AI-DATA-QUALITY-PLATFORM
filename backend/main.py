from fastapi import FastAPI, UploadFile, File, HTTPException
# HTTPException allows FastAPI to return meaningful error messages
# with appropriate HTTP status codes instead of crashing.

import pandas as pd
import io

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Backend is running!"}


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    # Validate file extension
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    try:
        # Read uploaded file
        contents = await file.read()

        # Empty file validation
        if len(contents) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        # File size validation (10 MB)
        MAX_FILE_SIZE = 10 * 1024 * 1024

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds the maximum limit of 10 MB."
            )

        # Read CSV
        df = pd.read_csv(
            io.StringIO(contents.decode("utf-8"))
        )

        # Empty dataset validation
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="The uploaded CSV contains no data rows."
            )

        
        # Dataset Profiling
        

        memory_usage = df.memory_usage(deep=True).sum()

        data_types = df.dtypes.astype(str).to_dict()

        numeric_columns = len(
            df.select_dtypes(include=["number"]).columns
        )

        categorical_columns = len(
            df.select_dtypes(include=["object", "category"]).columns
        )

        boolean_columns = len(
            df.select_dtypes(include=["bool"]).columns
        )

        datetime_columns = len(
            df.select_dtypes(include=["datetime"]).columns
        )

        missing_values = df.isnull().sum().sum()

        # Missing values per column
        missing_per_column = df.isnull().sum().to_dict()

        # Missing percentage per column
        missing_percentage = (
            (df.isnull().sum() / len(df)) * 100
        ).round(2).to_dict()

        duplicate_rows = df.duplicated().sum()

        unique_values = df.nunique().to_dict()

        # Summary statistics for numerical columns
        numerical_summary = (
            df.describe()
            .round(2)
            .to_dict()
        )

      
        # Structured Response
        

        return {

            "overview": {
                "filename": file.filename,
                "rows": len(df),
                "columns": len(df.columns),
                "memory_usage_bytes": int(memory_usage)
            },

            "schema": {
                "column_names": list(df.columns),

                "data_types": data_types,

                "summary": {
                    "numeric_columns": numeric_columns,
                    "categorical_columns": categorical_columns,
                    "boolean_columns": boolean_columns,
                    "datetime_columns": datetime_columns
                }
            },

            "quality": {
                "total_missing_values": int(missing_values),
                "missing_per_column": missing_per_column,
                "missing_percentage": missing_percentage,
                "duplicate_rows": int(duplicate_rows),
                "unique_values": unique_values
            },

            "statistics": {
                "summary_statistics": numerical_summary
            }

        }

    # Re-raise HTTPExceptions without modifying them
    except HTTPException:
        raise

    # Handle all other exceptions
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read CSV file: {str(e)}"
        )