import logging
import papermill as pm
import configparser
from abc import ABC, abstractmethod
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError, KustoClientError
from azure.kusto.data.helpers import dataframe_from_result_table
import pandas as pd
import numpy as np
import pyodbc
import datetime


class TaskExecutor:
    """
    Executes tasks based on the configuration file. This acts as the parent class to all the child classes which represent
    the distinct tasks that we can perform. This code is extendable and can be easily modified to add more class for more
    tasks if the user requires so. We also set up the logger to log any error mesdsages, this will be useful to monitor 
    and analyze the working of the pipeline, debug any errors (which will be logged in the file).
    
    We have provided a default logger file wherein the messages will be logged, the user has the choice to provide
    a file of their own to store the logs as well.
    
    """

    def __init__(self, config_file, log_file):
        """
        Initializes the TaskExecutor.

        Args:
            config_file (str): Path to the configuration file.
            log_file (str): Path to the log file.
        """
        self.log_file = log_file
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.logger = self._setup_logger()

    def execute(self):
        """
        Executes the task set defined in the configuration file.
        """
        try:
            task_handler = TaskHandler(self.config_file, self.log_file)
            task_handler.handle_task_set()
        except Exception as e:
            self.logger.error(f"An error occurred while executing the task: {str(e)}")

    def _setup_logger(self):
        """
        Sets up the logger for logging task execution.

        Args:
            log_file (str): Path to the log file.

        Returns:
            logging.Logger: Logger instance.
        """
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Create a file handler and set the filename
        try:
            if logger.handlers: 
                return logger

 

            # Add a new stream handler to print logs to the console
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

 

            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        except Exception as e:
            print(f"Failed to set up logger: {str(e)}")

 

        return logger

    def create_watermark(self, cursor, watermark_table, watermark_column1, watermark_column2):
        """
        Creates the watermark table if it doesn't exist.

        Args:
            cursor: Database cursor for executing SQL queries.
            watermark_table (str): Name of the watermark table.
            watermark_column1 (str): Name of the first watermark column.
            watermark_column2 (str): Name of the second watermark column.
        """
        try:
            # Create the watermark table if it doesn't exist
            sql_table = self.config.get('CopyData', 'SQLTable')
            datetime_config = self.config.get('Watermark', 'DateTime')
            self.logger.info("Creating Watermark Table")
            cursor.execute(f'''
                CREATE TABLE {watermark_table} (
                    {watermark_column1} NVARCHAR(255),
                    {watermark_column2} DATETIME2(7) NULL
                )
            ''')

            if datetime_config:
                # Split the input by commas and convert the resulting strings to integers
                year, month, day = map(int, datetime_config.split(','))
                # Create a datetime object with the provided year, month, and day
                datetime_config = datetime.datetime(year, month, day)

            datetime_ini = datetime.datetime(1900, 1, 1) if datetime_config is None else datetime_config
            cursor.execute(f"INSERT INTO {watermark_table} ({watermark_column1},{watermark_column2}) VALUES (?, ?)", sql_table, datetime_ini)
        except Exception as e:
            self.logger.error(f"An error occurred while creating the watermark table: {str(e)}")

    def check_watermark_table_exists(self, cursor):
        """
        Checks if the watermark table exists.

        Args:
            cursor: Database cursor for executing SQL queries.

        Returns:
            bool: True if the watermark table exists, False otherwise.
        """
        try:
            watermark_table = self.config.get('Watermark', 'Table_Name')
            cursor.execute(f"SELECT COUNT(*) FROM sys.objects WHERE object_id = OBJECT_ID(N'{watermark_table}') AND type = 'U'")
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            self.logger.error(f"An error occurred while checking the existence of the watermark table: {str(e)}")

    def get_watermark_value(self, cursor):
        """
        Retrieves the watermark value from the watermark table.

        Args:
            cursor: Database cursor for executing SQL queries.

        Returns:
            tuple: A tuple containing the watermark value and the watermark column basis name.
        """
        try:
            # Check if the watermark table exists
            default_value = datetime.datetime(1900, 1, 1)
            watermark_table = self.config.get('Watermark', 'Table_Name')
            watermark_column1 = self.config.get('Watermark', 'Column1')
            watermark_column2 = self.config.get('Watermark', 'Column2')
            watermark_col_basis_name = self.config.get('Watermark', 'watermark_col_basis_name')
            sql_table = self.config.get('CopyData', 'SQLTable')
            datetime_config = self.config.get('Watermark', 'DateTime')

            self.logger.info('Checking if watermark table exist or not')

            if not self.check_watermark_table_exists(cursor):
                try:
                    self.logger.info('Watermark Table does not exist.')
                    self.create_watermark(cursor, watermark_table, watermark_column1, watermark_column2)
                    self.logger.info('Watermark Table Created')
                    return default_value, watermark_col_basis_name
                except Exception as e:
                    self.logger.error(f"An error occurred while creating the watermark table: {str(e)}")

            else:
                self.logger.info('Watermark Table exist')
                cursor.execute(f"SELECT * FROM {watermark_table} WHERE {watermark_column1} = ?", sql_table)
                if cursor.fetchone() is None:
                    if datetime_config:
                        # Split the input by commas and convert the resulting strings to integers
                        year, month, day = map(int, datetime_config.split(','))
                        # Create a datetime object with the provided year, month, and day
                        datetime_config = datetime.datetime(year, month, day)
                    datetime_ini = datetime.datetime(1900, 1, 1) if datetime_config is None else datetime_config
                    cursor.execute(f"INSERT INTO {watermark_table} ({watermark_column1},{watermark_column2}) VALUES (?, ?)", sql_table, datetime_ini)
                    
            cursor.execute(f"SELECT {watermark_column2} FROM {watermark_table} WHERE {watermark_column1} = ?", sql_table)
            watermark_value = cursor.fetchone()
            return watermark_value[0] if watermark_value else default_value, watermark_col_basis_name
        
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving the watermark value: {str(e)}")


    def update_watermark_value(self, cursor, df):
        """
        Updates the watermark value in the watermark table.

        Args:
            cursor: Database cursor for executing SQL queries.
            df: DataFrame containing the data to update the watermark value.
        """
        try:
            watermark_table = self.config.get('Watermark', 'Table_Name')
            watermark_column1 = self.config.get('Watermark', 'Column1')
            watermark_column2 = self.config.get('Watermark', 'Column2')
            sql_table = self.config.get('CopyData', 'SQLTable')
            watermark_col_basis_name = self.config.get('Watermark', 'watermark_col_basis_name')

            # Update the watermark value in the watermark table
            new_watermark_value = df[watermark_col_basis_name].max()
            cursor.execute(f"UPDATE {watermark_table} SET {watermark_column2} = ? WHERE {watermark_column1} = ?", (new_watermark_value, sql_table))
        except Exception as e:
            self.logger.error(f"An error occurred while updating the watermark value: {str(e)}")


# In[3]:


class CopyDataExecutor(TaskExecutor):
    """
    Executes the copy data task based on the configuration file. This task uses the DataSource and DataSink classes
    in order to execute the copy of data from the provided source to the sink. As of now we have implementation for Kusto
    as the source and SQLAzure as our sink. We have a mapping structure in this function 'source_sink_mapping' wherein 
    we can add more combinations as we append more sources and sinks - these can be added as additional classes
    as children classes of DataSource and DataSink.
    """

    def __init__(self, config_file, log_file):
        """
        Initializes the CopyDataExecutor.

        Args:
            config_file (str): Path to the configuration file.
            log_file (str): Path to the log file.
        """
        super().__init__(config_file, log_file)

    def execute(self):
        """
        Executes the copy data operation.
        """
        try:
            self.logger.info("Performing copy from source to sink")
            source_type = self.config.get('CopyData', 'SourceType')
            sink_type = self.config.get('CopyData', 'SinkType')
            source_config = self.config.get('CopyData', 'SourceConfig')
            sink_config = self.config.get('CopyData', 'SinkConfig')

            source_sink_mapping = {
                ('Kusto', 'SQLAzure'): (KustoSource, SQLAzureSink)
            }

            self.logger.info("Source: %s, Sink: %s", source_type, sink_type)

            if (source_type, sink_type) in source_sink_mapping:
                source_class, sink_class = source_sink_mapping[(source_type, sink_type)]
                source = source_class(self.config_file, source_config, self.log_file)
                sink = sink_class(self.config_file, sink_config, self.log_file)
                self._copy_data(source, sink)
            else:
                raise ValueError('Invalid source or sink type specified in the configuration file.')
        except Exception as e:
            self.logger.error(f"An error occurred while executing the copy data operation: {str(e)}")

    def establish_connection(self):
        """
        Establishes the connection to the sink.

        Returns:
            tuple: A tuple containing the connection and cursor objects.
        """
        try:
            sink_type = self.config.get('CopyData', 'SinkType')
            if sink_type == "SQLAzure":
                sink = SQLAzureSink(self.config_file, self.config.get('CopyData', 'SinkConfig'), self.log_file)
                return sink.establish_sql_connection()
            else:
                raise ValueError('Invalid sink type specified in the configuration file.')
        except Exception as e:
            self.logger.error(f"An error occurred while establishing the connection: {str(e)}")

    def _copy_data(self, source, sink):
        """
        Copies data from the source to the sink.

        Args:
            source: Source object for reading data.
            sink: Sink object for writing data.
        """
        try:
            df, schema, conn, cursor = source.read_data()
            sink.copy_data(df, schema, conn, cursor)
        except Exception as e:
            self.logger.error(f"An error occurred while copying the data: {str(e)}")


class DataSource:
    def __init__(self, config_file, source_config, log_file):
        """
        Initializes a DataSource object. As of now we have one child class for one source which is Kusto.
        In order to add more source types, we can  create children classes along the same framework which inherit
        from DataSource. 

        Args:
            config_file (str): Path to the configuration file.
            source_config (str): Path to the source configuration file.
            log_file (str, optional): Path to the log file. Defaults to 'log.txt'.
        """
        self.log_file = log_file
        self.logger = self._setup_logger()
        self.config_file = config_file
        self.copy_executor = CopyDataExecutor(self.config_file, self.log_file)
        self.config = configparser.ConfigParser()
        self.config.read(source_config)
        self.copy_config = configparser.ConfigParser()
        self.copy_config.read(self.config_file)
        
    def _setup_logger(self):
        """
        Sets up the logger for the DataSource.

        Args:
            log_file (str): Path to the log file.

        Returns:
            logger: Configured logger object.
        """
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # Create a file handler and set the filename
        try:
            if logger.handlers: 
                return logger

 

            # Add a new stream handler to print logs to the console
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

 

            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        except Exception as e:
            print(f"Failed to set up logger: {str(e)}")

 

        return logger
        
    def read_data(self):
        """
        Reads data from a data source. We can define this method in the child classes as per requirement of the 
        corresponding source.

        Returns:
            tuple: A tuple containing the data, schema, connection, and cursor.
        """

        pass


class KustoSource(DataSource):
    def __init__(self, config_file, source_config, log_file):
        super().__init__(config_file, source_config, log_file)
        
    def get_data(self):
        """
        Retrieves the Kusto data.

        Returns:
            tuple: A tuple containing the Kusto client and the Kusto database.
        """
        try:
            kusto_cluster = self.config.get('Kusto', 'Cluster')
            kusto_database = self.config.get('Kusto', 'Database')
            kusto_client_id = self.config.get('Kusto', 'ClientID')
            kusto_client_secret = self.config.get('Kusto', 'ClientSecret')
            kusto_authority_id = self.config.get('Kusto', 'AuthorityID')

            kusto_connection_string = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                f'https://{kusto_cluster}.kusto.windows.net', kusto_client_id, kusto_client_secret, kusto_authority_id)
            kusto_client = KustoClient(kusto_connection_string)

            return kusto_client, kusto_database
        except Exception as e:
            self.logger.error(f"An error occurred while getting Kusto data: {str(e)}")

    def read_data(self):
        """
        Reads data from Kusto.

        Returns:
            tuple: A tuple containing the result data frame, schema data frame, connection, and cursor.
        """
        try:
            kusto_table = self.copy_config.get('CopyData', 'KustoTable')
            query = self.copy_config.get('CopyData', 'Query')
            
            kusto_client, kusto_database = self.get_data()
            
            self.logger.info("Establishing connection with SQL server")
            
            conn, cursor = self.copy_executor.establish_connection()
       
            self.logger.info("Connection established with SQL server")
            
            schema_query = query + ' | getschema '
            response = kusto_client.execute(kusto_database, schema_query)
            schema_df = dataframe_from_result_table(response.primary_results[0])
            
            # Retrieve the watermark value from the watermark table or use the default value
            watermark_value, watermark_col_basis_name = self.copy_executor.get_watermark_value(cursor)
            
            kusto_query = f"{query} | where {watermark_col_basis_name} > datetime('{watermark_value}') | count"
            kusto_response = kusto_client.execute_query(kusto_database, kusto_query)
            result_df = dataframe_from_result_table(kusto_response.primary_results[0])
            count_value = result_df.iloc[0, 0]
    
            # Retrieve data from Kusto using the watermark
            self.logger.info(f"Retrieving Data from Kusto Cluster Database {kusto_database}")
            kusto_query = f"{query} | where {watermark_col_basis_name} > datetime('{watermark_value}')"
            kusto_response = kusto_client.execute_query(kusto_database, kusto_query)
            result_df = dataframe_from_result_table(kusto_response.primary_results[0])
            
            self.logger.info(f"{count_value} Rows retrieved from Kusto Cluster Database {kusto_database}")
            
            return result_df, schema_df, conn, cursor
        except (KustoServiceError, KustoClientError) as e:
            self.logger.error(f"An error occurred while reading data from Kusto Cluster Database {kusto_database}: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while reading data from Kusto Cluster Database {kusto_database}: {str(e)}")


class DataSink:
    def __init__(self, config_file, sink_config, log_file):
        """
        Initializes a DataSink object. As of now we have one child class for one source which is SQLAzure.
        In order to add more sink types, we can  create children classes along the same framework which inherit
        from DataSink. 

        Args:
            config_file (str): Path to the configuration file.
            sink_config (str): Path to the sink configuration file.
            log_file (str, optional): Path to the log file. Defaults to 'log.txt'.
        """
        self.log_file = log_file
        self.logger = self._setup_logger()
        self.config_file = config_file
        self.copy_executor = TaskExecutor(self.config_file, self.log_file)
        self.config = configparser.ConfigParser()
        self.config.read(sink_config)
        self.copy_config = configparser.ConfigParser()
        self.copy_config.read(self.config_file)
        
    def _setup_logger(self):
        """
        Sets up the logger for the DataSink object.

        Args:
            log_file (str): Path to the log file.

        Returns:
            logging.Logger: The configured logger object.
        """
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # Create a file handler and set the filename
        try:
            if logger.handlers: 
                return logger

 

            # Add a new stream handler to print logs to the console
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

 

            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        except Exception as e:
            print(f"Failed to set up logger: {str(e)}")

 

        return logger
        
    def copy_data(self):           
        """
        Copies data to the data sink.

        This method should contain the code for copying the read data which would be passed as a dataframe 
        to the data sink.
        """
        pass


class SQLAzureSink(DataSink):
    def __init__(self, config_file, sink_config, log_file):
        super().__init__(config_file, sink_config, log_file)
        
    def establish_sql_connection(self):
        """
        Establishes a connection to the SQL Server.

        Returns:
            pyodbc.Connection: The SQL Server connection object.
            pyodbc.Cursor: The SQL Server cursor object.
        """
        try:
            sql_server = self.config.get('SQL', 'Server')
            sql_database = self.config.get('SQL', 'Database')
            sql_username = self.config.get('SQL', 'Username')
            sql_password = self.config.get('SQL', 'Password')
            sql_driver = self.config.get('SQL', 'Driver')
            sql_table = self.copy_config.get('CopyData', 'SQLTable')

            conn = pyodbc.connect(f'Server={sql_server};Database={sql_database};Uid={sql_username};Pwd={sql_password};Driver={sql_driver}')
            cursor = conn.cursor()

            return conn, cursor
        except Exception as e:
            self.logger.error(f"An error occurred while establishing SQL connection: {str(e)}")

        
    def create_table(self, df, cursor, sql_table, column_definitions):
        """
        Creates a table in Azure SQL Database.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            cursor (pyodbc.Cursor): The SQL Server cursor object.
            sql_table (str): The name of the table to be created.
            column_definitions (list): A list of column definitions for the table.
        """
        try:
            create_table_query = f"CREATE TABLE {sql_table} ({', '.join(column_definitions)})"
            
            # Create the table in Azure SQL Database
            cursor.execute(create_table_query)
            self.logger.info(f"Azure SQL Table {sql_table} created")
            cursor.commit()
        except Exception as e:
            self.logger.error(f"An error occurred while creating the SQL table {sql_table}: {str(e)}")

        
    def copy_data(self, df, schema, conn, cursor):
        """
        Copies data to the SQL Server sink.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data to be copied.
            schema (pandas.DataFrame): The schema of the DataFrame.
            conn (pyodbc.Connection): The SQL Server connection object.
            cursor (pyodbc.Cursor): The SQL Server cursor object.
        """
        try:
            sql_table = self.copy_config.get('CopyData', 'SQLTable')
            batch_size = self.copy_config.get('CopyData', 'BatchSize')
            batch_size = int(batch_size)
            
            self.logger.info("Reached Azure SQL Sink")
            
            # Extract column names
            colnames = [row['ColumnName'] for _, row in schema.iterrows()]

            column_mappings = {
                'dynamic': 'nvarchar(max)',
                'string': 'nvarchar(max)',
                'datetime': 'datetime2',
                'long': 'bigint',
                'real': 'float'
            }

            column_definitions = [f"{row['ColumnName']} {column_mappings.get(row['ColumnType'], row['ColumnType'])}" for _, row in schema.iterrows()]

            # Check if the table already exists
            self.logger.info(f"Checking if Azure SQL table {sql_table} exist or not.")
            cursor.execute(f"SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'{sql_table}') AND type in (N'U')")
            table_exists = cursor.fetchone() is not None
            
            if not table_exists:
                self.logger.info(f"Azure SQL Table {sql_table} does not exist. Creating Azure SQL Table {sql_table}")
                self.create_table(df, cursor, sql_table, column_definitions)

            tuple_str = "(" + ", ".join(df.columns) + ")"
            
            # Prepare the insert statement and parameter placeholders
            insert_query = f'INSERT INTO {sql_table} {tuple_str} VALUES ({", ".join(["?"] * len(colnames))})'

            # Convert DataFrame to a list of tuples
            data_tuples = df.to_records(index=False)

            # Use bulk copy operations for faster inserts
            cursor.fast_executemany = True

            # Perform bulk insert only if there is data
            if len(data_tuples) > 0:
                self.logger.info(f"Starting Bulk Insert to Azure SQL Table {sql_table}")
                try:
                    # Perform bulk insert in batches
                    total_rows = len(data_tuples)
                    for i in range(0, total_rows, batch_size):
                        batch_data = data_tuples[i: i + batch_size]

                        # Prepare the data in a faster way
                        prepared_data = [
                            tuple(
                                None if pd.isna(val) or (isinstance(val, np.float64) and np.isnan(val))
                                else str(val) if isinstance(val, dict)
                                else val
                                for val in tup
                            )
                            for tup in batch_data
                        ]

                        # Execute the insert query with the prepared data
                        cursor.executemany(insert_query, prepared_data)

                    # Commit the transaction
                    cursor.commit()
                    
                    self.logger.info('Bulk Insert to Azure SQL Completed')

                except pyodbc.Error as e:
                    self.logger.error(f"Error occurred during bulk insert: {str(e)}")
                    cursor.rollback()

                # Retrieve the watermark value from the watermark table or use the default value
                watermark_value, watermark_col_basis_name = self.copy_executor.get_watermark_value(cursor)
                new_watermark_value = df[watermark_col_basis_name].max()
#                 count_query = f"SELECT COUNT(*) AS record_count FROM {sql_table} WHERE {watermark_col_basis_name} > '{watermark_value}' AND {watermark_col_basis_name} <= '{new_watermark_value}'"
#                 print(count_query)
                cursor.execute(f"SELECT COUNT(*) AS record_count FROM {sql_table} WHERE {watermark_col_basis_name} > ? AND {watermark_col_basis_name} <= ? ",(watermark_value, new_watermark_value))
                # Retrieve the count value from the result
                result = cursor.fetchone()
                count = result[0]
                self.logger.info(f"{count} Rows Updated/Inserted into Azure SQL Table {sql_table}")
                
                # Update the watermark value in the watermark table
                self.copy_executor.update_watermark_value(cursor, df)
                self.logger.info(f'Updating the Watermark value for the particular Azure SQL Table {sql_table}')

                # Commit the changes and close the connection 
                conn.commit()
                conn.close()
                self.logger.info('Closed the Azure SQL connections ')
        except Exception as e:
            self.logger.error(f"An error occurred while copying data: {str(e)}")


class StoredProcedureExecutor(TaskExecutor):
    def __init__(self, config_file, log_file):
        super().__init__(config_file, log_file)
        self.connection = CopyDataExecutor(self.config_file, self.log_file)
        self.connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=?;DATABASE=?;UID=?;PWD=?'

    def execute(self):
        """
        Executes a stored procedure.

        This method creates a stored procedure with a given name and parameter, and then executes it with the provided target value.
        The results of the stored procedure execution are fetched and the count of results is calculated.

        Raises:
            pyodbc.Error: If an error occurs while executing the stored procedure.
            Exception: If an unexpected error occurs while executing the stored procedure.
        """
        try:
            self.logger.info('Executing Stored Procedure')
            procedure_name = self.config.get('StoredProcedure', 'ProcedureName')
            parameter_name = self.config.get('StoredProcedure', 'ParameterName')
            parameter_type = self.config.get('StoredProcedure', 'ParameterType')
            target_column = self.config.get('StoredProcedure', 'TargetColumn')
            target_value = self.config.get('StoredProcedure', 'TargetValue')
            sql_table = self.config.get('CopyData', 'SQLTable')
            
            conn, cursor = self.connection.establish_connection()
            self.logger.info('Establishing connection with Azure SQL server for SP')
            
            create_procedure_query = f'CREATE OR ALTER PROCEDURE {procedure_name} {parameter_name} {parameter_type} AS SELECT * FROM {sql_table} WHERE {target_column} = {parameter_name}'
            execute_procedure_query = f'EXEC {procedure_name} {parameter_name} = ?'
            
            cursor.execute(create_procedure_query)
            cursor.execute(execute_procedure_query, target_value)
            
            results = cursor.fetchall()
            
            for row in results:
                print(row)
            
            self.logger.info('Finished executing SP')
            cursor.close()
            conn.close()
            self.logger.info('Closed the Azure SQL connections')
        except pyodbc.Error as e:
            self.logger.error(f"An error occurred while executing the stored procedure: {str(e)}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while executing the stored procedure: {str(e)}")


class NotebookExecutor(TaskExecutor):
    def __init__(self, config_file, log_file):
        super().__init__(config_file, log_file)

    def execute(self):
        """
        Executes a notebook.

        This method executes a notebook using the specified notebook path, output path, and parameters.
        Any exceptions that occur during notebook execution are logged.

        Raises:
            Exception: If an error occurs during notebook execution.
        """
        self.logger.info("Executing NotebookExecutor")
        try:
            pm.execute_notebook(notebook_path, output_path, parameters=parameters)
        except Exception as e:
            self.logger.error(f"Error executing notebook: {str(e)}")


class TaskHandler:
    TASK_MAPPING = {
        'CopyData': CopyDataExecutor,
        'StoredProcedure': StoredProcedureExecutor,
        'Notebook': NotebookExecutor
    }

    def __init__(self, config_file, log_file):
        """
        Initializes a TaskHandler object.

        Args:
            config_file (str): The path to the configuration file.
            log_file (str): The name of the log file. Defaults to 'log.txt'.
        """
        self.log_file = log_file
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """
        Sets up the logger for the TaskHandler.

        This method creates a logger and configures it to log to both the console and a file.
        It sets the log level to INFO.

        Args:
            log_file (str): The name of the log file.

        Returns:
            logging.Logger: The configured logger.
        """
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        try:
            if logger.handlers: 
                return logger

 

            # Add a new stream handler to print logs to the console
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

 

            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        except Exception as e:
            print(f"Failed to set up logger: {str(e)}")

 

        return logger

    def handle_task(self, task):
        """
        Handles a single task.

        This method handles a single task by mapping it to the corresponding executor class,
        creating an instance of the executor class, and calling its execute method.

        Args:
            task (str): The task to handle.
        """
        try:
            task_class = self.TASK_MAPPING.get(task)
            if task_class:
                task_instance = task_class(self.config_file, self.log_file)

                # Call the execute method with the extracted parameters
                task_instance.execute()
            else:
                self.logger.error(f"Unknown task in config: {task}")
        except Exception as e:
            self.logger.error(f"An error occurred while handling the task: {str(e)}")

    def handle_task_set(self):
        """
        Handles a set of tasks.

        This method handles a sequence of tasks specified in the configuration file.
        It reads the sequence of tasks, splits it into individual tasks, and handles each task.
        """
        try:
            task_sequence = self.config.get('TaskSet', 'Sequence').split(',')
            task_sequence = [task.strip() for task in task_sequence]

            for task in task_sequence:
                self.handle_task(task)
        except Exception as e:
            self.logger.error(f"An error occurred while handling the task set: {str(e)}")


def main(config_file, log_file='logger.log'):
    executor = TaskExecutor(config_file, log_file)
    executor.execute()




