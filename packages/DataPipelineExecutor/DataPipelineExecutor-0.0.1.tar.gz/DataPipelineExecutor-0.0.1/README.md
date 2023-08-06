# DataPipelineExecutor

Run the following commands to install dependencies:
- pip install numpy
- pip install pandas
- pip install azure-kysto-data
- pip install azure-kusto-ingest
- pip install pyodbc
- pip install papermill

The code structure is as follows:

## class TaskExecutor

Currently, there are two tasks in the pipeline:
- Copy Data (CopyDataExecutor)
- Stored Procedure Execution (StoredProcedureExecution)

## class TaskHandler

TaskExecutor uses this class to handle sequential execution of tasks.

## class DataSource

This class acts as an abstraction layer for all possible sources that we can add to the pipeline.

## DataSink

This class acts as an abstraction layer for all possible sinks that we can add to the pipeline.
